from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.db.models import FloatField
from django.db.models.functions import Cast
from .models import DonneeCollectee
from datetime import datetime
from custumer.models import CustomUser

class StatsByAgent(APIView):
    def get(self, request, agent_id=None, start_date=None, end_date=None):
        # Convertir les dates en objets date si elles sont fournies
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Définir les filtres de date en fonction des paramètres fournis
        date_filters = {}
        if start_date:
            date_filters['create__date__gte'] = start_date
        if end_date:
            date_filters['create__date__lte'] = end_date

        # Filtrer les utilisateurs en fonction de l'ID de l'agent
        utilisateurs_filter = {'id': agent_id} if agent_id else {}

        # Liste pour stocker les agrégations des utilisateurs
        utilisateurs_aggregations = []

        # Agrégations par utilisateur
        utilisateurs = CustomUser.objects.filter(**utilisateurs_filter).values('id').distinct()
        for utilisateur_data in utilisateurs:
            utilisateur_id = utilisateur_data['id']
            utilisateur_entry = {'utilisateur_id': utilisateur_id, 'communes': []}

            # Agrégations par commune
            communes = DonneeCollectee.objects.filter(agent=utilisateur_id, **date_filters,is_deleted="False").values('commune').distinct()
            for commune_data in communes:
                commune = commune_data['commune']
                commune_entry = {'commune': commune, 'entreprises': []}

                # Agrégations par entreprise
                entreprises = DonneeCollectee.objects.filter(agent=utilisateur_id, commune=commune, **date_filters).values('entreprise').distinct()
                for entreprise_data in entreprises:
                    entreprise = entreprise_data['entreprise']
                    entreprise_entry = {'entreprise': entreprise, 'etat': {}}

                    # Agrégations par état
                    for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                        etat_aggregations = DonneeCollectee.objects.filter(
                            agent=utilisateur_id, commune=commune, entreprise=entreprise, etat_support=etat_support, **date_filters
                        ).annotate(
                            date=TruncDate('create')
                        ).values('date').annotate(
                            nombre_total=Count('id'),
                            montant_total_tsp=Sum(Cast('TSP', FloatField())),
                            montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                            montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                        )

                        # Calculer les sommes des montants pour chaque état
                        somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in etat_aggregations)
                        somme_montant_total_odp = sum(item['montant_total_odp'] for item in etat_aggregations)
                        somme_montant_total = sum(item['montant_total'] for item in etat_aggregations)

                        entreprise_entry['etat'][etat_support] = {
                            'somme_montant_total_tsp': somme_montant_total_tsp,
                            'somme_montant_total_odp': somme_montant_total_odp,
                            'somme_montant_total': somme_montant_total,
                            'nombre_total': sum(item['nombre_total'] for item in etat_aggregations),
                        }

                    commune_entry['entreprises'].append(entreprise_entry)

                utilisateur_entry['communes'].append(commune_entry)

            utilisateurs_aggregations.append(utilisateur_entry)

        return Response(utilisateurs_aggregations, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.db.models import FloatField
from django.db.models.functions import Cast
from .models import DonneeCollectee
from datetime import datetime

class DeleData(APIView):
    def get(self, request, start_date=None, end_date=None):
        try:
            # Convertir les dates en objets date si elles sont fournies
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            # Définir les filtres de date en fonction des paramètres fournis
            date_filters = {}
            if start_date:
                date_filters['create__date__gte'] = start_date
            if end_date:
                date_filters['create__date__lte'] = end_date

            # Supprimer les enregistrements correspondant aux filtres
            deleted_count, _ = DonneeCollectee.objects.filter(**date_filters).delete()

            return Response({'deleted_count': deleted_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
