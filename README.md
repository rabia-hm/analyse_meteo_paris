# Analyse Météo Paris 2024

Projet d'analyse des données météorologiques de Paris sur l'année 2024.

## Description

Ce projet traite et visualise des données météo journalières pour Paris (2024). Il couvre l'ensemble du pipeline data : chargement, nettoyage, analyse statistique et visualisation graphique.

## Données

Le fichier `data/paris_meteo_2024.csv` contient une ligne par jour avec les colonnes suivantes :

| Colonne               | Description                        |
|-----------------------|------------------------------------|
| `date`                | Date (YYYY-MM-DD)                  |
| `temp_max`            | Température maximale (°C)          |
| `temp_min`            | Température minimale (°C)          |
| `temp_mean`           | Température moyenne (°C)           |
| `precipitation_mm`    | Précipitations (mm)                |
| `wind_speed_max_kmh`  | Vitesse max du vent (km/h)         |
| `humidity_mean_pct`   | Humidité moyenne (%)               |

## Structure du projet

```
meteo_paris_me/
├── data/
│   └── paris_meteo_2024.csv   # Données brutes
├── exploration.py             # Chargement, nettoyage et exploration
├── analyse.py                 # Analyses statistiques et saisonnières
├── visualisation.py           # Graphiques matplotlib
├── requirements.txt           # Dépendances Python
└── README.md
```

## Fonctionnalités

### `exploration.py`
- Chargement et conversion des dates
- Rapport de qualité des données (valeurs manquantes, doublons, cohérence)
- Nettoyage : interpolation linéaire pour les températures/vent/humidité, remplacement par 0 pour les précipitations
- Calcul des moyennes mensuelles

### `analyse.py`
- Statistiques descriptives (min, max, moyenne, écart-type) sur toutes les variables
- Analyse saisonnière : moyennes de température et total de précipitations par saison
- Détection des jours extrêmes : canicule (> 30°C) et gel (< 0°C)
- Calcul des corrélations entre variables
- Export des résultats en CSV dans le dossier `outputs/`

### `visualisation.py`
- Graphique de la température moyenne mensuelle (courbe avec marqueurs)
- Graphique de l'évolution journalière de la température sur toute l'année

## Installation

```bash
# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # macOS/Linux

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

```bash
# Exploration et nettoyage des données + graphiques
python exploration.py

# Analyses statistiques + export CSV
python analyse.py
```

## Technologies utilisées

- **Python 3.12**
- **pandas** — manipulation et analyse des données
- **matplotlib** — visualisation graphique
- **numpy** — calculs numériques
