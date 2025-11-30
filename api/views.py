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

from .importdata import *

# class DonneeCollecteeCreate(generics.CreateAPIView):
#     queryset = DonneeCollectee.objects.all()
#     serializer_class = DonneeCollecteeSerializer1
    
#     permission_classes = [IsAuthenticated]
#     def perform_create(self, serializer):
#         # Associer l'utilisateur connecté comme propriétaire du Bien
#         if self.request.user.is_anonymous:
#             serializer.save()
#             # importer_donnees_de_excel("data.xlsx")
#         else:
#             # importer_donnees_de_excel("data.xlsx")
#             serializer.save(agent=self.request.user)

class DonneeCollecteeCreate(generics.CreateAPIView):
    queryset = DonneeCollectee.objects.all()
    serializer_class = DonneeCollecteeSerializer1
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        agent_name = self.request.user.last_name  # Nom de l'agent connecté, à adapter selon votre modèle utilisateur

        # Récupérer l'affectation active de l'agent connecté
        try:
            affectation = Affectation.objects.get(agent=agent_name, status=True)  # 'status=True' pour affectation active
        except Affectation.DoesNotExist:
            return Response({"error": "Affectation not found for the agent."}, status=404)

        # Récupérer la commune, le district et la région associés à l'agent
        commune = affectation.commune
        entreprise=affectation.entreprise
        try:
            district = Commune.objects.get(commune=commune).district
            region = Commune.objects.get(commune=commune).region
        except (District.DoesNotExist, Region.DoesNotExist):
            return Response({"error": "District or Region not found for the specified commune."}, status=404)

        # Afficher les données validées pour le débogage (optionnel)
        print(serializer.validated_data)

        # Sauvegarder l'objet DonneeCollectee avec l'agent, la commune, le district et la région
        serializer.save(
            agent=self.request.user,
            entreprise=entreprise,
            commune=commune,
            district=district,
            region=region
        )


class DonneeCollecteeListAgent(generics.ListAPIView):
    
    serializer_class = DonneeCollecteeSerializer # Assurez-vous que l'utilisateur est authentifié
    
    def get_queryset(self):
        # Filtrer les objets DonneeCollectee pour l'utilisateur connecté et l'entreprise associée
        user = self.request.user
        current_date = datetime.now().date()
        return DonneeCollectee.objects.filter(agent=user,is_deleted="False")
    
