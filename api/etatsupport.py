from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DonneeCollectee
from datetime import datetime

class StatByEtat(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user

        # Filtrer les objets DonneeCollectee pour l'agent connecté
        queryset = DonneeCollectee.objects.filter(agent=user)

        # Filtrer par date de collecte actuelle
        current_date = datetime.now().date()
        queryset = queryset.filter(create__date=current_date)

        # Calculer le nombre de supports dans chaque état
        nombre_support_total = queryset.count()
        nombre_support_bon = queryset.filter(etat_support='Bon').count()
        nombre_support_deteriore = queryset.filter(etat_support='Détérioré').count()
        nombre_support_defraichis = queryset.filter(etat_support='Défraichis').count()

        # Retourner les nombres de supports dans chaque état sous forme de dictionnaire
        return {
            'nombre_support_total': nombre_support_total,
            'nombre_support_bon': nombre_support_bon,
            'nombre_support_deteriore': nombre_support_deteriore,
            'nombre_support_defraichis': nombre_support_defraichis
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)


class StatByEtatAll(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user

        # Filtrer les objets DonneeCollectee pour l'agent connecté
        queryset = DonneeCollectee.objects.filter(agent=user)

        # Filtrer par date de collecte actuelle

        # Calculer le nombre de supports dans chaque état
        nombre_support_total = queryset.count()
        nombre_support_bon = queryset.filter(etat_support='Bon').count()
        nombre_support_deteriore = queryset.filter(etat_support='Détérioré').count()
        nombre_support_defraichis = queryset.filter(etat_support='Défraichis').count()

        # Retourner les nombres de supports dans chaque état sous forme de dictionnaire
        return {
            'nombre_support_total': nombre_support_total,
            'nombre_support_bon': nombre_support_bon,
            'nombre_support_deteriore': nombre_support_deteriore,
            'nombre_support_defraichis': nombre_support_defraichis
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)