import pandas as pd
import os

INPUT_CSV = "data/paris_meteo_2024.csv"

# ===== FONCTION 1 : CHARGEMENT DES DONNÉES =====
def load_data(filename):
    """
    Charge le CSV et convertit la colonne 'date' en datetime
    """
    if not os.path.exists(filename):
        print(f"Erreur : le fichier {filename} n'existe pas !")
        return None
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    return df


# ===== FONCTION 2 : VERIFICATION QUALITÉ DES DONNÉES =====
def checking_quality(df):
    """
    Vérifie la qualité des données :
    - valeurs manquantes
    - doublons
    - période couverte
    - cohérence des températures
    """
    print("\n===== RAPPORT QUALITÉ DES DONNÉES =====")
    df.info()

    # Vérifier les valeurs manquantes
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("Valeurs manquantes : aucune")
    else:
        print("Valeurs manquantes :")
        print(missing[missing > 0])

    # Vérifier les doublons sur la colonne date
    doublons = df.duplicated(subset=['date']).sum()
    print(f"Doublons sur la colonne date : {doublons}")

    # Vérifier la période couverte
    date_min = df['date'].min()
    date_max = df['date'].max()
    print(f"Période : {date_min.date()} -> {date_max.date()}")
    jours_attendus = (date_max - date_min).days + 1
    print(f"Jours présents : {len(df)} / {jours_attendus} attendus")

    # Vérifier la cohérence des températures
    erreurs = df[df['temp_min'] > df['temp_max']]
    if len(erreurs) == 0:
        print("Cohérence temp_min < temp_max : OK")
    else:
        print(f"Cohérence temp_min < temp_max : {len(erreurs)} erreurs")


# ===== FONCTION 3 : STATISTIQUES DESCRIPTIVES SIMPLIFIÉES =====
def show_stats(df):
    """
    Affiche des statistiques simples pour les colonnes principales
    """
    print("\n--- STATISTIQUES DESCRIPTIVES ---")
    colonnes = ['temp_max', 'temp_min', 'temp_mean',
                'precipitation_mm', 'wind_speed_max_kmh', 'humidity_mean_pct']
    colonnes_existantes = [col for col in colonnes if col in df.columns]
    stats = df[colonnes_existantes].describe()
    print(stats.round(1))


# ===== FONCTION 4 : CALCUL DES MOYENNES PAR MOIS =====
def calculate_monthly_averages(df):
    """
    Calcule la température moyenne par mois
    """
    df_copy = df.copy()
    df_copy['mois'] = df_copy['date'].dt.month
    monthly_avg = df_copy.groupby('mois')['temp_mean'].mean()
    return monthly_avg


# ===== FONCTION 5 : NETTOYAGE DES VALEURS MANQUANTES =====
def clean_missing_values(df):
    """
    Nettoie les valeurs manquantes du dataset météo.

    Règles :
    - températures / humidité / vent → interpolation temporelle
    - pluie → 0 mm
    """
    print("\n--- NETTOYAGE DES VALEURS MANQUANTES ---")
    df = df.sort_values("date")  # toujours trier par date

    cols_interpolate = [
        'temp_min',
        'temp_max',
        'temp_mean',
        'humidity_mean_pct',
        'wind_speed_max_kmh'
    ]
    for col in cols_interpolate:
        if col in df.columns:
            before = df[col].isna().sum()
            df[col] = df[col].interpolate(method='linear')
            after = df[col].isna().sum()
            print(f"{col} : {before} → {after} valeurs manquantes")

    if 'precipitation_mm' in df.columns:
        before = df['precipitation_mm'].isna().sum()
        df['precipitation_mm'] = df['precipitation_mm'].fillna(0)
        after = df['precipitation_mm'].isna().sum()
        print(f"precipitation_mm : {before} → {after} valeurs manquantes (remplacées par 0)")

    return df


# ===== PROGRAMME PRINCIPAL =====
if __name__ == "__main__":
    # 1. Charger les données
    df = load_data(INPUT_CSV)
    if df is None:
        exit()  # Arrêter si le fichier n'existe pas

    print("\nDonnées chargées :")
    print(df.head())

    # 2. Vérifier la qualité avant nettoyage
    checking_quality(df)

    # 3. Nettoyer les valeurs manquantes
    df = clean_missing_values(df)

    # 4. Vérifier la qualité après nettoyage
    checking_quality(df)

    # 5. Calculer les moyennes par mois
    monthly = calculate_monthly_averages(df)
    print("\nMoyennes par mois :")
    print(monthly)

    # 6. Statistiques descriptives globales
    show_stats(df)
