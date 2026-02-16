import pandas as pd
import os


INPUT_CSV = "data/paris_meteo_2024.csv" 

# ===== CHARGEMENT DES DONNÉES =====
def load_data(filename):
    if not os.path.exists(filename):
        print(f"Erreur : le fichier {filename} n'existe pas !")
        return None
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    df['mois'] = df['date'].dt.month
    return df

# ===== Déterminer la saison =====
def get_saison(mois):
    if mois in [12, 1, 2]:
        return "Hiver"
    elif mois in [3, 4, 5]:
        return "Printemps"
    elif mois in [6, 7, 8]:
        return "Ete"
    else:
        return "Automne"

def add_saison_column(df):
    df['saison'] = df['mois'].apply(get_saison)
    return df

# ===== Moyennes par saison =====
def moyenne_saison(df, saison):
    df_s = df[df['saison'] == saison]
    temp_max_moy = df_s['temp_max'].mean()
    temp_min_moy = df_s['temp_min'].mean()
    temp_mean_moy = df_s['temp_mean'].mean()
    precip_total = df_s['precipitation_mm'].sum() if 'precipitation_mm' in df.columns else None
    return temp_max_moy, temp_min_moy, temp_mean_moy, precip_total

def analyze_seasonal(df):
    df = add_saison_column(df)
    saisons = ['Hiver', 'Printemps', 'Ete', 'Automne']
    summary_list = []
    print("\n--- MOYENNES PAR SAISON ---")
    for s in saisons:
        temp_max, temp_min, temp_mean, precip = moyenne_saison(df, s)
        summary_list.append({
            'saison': s,
            'temp_max': round(temp_max,1),
            'temp_min': round(temp_min,1),
            'temp_mean': round(temp_mean,1),
            'precipitation_mm': round(precip,1) if precip is not None else None
        })
        if precip is not None:
            print(f"{s} : max={temp_max:.1f}, min={temp_min:.1f}, mean={temp_mean:.1f}, pluie={precip:.1f}")
        else:
            print(f"{s} : max={temp_max:.1f}, min={temp_min:.1f}, mean={temp_mean:.1f}")
    return pd.DataFrame(summary_list)

# ===== Détecter les jours extrêmes =====
def detect_extremes(df):
    extremes = {}
    canicule = df[df['temp_max'] > 30]
    print(f"\nJours > 30°C : {len(canicule)}")
    if len(canicule) > 0:
        print(canicule[['date','temp_max','temp_min']].to_string(index=False))
        extremes['extreme_canicule'] = canicule

    gel = df[df['temp_min'] < 0]
    print(f"\nJours < 0°C : {len(gel)}")
    if len(gel) > 0:
        print(gel[['date','temp_max','temp_min']].to_string(index=False))
        extremes['extreme_gel'] = gel

    return extremes

# ===== Statistiques descriptives =====
def show_stats(df):
    print("\n--- STATISTIQUES DESCRIPTIVES ---")
    colonnes = ['temp_max', 'temp_min', 'temp_mean',
                'precipitation_mm', 'wind_speed_max_kmh', 'humidity_mean_pct']
    colonnes_existantes = [c for c in colonnes if c in df.columns]
    stats = df[colonnes_existantes].describe().round(1)
    print(stats)
    return stats

# ===== Corrélations =====
def show_correlations(df):
    print("\n--- CORRELATIONS ---")
    colonnes = ['temp_max', 'temp_min', 'temp_mean',
                'precipitation_mm', 'wind_speed_max_kmh', 'humidity_mean_pct']
    colonnes_existantes = [c for c in colonnes if c in df.columns]
    corr = df[colonnes_existantes].corr().round(2)
    print(corr)
    return corr

# ===== GENERATION CSV =====
def save_csvs(dataframes_dict):
    os.makedirs("outputs", exist_ok=True)
    for name, df in dataframes_dict.items():
        # certaines DataFrames (corrélation) ont un index à conserver
        if df.index.name or df.index.dtype != 'int64':
            df.to_csv(f"outputs/{name}.csv")
        else:
            df.to_csv(f"outputs/{name}.csv", index=False)
        print(f"CSV généré : outputs/{name}.csv")

# ===== MAIN =====
def main():
    print("=" * 50)
    print("ANALYSES - METEO PARIS 2024")
    print("=" * 50)

    df = load_data(INPUT_CSV)
    if df is None:
        return

    # Analyses
    stats = show_stats(df)
    seasonal_summary = analyze_seasonal(df)
    extremes = detect_extremes(df)
    corr = show_correlations(df)

    # Génération CSV
    dataframes_to_save = {
        "descriptive_stats": stats,
        "seasonal_summary": seasonal_summary,
        "correlations": corr
    }
    dataframes_to_save.update(extremes)
    save_csvs(dataframes_to_save)

    print("\n" + "=" * 50)
    print("ANALYSES TERMINEES")
    print("=" * 50)

if __name__ == "__main__":
    main()