class DonneeCollecteeDetailView1(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DonneeCollecteeSerializer
    def get_queryset(self):
        return DonneeCollectee.objects.all()
        
class DonneeCollecteeListAll(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = DonneeCollecteeSerializer# Assurez-vous que l'utilisateur est authentifié
    def get_queryset(self):
        # Filtrer les objets DonneeCollectee pour l'utilisateur connecté et l'entreprise associée
        user = self.request.user
        return DonneeCollectee.objects.filter(agent=user,is_deleted="False")

class Allcollecte(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = DonneeCollecteeSerializer# Assurez-vous que l'utilisateur est authentifié
    def get_queryset(self):
        # Filtrer les objets DonneeCollectee pour l'utilisateur connecté et l'entreprise associée
        user = self.request.user
        return DonneeCollectee.objects.filter(agent=user,is_deleted="False")

           
# class DonneeCollecteeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = DonneeCollecteeSerializer
#     def get_queryset(self):
#         return DonneeCollectee.objects.all()
        
class NombreSupportsParAgent(APIView):
    def get(self, request):
        # Vérifiez si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtenez le nombre de supports collectés par agent
        supports_par_agent = DonneeCollectee.objects.filter(agent=request.user).values('agent').annotate(nombre_supports=Count('id'))

        # supports_par_agent est maintenant une liste de dictionnaires avec 'agent' et 'nombre_supports'
        for entry in supports_par_agent:
            agent = entry['agent']
            nombre_supports = entry['nombre_supports']
            return Response({'agent': agent, 'nombre_supports': nombre_supports}, status=status.HTTP_200_OK)
        

class DonneeCollecteeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DonneeCollectee.objects.filter(is_deleted=False)
    serializer_class = DonneeCollecteeSerializer
    # permission_classes = [permissions.DjangoModelPermissions]
    
    def update(self, request, *args, **kwargs):
        # Utiliser partial=True pour les mises à jour partielles
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class SupportPublicitaireListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia] 
    queryset = SupportPublicitaire.objects.all()
    serializer_class = SupportPublicitaireSerializer

class SupportPublicitaireDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia] 
    queryset = SupportPublicitaire.objects.all()
    serializer_class = SupportPublicitaireSerializer

class MarqueListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer

class MarqueListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer

class VisibiliteListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Visibilite.objects.all()
    serializer_class = VisibiliteSerializer

class VisibiliteListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Visibilite.objects.all()
    serializer_class = VisibiliteSerializer

class EtatListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Etat.objects.all()
    serializer_class = EtatSerializer

class EtatListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Etat.objects.all()
    serializer_class = EtatSerializer

class CanalListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer

class CanalListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer

class SiteListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class SiteListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class CommuneL(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializers

class CommuneDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializers

class CommuneApp(generics.ListAPIView):
    # permission_classes = [IsLanfia]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializersApp


class DistrictApp(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictAppFiltre(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = District.objects.all()
    serializer_class = DistrictSerializerFiltre

class RegionApp(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionAppFiltre(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Region.objects.all()
    serializer_class = RegionSerializerFiltre

class AffectationApp(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Affectation.objects.all()
    serializer_class = AffectationSerializer

class DistrictAppDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictAppFiltreDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = District.objects.all()
    serializer_class = DistrictSerializerFiltre

class RegionAppDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionAppFiltreDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Region.objects.all()
    serializer_class = RegionSerializerFiltre

class VillageAppFiltreDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Village.objects.all()
    serializer_class = VillageSerializerFiltre

class VillageAppFiltre(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class VillageApp(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Village.objects.all()
    serializer_class = VillageSerializer

class AffectationAppDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Affectation.objects.all()
    serializer_class = AffectationSerializer

# from django.db.models import Q

# class DonneeCollecteeList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DonneeCollecteeSerializer

#     def get_queryset(self):
#         user = self.request.user
#         # Récupérer les paramètres de date de début et de fin depuis les paramètres d'URL
#         start_date_str = self.kwargs.get('start_date')
#         end_date_str = self.kwargs.get('end_date')

#         # Convertir les chaînes de date en objets datetime.date si elles sont fournies
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
#         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

#         # Récupérer le queryset de tous les objets DonneeCollectee
#         queryset = DonneeCollectee.objects.filter(is_deleted="False")

#         # Filtrer le queryset en fonction des dates fournies
#         if start_date and end_date:
#             queryset = queryset.filter(create__date__range=(start_date, end_date))
#         elif start_date:
#             queryset = queryset.filter(create__date__gte=start_date)
#         elif end_date:
#             queryset = queryset.filter(create__date__lte=end_date)
        
#         # Créer un dictionnaire de filtres pour les autres champs
#         filters_dict = {
#             'entreprise': 'MTN CI',
#             'Marque': 'MTN CI',
#             'commune': 'cocody',
#             'quartier': '',
#             'type_support': 'Affiche',
#             'canal': 'franchise',
#             'etat_support': 'Bon',
#             'typesite': '',
#             'visibilite': 'Bonne',
#             'duree': '12',
#             'surface': '4'
#         }

#         # Créer un dictionnaire de correspondance entre les noms de champ dans le modèle DonneeCollectee
#         # et les noms de champ attendus dans le dictionnaire de filtres
#         field_mapping = {
#             'entreprise': 'entreprise',
#             'Marque': 'Marque',
#             'commune': 'commune',
#             'quartier': 'quartier',
#             'type_support': 'type_support',
#             'canal': 'canal',
#             'etat_support': 'etat_support',
#             'typesite': 'typesite',
#             'visibilite': 'visibilite',
#             'anciennete': 'anciennete',
#             'duree': 'duree',
#             'surface': 'surface'
#         }
#         # Appliquer les filtres dynamiquement en parcourant le dictionnaire de filtres
#         for key, value in filters_dict.items():
#             if key in field_mapping:
#                 field_name = field_mapping[key]
#                 # Construire le filtre pour ce champ spécifique avec icontains
#                 queryset = queryset.filter(**{f'{field_name}__icontains': value})
#         if user.is_agent:
#             return queryset
#         else:
#             return queryset.filter(entreprise=user.entreprise)
        

# from rest_framework import generics
# from .models import DonneeCollectee
# from .serializers import DonneeCollecteeSerializer
# from django.http import JsonResponse

# class DonneeCollecteeList(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DonneeCollecteeSerializer

#     def post(self, request, *args, **kwargs):
#         user = request.user
#         queryset = DonneeCollectee.objects.filter(is_deleted="False")

#         # Récupérer les données POST envoyées avec la requête
#         filters_dict = request.data

#         # Récupérer les paramètres de date de début et de fin
#         start_date_str = filters_dict.get('start_date')
#         end_date_str = filters_dict.get('end_date')

#         # Convertir les chaînes de date en objets datetime.date si elles sont fournies
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
#         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

#         # Filtrer le queryset en fonction des dates fournies
#         if start_date and end_date:
#             queryset = queryset.filter(create__date__range=(start_date, end_date))
#         elif start_date:
#             queryset = queryset.filter(create__date__gte=start_date)
#         elif end_date:
#             queryset = queryset.filter(create__date__lte=end_date)

#         # Créer un dictionnaire de correspondance entre les noms de champ dans le modèle DonneeCollectee
#         # et les noms de champ attendus dans le dictionnaire de filtres
        
#         field_mapping = {
#             'entreprise': 'entreprise',
#             'Marque': 'Marque',
#             'commune': 'commune',
#             'ville': 'ville',
#             'quartier': 'quartier',
#             'type_support': 'type_support',
#             'canal': 'canal',
#             'etat_support': 'etat_support',
#             'typesite': 'typesite',
#             'visibilite': 'visibilite',
#             'anciennete': 'anciennete',
#             'duree': 'duree',
#             'surface': 'surface'
#         }

#         # Appliquer les filtres dynamiques en parcourant le dictionnaire de filtres
#         for key, value in filters_dict.items():
#             if key in field_mapping and key not in ['start_date', 'end_date']:
#                 field_name = field_mapping[key]
#                 # Construire le filtre pour ce champ spécifique avec icontains
#                 queryset = queryset.filter(**{f'{field_name}__icontains': value})

#         # Appliquer le filtre supplémentaire pour l'utilisateur non-agent
#         if not user.is_agent:
#             queryset = queryset.filter(entreprise=user.entreprise)

#         # Sérialiser le queryset filtré
#         serializer = self.serializer_class(queryset, many=True)
#         return JsonResponse(serializer.data, safe=False)


from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import DonneeCollectee
from .serializers import DonneeCollecteeSerializer
from datetime import datetime

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 200

class DonneeCollecteeList(generics.GenericAPIView):
    serializer_class = DonneeCollecteeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Start with the base queryset
        queryset = DonneeCollectee.objects.all()

        # Get filters from the request body (only for POST requests)
        filters_dict = self.request.data

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

        return queryset

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Pagination of the results
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize the paginated queryset
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Quartier, Affectation, SupportPublicitaire, Marque

class QuartiersByCommuneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer l'utilisateur connecté (l'agent)
        agent_name = request.user.last_name  # Vous pouvez adapter cela selon votre logique d'authentification

        # Trouver l'affectation de l'agent connecté
        try:
            affectation = Affectation.objects.get(agent=agent_name, status=True)  # 'status=True' pour l'affectation active
        except Affectation.DoesNotExist:
            return Response({"error": "Affectation not found for the agent."}, status=404)

        # Récupérer la commune et l'entreprise à partir de l'affectation

        commune = affectation.commune
        
        entreprise = affectation.entreprise

        # Filtrer les quartiers en fonction de la commune de l'agent
        quartiers = Quartier.objects.filter(commune=commune)
        village = Village.objects.filter(village=village)

        # Récupérer les supports publicitaires et les marques en fonction de l'entreprise
        supports = SupportPublicitaire.objects.filter(entreprise=entreprise)
        marques = Marque.objects.filter(entreprise=entreprise)

        # Créer une liste des noms de quartiers
        quartiers_list = quartiers.values_list('quartier', flat=True)

        # Créer une liste des types de supports publicitaires
        supports_list = supports.values('type_support')

        # Créer une liste des marques
        marques_list = marques.values('marque')

        # Retourner la réponse avec la commune, l'entreprise, la liste des quartiers, les supports et les marques
        return Response({
            "commune": commune,
            "village": village,
            "entreprise": entreprise,
            "quartiers": list(quartiers_list),
            "type_supports": list(supports_list),
            "marques": list(marques_list)
        }, status=200)

