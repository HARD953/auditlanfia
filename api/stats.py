from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.db.models import FloatField
from django.db.models.functions import Cast
from .models import DonneeCollectee
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .serializers import DonneeCollecteeSerializer
from rest_framework import generics

class TotalCollectedDataView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Require the user to be authenticated
    serializer_class = DonneeCollecteeSerializer

    def post(self, request, *args, **kwargs):
        filters_dict = self.request.data

        # Initialize the queryset
        queryset = DonneeCollectee.objects.all()  # Make sure to initialize the queryset

        # Get date range filters
        start_date_str = filters_dict.get('start_date')
        end_date_str = filters_dict.get('end_date')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        # Apply date filters
        if start_date and end_date:
            queryset = queryset.filter(create__date__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(create__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(create__date__lte=end_date)

        # Field mapping
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

        # Apply dynamic filters
        for key, value in filters_dict.items():
            if key in field_mapping and key not in ['start_date', 'end_date']:
                field_name = field_mapping[key]
                queryset = queryset.filter(**{f'{field_name}__icontains': value})

        # Agrégations par commune avec les filtres de date
        if self.request.user.is_agent:
            communes_aggregations = {}
            communes = DonneeCollectee.objects.filter(**date_filters,is_deleted="False").values('commune').distinct()
            for commune_data in communes:
                commune = commune_data['commune']
                commune_aggregations = {}
                for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                    commune_etat_aggregations = DonneeCollectee.objects.filter(
                        commune=commune, etat_support=etat_support, **date_filters
                    ).annotate(
                        date=TruncDate('create')
                    ).values('date').annotate(
                        nombre_total=Count('id'),
                        montant_total_tsp=Sum(Cast('TSP', FloatField())),
                        montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                        montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                    )

                    # Ajouter la somme des montants pour chaque état
                    somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in commune_etat_aggregations)
                    somme_montant_total_odp = sum(item['montant_total_odp'] for item in commune_etat_aggregations)
                    somme_montant_total = sum(item['montant_total'] for item in commune_etat_aggregations)

                    commune_aggregations[etat_support] = {
                        'somme_montant_total_tsp': somme_montant_total_tsp,
                        'somme_montant_total_odp': somme_montant_total_odp,
                        'somme_montant_total': somme_montant_total,
                        'nombre_total': sum(item['nombre_total'] for item in commune_etat_aggregations),
                    }

                # Ajouter une agrégation pour la somme totale sans distinction des états
                commune_total_aggregation = DonneeCollectee.objects.filter(
                    commune=commune, **date_filters
                ).aggregate(
                    somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                    somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                    somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                    nombre_total=Count('id'),
                )

                commune_aggregations['Total'] = {
                    'somme_montant_total_tsp': commune_total_aggregation['somme_montant_total_tsp'] or 0,
                    'somme_montant_total_odp': commune_total_aggregation['somme_montant_total_odp'] or 0,
                    'somme_montant_total': commune_total_aggregation['somme_montant_total'] or 0,
                    'nombre_total': commune_total_aggregation['nombre_total'] or 0,
                }

                communes_aggregations[commune] = commune_aggregations
        else:
            communes_aggregations = {}
            communes = DonneeCollectee.objects.filter(
                entreprise=self.request.user.entreprise, **date_filters,is_deleted="False"
            ).values('commune').distinct()
            for commune_data in communes:
                commune = commune_data['commune']
                commune_aggregations = {}
                for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                    commune_etat_aggregations = DonneeCollectee.objects.filter(
                        commune=commune, etat_support=etat_support, entreprise=self.request.user.entreprise,
                        **date_filters
                    ).annotate(
                        date=TruncDate('create')
                    ).values('date').annotate(
                        nombre_total=Count('id'),
                        montant_total_tsp=Sum(Cast('TSP', FloatField())),
                        montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                        montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                    )

                    # Ajouter la somme des montants pour chaque état
                    somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in commune_etat_aggregations)
                    somme_montant_total_odp = sum(item['montant_total_odp'] for item in commune_etat_aggregations)
                    somme_montant_total = sum(item['montant_total'] for item in commune_etat_aggregations)

                    commune_aggregations[etat_support] = {
                        'somme_montant_total_tsp': somme_montant_total_tsp,
                        'somme_montant_total_odp': somme_montant_total_odp,
                        'somme_montant_total': somme_montant_total,
                        'nombre_total': sum(item['nombre_total'] for item in commune_etat_aggregations),
                    }

                # Ajouter une agrégation pour la somme totale sans distinction des états
                commune_total_aggregation = DonneeCollectee.objects.filter(
                    commune=commune, entreprise=self.request.user.entreprise, **date_filters
                ).aggregate(
                    somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                    somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                    somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                    nombre_total=Count('id'),
                )

                commune_aggregations['Total'] = {
                    'somme_montant_total_tsp': commune_total_aggregation['somme_montant_total_tsp'] or 0,
                    'somme_montant_total_odp': commune_total_aggregation['somme_montant_total_odp'] or 0,
                    'somme_montant_total': commune_total_aggregation['somme_montant_total'] or 0,
                    'nombre_total': commune_total_aggregation['nombre_total'] or 0,
                }

                communes_aggregations[commune] = commune_aggregations

        return Response({
            'communes_aggregations': communes_aggregations,
        }, status=status.HTTP_200_OK)
