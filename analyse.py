import pandas as pd

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
