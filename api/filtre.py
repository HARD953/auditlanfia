from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from custumer.models import*
from custumer.serializers import UserSerializer1
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import *
from datetime import datetime
from .serializers2 import *
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import BasePagination

class NoPagination(BasePagination):
    def paginate_queryset(self, queryset, request, view=None):
        return None

    def get_paginated_response(self, data):
        return data

class SupportPublicitaireListViewF(generics.ListCreateAPIView):
    queryset = SupportPublicitaire.objects.all()
    serializer_class = SupportPublicitaireSerializerF

class MarqueListViewF(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializerF

class VisibiliteListViewF(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Visibilite.objects.all()
    serializer_class = VisibiliteSerializerF

class EtatListViewF(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Etat.objects.all()
    serializer_class = EtatSerializerF

class CanalListViewF(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Canal.objects.all()
    serializer_class = CanalSerializerF

class SiteListViewF(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Site.objects.all()
    serializer_class = SiteSerializerF

class QuartierF(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset =Quartier.objects.all()
    serializer_class = QuartierSerialiser1


class NoPagination(BasePagination):
    def paginate_queryset(self, queryset, request, view=None):
        return None

    def get_paginated_response(self, data):
        return data

class QuartierListe(ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Quartier.objects.all()
    serializer_class = QuartierSerialiser2
    pagination_class = NoPagination  # Utilisez votre pagination personnalisée

class VilleListe(ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Ville.objects.all()
    serializer_class = VilleSerializers
    # pagination_class = NoPagination  # Utilisez votre pagination personnalisée

class VilleListeP(ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Ville.objects.all()
    serializer_class = VilleSerializers
    

class VilleDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset =Ville.objects.all()
    serializer_class = VilleSerializers

class QuartierCommune(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Quartier.objects.all()
    serializer_class = QuartierSerialiser1


class QuartierCommuneDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset =Quartier.objects.all()
    serializer_class = QuartierSerialiser1

class CommuneApp(generics.ListAPIView):
    # permission_classes = [IsLanfia]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializersApp
    pagination_class = NoPagination 

class QuartierListViewF(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    serializer_class = FiltreQuartier

    def get_queryset(self):
        # Récupérer tous les objets DonneeCollectee
        queryset = DonneeCollectee.objects.all()

        # Filtrer les éléments uniques (distincts) par quartier
        unique_quartiers = set()
        filtered_queryset = []
        
        for obj in queryset:
            if obj.quartier not in unique_quartiers:
                unique_quartiers.add(obj.quartier)
                filtered_queryset.append(obj)
        
        return filtered_queryset
    





