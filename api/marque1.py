from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.db.models import FloatField
from django.db.models.functions import Cast
from .models import DonneeCollectee
from datetime import datetime

class GTotalCollectedDataViewM(APIView):
    def get(self, request, start_date=None, end_date=None):
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

        # Agrégations par entreprise
        entreprises_aggregations = []

        if self.request.user.is_agent:
            entreprises = DonneeCollectee.objects.filter(**date_filters).values('entreprise').distinct()
            for entreprise_data in entreprises:
                entreprise = entreprise_data['entreprise']
                entreprise_entry = {'entreprise': entreprise, 'communes': []}

                # Agrégations par commune
                communes = DonneeCollectee.objects.filter(entreprise=entreprise, **date_filters).values('commune').distinct()
                for commune_data in communes:
                    commune = commune_data['commune']
                    commune_entry = {'commune': commune, 'marques': []}

                    # Agrégations par marque
                    marques = DonneeCollectee.objects.filter(entreprise=entreprise, commune=commune, **date_filters).values('Marque').distinct()
                    for marque_data in marques:
                        marque = marque_data['Marque']
                        marque_entry = {'marque': marque, 'etat': {}}

                        # Agrégations par état
                        for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                            etat_aggregations = DonneeCollectee.objects.filter(
                                entreprise=entreprise, commune=commune, Marque=marque, etat_support=etat_support, **date_filters
                            ).aggregate(
                                somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                                somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                                somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                                nombre_total=Count('id'),
                            )

                            marque_entry['etat'][etat_support] = {
                                'somme_montant_total_tsp': etat_aggregations['somme_montant_total_tsp'] or 0,
                                'somme_montant_total_odp': etat_aggregations['somme_montant_total_odp'] or 0,
                                'somme_montant_total': etat_aggregations['somme_montant_total'] or 0,
                                'nombre_total': etat_aggregations['nombre_total'] or 0,
                            }

                        commune_entry['marques'].append(marque_entry)

                    entreprise_entry['communes'].append(commune_entry)

                entreprises_aggregations.append(entreprise_entry)

        else:
            entreprises = DonneeCollectee.objects.filter(entreprise=self.request.user.entreprise, **date_filters).values('entreprise').distinct()
            for entreprise_data in entreprises:
                entreprise = entreprise_data['entreprise']
                entreprise_entry = {'entreprise': entreprise, 'communes': []}

                # Agrégations par commune
                communes = DonneeCollectee.objects.filter(entreprise=entreprise, **date_filters).values('commune').distinct()
                for commune_data in communes:
                    commune = commune_data['commune']
                    commune_entry = {'commune': commune, 'marques': []}

                    # Agrégations par marque
                    marques = DonneeCollectee.objects.filter(entreprise=entreprise, commune=commune, **date_filters).values('Marque').distinct()
                    for marque_data in marques:
                        marque = marque_data['Marque']
                        marque_entry = {'marque': marque, 'etat': {}}

                        # Agrégations par état
                        for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                            etat_aggregations = DonneeCollectee.objects.filter(
                                entreprise=entreprise, commune=commune, Marque=marque, etat_support=etat_support, **date_filters
                            ).aggregate(
                                somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                                somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                                somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                                nombre_total=Count('id'),
                            )

                            marque_entry['etat'][etat_support] = {
                                'somme_montant_total_tsp': etat_aggregations['somme_montant_total_tsp'] or 0,
                                'somme_montant_total_odp': etat_aggregations['somme_montant_total_odp'] or 0,
                                'somme_montant_total': etat_aggregations['somme_montant_total'] or 0,
                                'nombre_total': etat_aggregations['nombre_total'] or 0,
                            }

                        commune_entry['marques'].append(marque_entry)

                    entreprise_entry['communes'].append(commune_entry)

                entreprises_aggregations.append(entreprise_entry)

        return Response(entreprises_aggregations, status=status.HTTP_200_OK)