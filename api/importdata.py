import pandas as pd
from .models import DonneeCollectee

def importer_donnees_de_excel(fichier):
    # Charger le fichier Excel dans un DataFrame pandas
    df = pd.read_excel(fichier)

    # Itérer sur les lignes du DataFrame et insérer les données dans la base de données
    for index, row in df.iterrows():
        print(index)
        DonneeCollectee.objects.create(
            agent_id=row['agent'],
            entreprise=row['entreprise'],
            Marque=row['Marque'],
            ville=row['ville'],
            commune=row['commune'],
            quartier=row['quartier'],
            type_support=row['type_support'],
            surface=row['surface'],
            surfaceODP=row['surfaceODP'],
            canal=row['canal'],
            etat_support=row['etat_support'],
            typesite=row['typesite'],
            visibilite=row['visibilite'],
            description=row['description'],
            observation=row['observation'],
            date_collecte=row['date_collecte'],
            duree=row['duree'],
            anciennete=row['anciennete'],
            TSP=row['TSP'],
            ODP=row['ODP'],
            AP=row['AP'],
            APA=row['APA'],
            APT=row['APT'],
            AE=row['AE'],
            AEA=row['AEA'],
            AET=row['AET'],
            ODP_value=row['ODP_value'],
            create=row['create'],  
            updated_at=row['updated_at'], 
            latitude=row['latitude'],
            longitude=row['longitude']
        )

