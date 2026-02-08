import pandas as pd

# ===== FONCTION 1 : CHARGEMENT DES DONNÉES =====
def load_data(filename):
    """
    Charge les données depuis un fichier CSV et convertit la colonne 'date' en datetime.

    Paramètres :
        filename (str) : Chemin du fichier CSV
    
    Retourne :
        DataFrame : Tableau avec colonnes 'date', 'temp_max', 'temp_min', 'temp_mean'
    """
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    return df


# ===== FONCTION 2 : CALCUL DES MOYENNES PAR MOIS =====
def calculate_monthly_averages(df):
    """
    Calcule la température moyenne par mois.

    Paramètres :
        df (DataFrame) : Données météo journalières
    
    Retourne :
        Series : Moyenne de temp_mean pour chaque mois
    """
    df_copy = df.copy()  # On ne modifie pas le dataframe original
    df_copy['mois'] = df_copy['date'].dt.month
    monthly_avg = df_copy.groupby('mois')['temp_mean'].mean()
    return monthly_avg


# ===== FONCTION 3 : VERIFICATION QUALITÉ DES DONNÉES =====
def checking_quality(df):
    """
    Vérifie la qualité des données :
    - valeurs manquantes
    - doublons
    - période couverte
    - cohérence des températures
    """
    print("\n===== RAPPORT QUALITÉ DES DONNÉES =====")

    # Informations générales
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


# ===== PROGRAMME PRINCIPAL =====
if __name__ == "__main__":
    # Charger les données
    df = load_data("data/paris_meteo_2024.csv")
    print("Données chargées :")
    print(df.head())

    # Vérifier la qualité des données
    checking_quality(df)

    # Calculer les moyennes par mois
    monthly = calculate_monthly_averages(df)
    print("\nMoyennes par mois :")
    print(monthly)

