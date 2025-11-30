from rest_framework import serializers
from .models import *

class DonneeCollecteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonneeCollectee
        fields = '__all__'

class DonneeCollecteeSerializer1(serializers.ModelSerializer):
    class Meta:
        model = DonneeCollectee
        fields = '__all__'
        read_only_fields = ('id', 'create', 'updated_at', 'TSP', 'ODP_value')

    def create(self, validated_data):
        # Supprimez les champs en lecture seule pour éviter les erreurs
        validated_data.pop('TSP', None)
        validated_data.pop('ODP_value', None)
        
        # Appelez la méthode create de DonneeCollectee avec les données validées
        instance = DonneeCollectee(**validated_data)
        instance.save()  # Cela appellera votre méthode save() personnalisée
        return instance

class EntrepriseSerializers(serializers.ModelSerializer):
    class Meta:
        model = DonneeCollectee
        fields = ["entreprise"]

class CommuneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class VilleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = '__all__'

class CommuneSerializersApp(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ["commune"]

class QuartierSerialiser1(serializers.ModelSerializer):
    class Meta:
        model = Quartier
        fields = '__all__'

class QuartierSerialiser2(serializers.ModelSerializer):
    class Meta:
        model = Quartier
        fields = ["quartier"]
        

# class TauxODPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DonneeCollectee
#         fields = ["tauxODP"]

# class TauxTSPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DonneeCollectee
#         fields = ["tauxTSP"]

class SupportPublicitaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportPublicitaire
        fields = '__all__'

class VisibiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visibilite
        fields = '__all__'
class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = '__all__'
class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'
class CanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = '__all__'

class EtatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etat
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class DistrictSerializerFiltre(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["district"]

class RegionSerializerFiltre(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["region"]

class AffectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affectation
        fields = '__all__'

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'

class VillageSerializerFiltre(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ["village"]