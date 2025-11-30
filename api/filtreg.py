from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import TruncDate, Cast
from datetime import datetime
from .models import DonneeCollectee
from .serializers import DonneeCollecteeSerializer
from rest_framework import generics

class TotalCollectedDataPagination(PageNumberPagination):
    page_size = 10  # Nombre d'éléments par page
    page_size_query_param = 'page_size'
    max_page_size = 100

class TotalCollectedDataView(generics.GenericAPIView):
    pagination_class = TotalCollectedDataPagination
    permission_classes = [IsAuthenticated]  # Require the user to be authenticated
    serializer_class = DonneeCollecteeSerializer

    # Ajout de l'attribut queryset
    queryset = DonneeCollectee.objects.all()  # Définir le queryset par défaut

    def post(self, request, *args, **kwargs):
        filters_dict = request.data

        # Initialiser le queryset
        queryset = self.get_queryset()  # Utilisez le queryset défini

        # Récupérer les filtres de plage de dates
        start_date_str = filters_dict.get('start_date')
        end_date_str = filters_dict.get('end_date')

        # Convertir les chaînes de date en objets datetime.date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        # Appliquer les filtres de date
        if start_date and end_date:
            queryset = queryset.filter(create__date__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(create__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(create__date__lte=end_date)

        # Dictionnaire de correspondance pour les champs
        field_mapping = {
            'entreprise': 'entreprise',
            'Marque': 'Marque',
            'district': 'district',
            'region': 'region',
            'commune': 'commune',
            'ville': 'ville',
            'quartier': 'quartier',
            'type_support': 'type_support',
            'canal': 'canal',
            'etat_support': 'etat_support',
            'typesite': 'typesite',
            'visibilite': 'visibilite',
            'anciennete': 'anciennete',
            'duree': 'duree',
            'surface': 'surface'
        }

        # Appliquer les filtres dynamiques
        for key, value in filters_dict.items():
            if key in field_mapping and key not in ['start_date', 'end_date']:
                field_name = field_mapping[key]
                queryset = queryset.filter(**{f'{field_name}__icontains': value})

        # Pagination des résultats
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)

        # Agrégation par district, région, commune, et marque
        districts_aggregations = {}
        districts = queryset.values('district').distinct()

        for district_data in districts:
            district_name = district_data['district']
            regions_aggregations = {}
            regions = queryset.filter(district=district_name).values('region').distinct()

            for region_data in regions:
                region_name = region_data['region']
                communes_aggregations = {}
                communes = queryset.filter(region=region_name).values('commune').distinct()

                for commune_data in communes:
                    commune_name = commune_data['commune']
                    marque_aggregations = {}
                    marques = queryset.filter(commune=commune_name).values('Marque').distinct()  # Changez ici aussi

                    for marque_data in marques:
                        marque_name = marque_data['Marque']  # Changez ici aussi
                        marque_etat_aggregations = {}

                        for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                            etat_aggregations = queryset.filter(
                                commune=commune_name, Marque=marque_name, etat_support=etat_support  # Changez ici aussi
                            ).annotate(
                                date=TruncDate('create')
                            ).values('date').annotate(
                                nombre_total=Count('id'),
                                montant_total_tsp=Sum(Cast('TSP', FloatField())),
                                montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                                montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                            )

                            # Ajouter la somme des montants pour chaque état
                            somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in etat_aggregations)
                            somme_montant_total_odp = sum(item['montant_total_odp'] for item in etat_aggregations)
                            somme_montant_total = sum(item['montant_total'] for item in etat_aggregations)

                            marque_etat_aggregations[etat_support] = {
                                'somme_montant_total_tsp': somme_montant_total_tsp,
                                'somme_montant_total_odp': somme_montant_total_odp,
                                'somme_montant_total': somme_montant_total,
                                'nombre_total': sum(item['nombre_total'] for item in etat_aggregations),
                            }

                        # Agrégation totale pour la marque dans chaque commune
                        marque_total_aggregation = queryset.filter(
                            commune=commune_name, Marque=marque_name  # Changez ici aussi
                        ).aggregate(
                            somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                            somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                            somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                            nombre_total=Count('id'),
                        )

                        marque_etat_aggregations['Total'] = {
                            'somme_montant_total_tsp': marque_total_aggregation['somme_montant_total_tsp'] or 0,
                            'somme_montant_total_odp': marque_total_aggregation['somme_montant_total_odp'] or 0,
                            'somme_montant_total': marque_total_aggregation['somme_montant_total'] or 0,
                            'nombre_total': marque_total_aggregation['nombre_total'] or 0,
                        }

                        marque_aggregations[marque_name] = marque_etat_aggregations

                    communes_aggregations[commune_name] = {
                        'marques': marque_aggregations
                    }

                regions_aggregations[region_name] = {
                    'communes': communes_aggregations
                }

            districts_aggregations[district_name] = {
                'regions': regions_aggregations
            }

        return paginator.get_paginated_response({
            'districts_aggregations': districts_aggregations,
        })
