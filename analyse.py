import pandas as pd

# 1. CHARGEMENT (La base)
df = pd.read_csv("data/paris_meteo_2024.csv")
df['date'] = pd.to_datetime(df['date'])

# On ajoute une colonne 'mois' pour l'analyse mensuelle
df['mois'] = df['date'].dt.month

print("="*30)
print("  ANALYSE MÉTÉO PARIS 2024")
print("="*30)

# 2. CALCULS DES RECORDS
# idxmax() nous donne l'index de la ligne où se trouve la valeur max
idx_max = df['temp_max'].idxmax()
date_max = df.loc[idx_max, 'date']
val_max = df.loc[idx_max, 'temp_max']

print(f"\n☀️ Record de chaleur : {val_max}°C le {date_max.strftime('%d/%m/%Y')}")

# 3. CALCULS DES MOYENNES PAR MOIS (Le GroupBy)
# On groupe par mois et on calcule la moyenne de la température
moyennes_mensuelles = df.groupby('mois')['temp_mean'].mean()

print("\n🌡️ Températures moyennes par mois :")
print(moyennes_mensuelles.round(1)) # Ici on arrondit à 1 chiffre après la virgule

# 4. CALCULS DES PRÉCIPITATIONS (Cumul)
pluie_totale = df['precipitation_mm'].sum()
print(f"\n🌧️ Précipitations totales sur l'année : {pluie_totale:.1f} mm")