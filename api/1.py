import pandas as pd
def importer_donnees_de_excel(nom_fichier):
    # Charger le fichier Excel dans un DataFrame pandas
    df = pd.read_excel(nom_fichier)

# Utilisation de la fonction pour importer les données depuis le fichier Excel
nom_fichier_excel = "data.xlsx"
importer_donnees_de_excel(nom_fichier_excel)