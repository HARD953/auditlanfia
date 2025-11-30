from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import TruncDate, Cast, Coalesce
from .models import DonneeCollectee
from .serializers import DonneeCollecteeSerializer
from datetime import datetime

class GTotalCollectedDataView(generics.GenericAPIView):
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

        # Initialize total aggregations
        total_aggregations = {}

        # Check if the user is authenticated
        if request.user.is_authenticated:
            if hasattr(request.user, 'is_agent') and request.user.is_agent:
                # Aggregations for agents
                for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                    etat_aggregations = queryset.filter(
                        etat_support=etat_support, is_deleted=False
                    ).annotate(
                        date=TruncDate('create')
                    ).values('date').annotate(
                        nombre_total=Count('id'),
                        montant_total_tsp=Sum(Cast('TSP', FloatField())),
                        montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                        montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                    )

                    # Sum amounts for each state
                    somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in etat_aggregations)
                    somme_montant_total_odp = sum(item['montant_total_odp'] for item in etat_aggregations)
                    somme_montant_total = sum(item['montant_total'] for item in etat_aggregations)

                    total_aggregations[etat_support] = {
                        'somme_montant_total_tsp': somme_montant_total_tsp,
                        'somme_montant_total_odp': somme_montant_total_odp,
                        'somme_montant_total': somme_montant_total,
                        'nombre_total': sum(item['nombre_total'] for item in etat_aggregations),
                    }

                # Global aggregation without state distinction
                total_aggregations['Total'] = queryset.filter(
                    is_deleted=False
                ).aggregate(
                    somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                    somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                    somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                    nombre_total=Count('id'),
                )
            elif hasattr(request.user, 'entreprise'):
                # Aggregations for enterprise users
                for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                    etat_aggregations = queryset.filter(
                        entreprise=request.user.entreprise, etat_support=etat_support, is_deleted=False
                    ).annotate(
                        date=TruncDate('create')
                    ).values('date').annotate(
                        nombre_total=Count('id'),
                        montant_total_tsp=Sum(Cast('TSP', FloatField())),
                        montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                        montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                    )

                    # Sum amounts for each state
                    somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in etat_aggregations)
                    somme_montant_total_odp = sum(item['montant_total_odp'] for item in etat_aggregations)
                    somme_montant_total = sum(item['montant_total'] for item in etat_aggregations)

                    total_aggregations[etat_support] = {
                        'somme_montant_total_tsp': somme_montant_total_tsp,
                        'somme_montant_total_odp': somme_montant_total_odp,
                        'somme_montant_total': somme_montant_total,
                        'nombre_total': sum(item['nombre_total'] for item in etat_aggregations),
                    }

                # Global aggregation without state distinction
                total_aggregations['Total'] = queryset.filter(
                    entreprise=request.user.entreprise, is_deleted=False
                ).aggregate(
                    somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                    somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                    somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                    nombre_total=Count('id'),
                )
        else:
            return Response({"error": "Non autorisé"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'total_aggregations': total_aggregations,
        }, status=status.HTTP_200_OK)
