import pandas as pd

# 1. Chargement
# On utilise le chemin relatif vers ton dossier data
df = pd.read_csv("data/paris_meteo_2024.csv")

# 2. Formatage
df['date'] = pd.to_datetime(df['date'])

# 3. Vérification (Le réflexe de survie !)
print("--- BILAN DES DONNÉES ---")
print(df.info())

print("\n--- 5 PREMIÈRES LIGNES ---")
print(df.head())