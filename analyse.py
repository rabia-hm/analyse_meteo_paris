"""
Projet Météo Paris 2024
Script d'analyse simple :
- Moyennes par saison
- Détection des jours extrêmes
- Corrélations entre variables
"""

import pandas as pd

# ===== CONFIGURATION =====
INPUT_CSV = "data/paris_meteo_2024.csv"

# Définition des saisons et leurs mois avec un dictionnaire globale
SAISONS = {
    'Hiver': [12, 1, 2],
    'Printemps': [3, 4, 5],
    'Ete': [6, 7, 8],
    'Automne': [9, 10, 11],
}


# ===== FONCTION 1 : Charger et préparer les données =====
def load_data(filepath):
    """
    Charge le CSV et crée la colonne 'mois'.
    """
    df = pd.read_csv(filepath, parse_dates=['date'])  # lit CSV et transforme date
    df['mois'] = df['date'].dt.month                 # ajoute le mois
    return df


# ===== FONCTION 2 : Déterminer la saison =====
#.items() → pour parcourir un dictionnaire et récupérer clé et valeur en même temps
def get_saison(mois):
    """
    Retourne la saison correspondant au mois.
    """
    for saison, mois_list in SAISONS.items():
        if mois in mois_list:
            return saison
    return "Inconnu"