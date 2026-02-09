import pandas as pd

# ===== CONFIGURATION =====
INPUT_CSV = "data/paris_meteo_2024.csv"  # chemin vers ton fichier CSV

# ===== FONCTION 1 : Déterminer la saison à partir du mois =====
def get_saison(mois):
    """
    Retourne la saison correspondant au mois.
    """
    if mois in [12, 1, 2]:
        return "Hiver"
    elif mois in [3, 4, 5]:
        return "Printemps"
    elif mois in [6, 7, 8]:
        return "Ete"
    else:
        return "Automne"

# ===== FONCTION 2 : Ajouter la colonne saison au dataframe =====
def add_saison_column(df):
    """
    Ajoute une colonne 'saison' au dataframe en fonction de la colonne 'mois'.
    """
    df['saison'] = df['mois'].apply(get_saison)
    return df

# ===== FONCTION 3 : Calculer les moyennes pour une saison =====
def moyenne_saison(df, saison):
    """
    Calcule les moyennes de température et la somme des précipitations pour une saison.
    """
    df_s = df[df['saison'] == saison]  # Filtrer les lignes de cette saison
    temp_max_moy = df_s['temp_max'].mean()
    temp_min_moy = df_s['temp_min'].mean()
    temp_mean_moy = df_s['temp_mean'].mean()
    
    # Précipitation si la colonne existe
    if 'precipitation_mm' in df.columns:
        precip_total = df_s['precipitation_mm'].sum()
        return temp_max_moy, temp_min_moy, temp_mean_moy, precip_total
    else:
        return temp_max_moy, temp_min_moy, temp_mean_moy, None

# ===== FONCTION 4 : Afficher les moyennes par saison =====
def analyze_seasonal(df):
    """
    Boucle sur les saisons et affiche les moyennes de chaque saison.
    """
    saisons = ['Hiver', 'Printemps', 'Ete', 'Automne']
    
    # Ajouter la colonne saison
    df = add_saison_column(df)
    
    print("\n--- MOYENNES PAR SAISON ---")
    
    for s in saisons:
        temp_max, temp_min, temp_mean, precip = moyenne_saison(df, s)
        if precip is not None:
            print(f"{s} : max={temp_max:.1f}, min={temp_min:.1f}, mean={temp_mean:.1f}, pluie={precip:.1f}")
        else:
            print(f"{s} : max={temp_max:.1f}, min={temp_min:.1f}, mean={temp_mean:.1f}")

# ===== FONCTION 5 : Détecter les jours extrêmes =====
def detect_extremes(df):
    """
    Détecte les jours de canicule et de gel.
    """
    print("\n--- JOURS EXTREMES ---")

    # Canicule : temp_max > 30
    canicule = df[df['temp_max'] > 30]
    print(f"\nJours > 30°C : {len(canicule)}")
    if len(canicule) > 0:
        print(canicule[['date', 'temp_max', 'temp_min']].to_string(index=False))

    # Gel : temp_min < 0
    gel = df[df['temp_min'] < 0]
    print(f"\nJours < 0°C : {len(gel)}")
    if len(gel) > 0:
        print(gel[['date', 'temp_max', 'temp_min']].to_string(index=False))

# ===== FONCTION 6 : Statistiques descriptives simples =====
def show_stats(df):
    """
    Affiche statistiques simples : count, mean, std, min, quartiles, max
    """
    print("\n--- STATISTIQUES DESCRIPTIVES ---")
    colonnes = ['temp_max', 'temp_min', 'temp_mean',
                'precipitation_mm', 'wind_speed_max_kmh', 'humidity_mean_pct']

    # On garde seulement les colonnes existantes pour éviter les erreurs
    colonnes_existantes = [col for col in colonnes if col in df.columns]
    stats = df[colonnes_existantes].describe().round(1)
    print(stats)

# ===== FONCTION 7 : Corrélations =====
def show_correlations(df):
    """
    Calcule les corrélations entre les colonnes principales.
    """
    print("\n--- CORRELATIONS ---")
    colonnes = ['temp_max', 'temp_min', 'temp_mean',
                'precipitation_mm', 'wind_speed_max_kmh', 'humidity_mean_pct']
    colonnes_existantes = [col for col in colonnes if col in df.columns]

    corr = df[colonnes_existantes].corr().round(2)
    print(corr)

# ===== FONCTION 8 : Charger les données =====
def load_data(filename):
    """
    Charge les données depuis le CSV et convertit la colonne 'date' en datetime.
    """
     # Vérifier si le fichier existe
    if not os.path.exists(filename):
        print(f"Erreur : le fichier {filename} n'existe pas !")
        return None
    
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    # Extraire le mois pour les analyses saisonnières
    df['mois'] = df['date'].dt.month
    return df

# ===== PROGRAMME PRINCIPAL =====
def main():
    print("=" * 50)
    print("ANALYSES - METEO PARIS 2024")
    print("=" * 50)

    # 1. Charger les données
    df = load_data(INPUT_CSV)
    if df is None:
        return  # Arrêter si le chargement a échoué
    print(f"\n{len(df)} jours chargés")

    # 2. Statistiques descriptives
    show_stats(df)

    # 3. Moyennes par saison
    analyze_seasonal(df)

    # 4. Jours extrêmes
    detect_extremes(df)

    # 5. Corrélations
    show_correlations(df)

    print("\n" + "=" * 50)
    print("ANALYSES TERMINEES")
    print("=" * 50)

# ===== EXECUTION =====
if __name__ == "__main__":
    main()
