from rest_framework import serializers
from .models import *

class EntrepriseSerializers(serializers.ModelSerializer):
    class Meta:
        model = DonneeCollectee
        fields = ["entreprise"]

class CommuneSerializersApp(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ["commune"]

class SupportPublicitaireSerializerF(serializers.ModelSerializer):
    class Meta:
        model = SupportPublicitaire
        fields = ['type_support']

class VisibiliteSerializerF(serializers.ModelSerializer):
    class Meta:
        model = Visibilite
        fields = ['visibilite']
class MarqueSerializerF(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = ['marque']
        
class SiteSerializerF(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['site']
class CanalSerializerF(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = ['canal']

class EtatSerializerF(serializers.ModelSerializer):
    class Meta:
        model = Etat
        fields = ['etat']

class FiltreQuartier(serializers.ModelSerializer):
    class Meta:
        model = DonneeCollectee
        fields = ['quartier']