import matplotlib.pyplot as plt

def graph_monthly_temp(monthly_avg):
    """
    Trace un graphique simple de la température moyenne par mois.

    Parameters:
        monthly_avg : pandas Series avec
                      - index = mois (1 à 12)
                      - valeurs = température moyenne
    """
    # Récupérer les mois (1,2,...,12) et les températures correspondantes
    mois = monthly_avg.index
    temp = monthly_avg.values

    # Créer le graphique
    plt.plot(mois, temp, marker='o', color='orange')  # ligne orange avec petits cercles sur chaque point
    plt.title("Température moyenne par mois - Paris 2024")  # Titre du graphique
    plt.xlabel("Mois")                                     # Axe X
    plt.ylabel("Température moyenne (°C)")                # Axe Y
    plt.xticks(mois)                                       # Affiche tous les mois sur l'axe X
    plt.grid(True)                                         # Ajoute une grille pour mieux lire les valeurs

    # Afficher le graphique
    plt.show()
