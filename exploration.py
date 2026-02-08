import pandas as pd

def load_data(filename):
    """
    Charge les données depuis un fichier CSV et convertit la colonne 'date' en datetime

    Paramètres :
        filename (str) : Chemin du fichier CSV
    
    Retourne :
        DataFrame : Tableau avec colonnes 'date', 'temp_max', 'temp_min', 'temp_mean'
    """
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])  # Convertir les dates en type datetime
    return df

# ===== FONCTION 2 : CALCUL DES MOYENNES PAR MOIS =====
def calculate_monthly_averages(df):
    """
    Calcule la température moyenne par mois

    Paramètres :
        df (DataFrame) : Données météo journalières
    
    Retourne :
        Series : Moyenne de temp_mean pour chaque mois
    """
    # Extraire le mois de la date
    df['mois'] = df['date'].dt.month

    # Grouper par mois et calculer la moyenne
    monthly_avg = df.groupby('mois')['temp_mean'].mean()
    return monthly_avg

def checking(df):
    df.info()

# ===== PROGRAMME DE TEST =====
if __name__ == "__main__":
    df = load_data("data/paris_meteo_2024.csv")
    print("Données chargées :")
    print(df.head())

    monthly = calculate_monthly_averages(df)
    print("\n Moyennes par mois :")
    print(monthly)

