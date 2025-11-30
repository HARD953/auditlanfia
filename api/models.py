# api/models.py
from django.dispatch import receiver
from django.db import models
from custumer.models import CustomUser
from django.db.models.signals import pre_save
from django.utils import timezone

class SupportPublicitaire(models.Model):
    entreprise = models.CharField(max_length=50, blank=True)
    type_support = models.CharField(max_length=50)
    nombre_face = models.FloatField(blank=True)
    surface= models.FloatField(blank=True)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.type_support
    
class Taux(models.Model):
    TTAP = models.CharField(max_length=50)
    TTPAT= models.CharField(max_length=50)
    TAE = models.CharField(max_length=50)
    TAEAT = models.CharField(max_length=50) 
    def __str__(self):
        return f"Donnée #{self.TTAP}_{self.TTPAT}_{self.TAE}_{self.TAEAT}"
    
class Marque(models.Model):
    entreprise = models.CharField(max_length=50, blank=True)
    marque = models.CharField(max_length=50)
    surface = models.CharField(max_length=50, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.marque
    
class Canal(models.Model):
    canal = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.canal
    
class Site(models.Model):
    site = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.site
    
class Etat(models.Model):
    etat = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.etat
    
class Visibilite(models.Model):
    visibilite = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.visibilite

class District(models.Model):
    district = models.CharField(max_length=50,default="Abidjan")
    tauxODP = models.CharField(max_length=50,default="6")
    tauxTSP=models.CharField(max_length=50,default="7")
    tauxAP = models.CharField(max_length=50)
    tauxAPA= models.CharField(max_length=50)
    tauxAPT = models.CharField(max_length=50)
    tauxAE = models.CharField(max_length=50)
    tauxAEA = models.CharField(max_length=50)
    tauxAET = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.district

class Region(models.Model):
    district = models.CharField(max_length=50,default="Abidjan")
    region = models.CharField(max_length=50,default="Abidjan")
    tauxODP = models.CharField(max_length=50,default="6")
    tauxTSP=models.CharField(max_length=50,default="7")
    tauxAP = models.CharField(max_length=50)
    tauxAPA= models.CharField(max_length=50)
    tauxAPT = models.CharField(max_length=50)
    tauxAE = models.CharField(max_length=50)
    tauxAEA = models.CharField(max_length=50)
    tauxAET = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.region

class Ville(models.Model):
    ville = models.CharField(max_length=50,default="Abidjan")
    tauxODP = models.CharField(max_length=50,default="6")
    tauxTSP=models.CharField(max_length=50,default="7")
    tauxAP = models.CharField(max_length=50)
    tauxAPA= models.CharField(max_length=50)
    tauxAPT = models.CharField(max_length=50)
    tauxAE = models.CharField(max_length=50)
    tauxAEA = models.CharField(max_length=50)
    tauxAET = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.ville

class Commune(models.Model):
    district = models.CharField(max_length=50,default="Abidjan")
    region = models.CharField(max_length=50,default="Abidjan")
    ville = models.CharField(max_length=50,default="Abidjan")
    commune = models.CharField(max_length=50,default="Abidjan")
    tauxODP = models.CharField(max_length=50,default="6")
    tauxTSP=models.CharField(max_length=50,default="7")
    tauxAP = models.CharField(max_length=50)
    tauxAPA= models.CharField(max_length=50)
    tauxAPT = models.CharField(max_length=50)
    tauxAE = models.CharField(max_length=50)
    tauxAEA = models.CharField(max_length=50)
    tauxAET = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.commune

class Village(models.Model):
    commune = models.CharField(max_length=50,default="Abidjan")
    village = models.CharField(max_length=50,default="Abidjan")
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.quartier

class Quartier(models.Model):
    commune = models.CharField(max_length=50,default="Abidjan")
    village = models.CharField(max_length=50,default="Abidjan")
    quartier= models.CharField(max_length=50,default="Rue 12")
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.quartier

class Affectation(models.Model):
    agent=models.CharField(max_length=100,blank=False,default='issa')
    commune = models.CharField(max_length=50,default="Abidjan")
    entreprise=models.CharField(max_length=50,default="Rue 12")
    create=models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    def __str__(self):
        return f"Agent {self.agent} est Affecté pour la collecte des supports de {self.entreprise} dans la commune de {self.commune}"

# class Entreprise(models.Model):
#     agent=models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=1)
#     nom = models.CharField(max_length=50,default="Orange")
#     emplacement = models.CharField(max_length=50,default="6")

from django.db import models

class DonneeCollectee(models.Model):
    agent = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    entreprise = models.CharField(max_length=50, blank=True)
    Marque = models.CharField(max_length=50, blank=True)
    ville = models.CharField(max_length=50, blank=True, default="Abidjan")
    commune = models.CharField(max_length=50, blank=True, default="Abidjan")
    region = models.CharField(max_length=50, blank=True, default="Abidjan")
    district = models.CharField(max_length=50, blank=True, default="Abidjan")
    village = models.CharField(max_length=50, blank=True, default="Abidjan")
    quartier = models.CharField(max_length=50, blank=True)
    nomsite = models.CharField(max_length=50, blank=True)
    type_support = models.CharField(max_length=50, blank=True)
    surface = models.FloatField(blank=True, null=True)
    nombre_support = models.FloatField(blank=True, null=True)
    nombre_face = models.FloatField(blank=True, null=True)
    surfaceODP = models.FloatField(blank=True, null=True)
    canal = models.CharField(max_length=50, blank=True)
    etat_support = models.CharField(max_length=50, blank=True)
    typesite = models.CharField(max_length=50, blank=True)
    visibilite = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=50, blank=True)
    observation = models.CharField(max_length=50, blank=True)
    date_collecte = models.DateTimeField(auto_now_add=True, blank=True)
    image_support_1 = models.ImageField(upload_to='collecte_images/', null=True, blank=True)
    image_support_2 = models.ImageField(upload_to='collecte_images/', null=True, blank=True)
    signature = models.ImageField(upload_to='collecte_images/', null=True, blank=True)
    signature1 = models.ImageField(upload_to='collecte_images/', null=True, blank=True)
    Rnom = models.CharField(max_length=50, blank=True)
    Rprenom = models.CharField(max_length=50, blank=True)
    Rcontact = models.CharField(max_length=50, blank=True)
    Snom = models.CharField(max_length=50, blank=True)
    Sprenom = models.CharField(max_length=50, blank=True)
    Scontact = models.CharField(max_length=50, blank=True)
    duree = models.CharField(max_length=50, blank=True)
    anciennete = models.BooleanField(default=False, blank=True)
    TSP = models.CharField(max_length=50, default="12", blank=True)
    ODP = models.BooleanField(default=False, blank=True)
    AP = models.BooleanField(default=False, blank=True)
    APA = models.BooleanField(default=False, blank=True)
    APT = models.BooleanField(default=False, blank=True)
    AE = models.BooleanField(default=False, blank=True)
    AEA = models.BooleanField(default=False, blank=True)
    AET = models.BooleanField(default=False, blank=True)
    tauxCommune = models.BooleanField(default=False, blank=True)
    tauxRegion = models.BooleanField(default=False, blank=True)
    tauxDistrict = models.BooleanField(default=False, blank=True)
    ODP_value = models.CharField(max_length=50, default="1", blank=True)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.surface:
            # Si la surface est vide, récupérer la surface à partir du SupportPublicitaire
            try:
                support = SupportPublicitaire.objects.get(type_support=self.type_support)
                self.surface = support.surface
                self.nombre_face = support.nombre_face
            except SupportPublicitaire.DoesNotExist:
                self.surface = 0
                self.nombre_face = 1  # Valeur par défaut pour éviter des erreurs de multiplication

        # Calculer TSP et ODP_value
        tauxODP1, tauxAP1, tauxAPA1, tauxAPT1, tauxAE1, tauxAEA1, tauxAET1 = [0] * 7

        if self.tauxCommune:
            commune = Commune.objects.get(commune=self.commune)
            tauxODP1, tauxAP1, tauxAPA1, tauxAPT1, tauxAE1, tauxAEA1, tauxAET1 = (
                commune.tauxODP,
                commune.tauxAP,
                commune.tauxAPA,
                commune.tauxAPT,
                commune.tauxAE,
                commune.tauxAEA,
                commune.tauxAET,
            )
        elif self.tauxRegion:
            region = Region.objects.get(region=self.region)
            tauxODP1, tauxAP1, tauxAPA1, tauxAPT1, tauxAE1, tauxAEA1, tauxAET1 = (
                region.tauxODP,
                region.tauxAP,
                region.tauxAPA,
                region.tauxAPT,
                region.tauxAE,
                region.tauxAEA,
                region.tauxAET,
            )
        elif self.tauxDistrict:
            district = District.objects.get(district=self.district)
            tauxODP1, tauxAP1, tauxAPA1, tauxAPT1, tauxAE1, tauxAEA1, tauxAET1 = (
                district.tauxODP,
                district.tauxAP,
                district.tauxAPA,
                district.tauxAPT,
                district.tauxAE,
                district.tauxAEA,
                district.tauxAET,
            )

        # Initialiser les valeurs pour TSP et ODP_value
        duree_value = 0
        nombre_face_value = self.nombre_face if self.nombre_face else 1  # Valeur par défaut

        try:
            duree_value = float(self.duree) if self.duree else 0  # Valeur par défaut
        except ValueError:
            duree_value = 0  # Gérer l'erreur de conversion

        # Calculer TSP
        if self.AP:
            self.TSP = float(self.surface) * duree_value * float(tauxAP1) * nombre_face_value * float(self.nombre_face)
        elif self.APA:
            self.TSP = float(self.surface) * duree_value * float(tauxAPA1) * nombre_face_value * float(self.nombre_face)
        elif self.APT:
            self.TSP = float(self.surface) * duree_value * float(tauxAPT1) * nombre_face_value * float(self.nombre_face)
        elif self.AE:
            self.TSP = float(self.surface) * duree_value * float(tauxAE1) * nombre_face_value * float(self.nombre_face)
        elif self.AEA:
            self.TSP = float(self.surface) * duree_value * float(tauxAEA1) * nombre_face_value * float(self.nombre_face)
        elif self.AET:
            self.TSP = float(self.surface) * duree_value * float(tauxAET1) * nombre_face_value * float(self.nombre_face)
        else:
            self.TSP = float(self.surface) * duree_value  # Valeur par défaut

        # Calculer ODP_value
        if self.ODP:
            try:
                self.ODP_value = float(self.surfaceODP) * duree_value * float(tauxODP1) * float(self.nombre_face)
            except (ValueError, TypeError):
                self.ODP_value = 0  # Gérer les erreurs de conversion
        else:
            self.ODP_value = 0
   
        super(DonneeCollectee, self).save(*args, **kwargs)

    def __str__(self):
        return f"Donnée #{self.id} pour {self.type_support}"

    
