import os
import pandas as pd



RAW_DIR = os.path.join("data", "raw")
PROCESSED_POR_DIR = os.path.join("data", "processed", "por")
PROCESSED_SCATTER_DIR = os.path.join("data", "processed", "scatter")


GROSS_POR_OBSERVED = 12.229


AVAILABLE_DATASETS = {
    "ERA5": "mc_era5.csv",
    "MERRA2": "mc_merra2.csv",
    "Kombiniert": "mc_combined.csv",
    "ERA5 gefiltert": "mc_era5_true.csv",
    "MERRA2 gefiltert": "mc_merra2_true.csv",
}

DATAFRAMES = {
    label: pd.read_csv(os.path.join(RAW_DIR, filename))
    for label, filename in AVAILABLE_DATASETS.items()
}


TIMESERIES_FILES = {
    "ERA5": "era5_timeseries.csv",
    "MERRA2": "merra2_timeseries.csv"
}

TIMESERIES_DATAFRAMES = {
    label: pd.read_csv(os.path.join(RAW_DIR, filename), parse_dates=["Date"])
    for label, filename in TIMESERIES_FILES.items()
    
}

# Zeitreihen (für Zeitverlaufsplot)
POR_DATASETS = {
    "ERA5": "mc_era5_por.csv",
    "MERRA2": "mc_merra2_por.csv",
    "ERA5 gefiltert": "mc_era5_gefiltert_por.csv",
    "MERRA2 gefiltert": "mc_merra2_gefiltert_por.csv",
}

POR_DATAFRAMES = {
    label: pd.read_csv(os.path.join(PROCESSED_POR_DIR, filename), parse_dates=["time"])
    for label, filename in POR_DATASETS.items()
}

# Scatterplot-Daten (für Regressionsplot)
POR_SCATTERSETS = {
    "ERA5": "mc_era5_scatter.csv",
    "MERRA2": "mc_merra2_scatter.csv",
    "ERA5 gefiltert": "mc_era5_gefiltert_scatter.csv",
    "MERRA2 gefiltert": "mc_merra2_gefiltert_scatter.csv",
}

POR_SCATTERFRAMES = {
    label: pd.read_csv(os.path.join(PROCESSED_SCATTER_DIR, filename), parse_dates=["time"])
    for label, filename in POR_SCATTERSETS.items()
}


COLOR_MAP = {
    "ERA5": "#00FFFF",           # Neon Cyan (statt skyblue)
    "ERA5 gefiltert": "#FF9900", # Neon Orange
    "MERRA2": "#FF1744",         # Neon Rot (kräftiger als tomato)
    "MERRA2 gefiltert": "#FF66CC", # Neon Pink
    "Kombiniert": "#39FF14"      # Neon Grün
}


LONGTERM_DIR = os.path.join("data", "processed", "longterm")

LONGTERM_FILES = {
    "ERA5": "mc_era5_lt.csv",
    "ERA5 gefiltert": "mc_era5_filtered_lt.csv",
    "MERRA2": "mc_merra2_lt.csv",
    "MERRA2 gefiltert": "mc_merra2_filtered_lt.csv",
    "Kombiniert": "mc_combined_lt.csv"
}

LONGTERM_DFS = {
    label: pd.read_csv(os.path.join(LONGTERM_DIR, filename))
    for label, filename in LONGTERM_FILES.items()
}


TAB_KEYWORDS = {
    "tab-home": [
        "projekt", "überblick", "einleitung", "bachelorarbeit", "openoa",
        "reanalyse", "era5", "merra2", "kombiniert", "unsicherheit", "interaktiv",
        "aep", "interannuell", "variabilität", "navigation", "kontakt", "technologien",
        "dash", "plotly", "pandas", "hochschule", "ansbach", "visualisierung", "energieproduktion",
        "filter", "huber", "schätzung"
    ],
    
    "tab-data": [
        "reanalyse", "windpark", "la haute borne", "nordfrankreich",
        "scada", "energie", "energieproduktion", "zeitreihe", "monat", "2014", "2015",
        "era5", "merra2", "copernicus", "nasa", "modell", "wettermodell", "datenqualität",
        "windgeschwindigkeit", "normalisierung", "rollierend", "mittelwert", "12-monats",
        "auflösung", "schwankung", "trend", "vergleich", "zeitverlauf", "plot", "graph",
        "mittelwert", "analyse", "glättung", "kurzfristig", "langfristig"
    ],
    
    "tab-core": [
        "aep", "annual energy production", "unsicherheit", "cv", "kern", "zentrale",
        "barplot", "violinplot", "boxplot", "jitter", "scatterplot", "histogramm",
        "vergleich", "era5", "merra2", "kombiniert", "gefiltert",
        "iterationen", "iteration", "mean", "mittelwert", "iav", "iav-faktor",
        "analyse", "auswertung", "kennzahl", "rolling", "mean", "linie", "plot",
        "standardabweichung", "abweichung", "unsicherheitsanalyse", "verteilung",
        "vergleich aep", "aep analyse"
    ],
    
    "tab-lt": [
        "lt", "langzeit", "longterm", "langzeitanalyse",
        "entwicklung", "zeitreihe", "trend", "jahre", "jahr", "zeit",
        "energie", "lt-bruttoenergie", "wind", "iav", "interannual variability",
        "cv", "variabilität", "monte-carlo", "mc", "vergleich", "filter", "gefiltert",
        "steigung", "regression", "slope", "korrelation",
        "plot", "scatter", "linie", "graph", "visualisierung",
        "era5", "merra2", "kombiniert",
        "auswertung", "verlauf", "unsicherheit", "analyse"
    ],
    
    "tab-sensitivity": [
        "modell", "modellvergleich", "prognose", "modellgüte", "modellqualität", 
        "vergleich", "verteilung", "koeffizient", "parameter", 
        "steigung", "intercept", "achse", "achsenabschnitt", 
        "r2", "r²", "mse", "mean squared error", "bestimmtheitsmaß",
        "histogramm", "violin", "scatter", "streudiagramm", 
        "x-achse", "y-achse", "z-achse", "farben", "korrelation",
        "sensitivität", "analyse", "grafik", "visualisierung",
        "era5", "merra2", "kombiniert", "filter", "gefiltert"
    ],
    
    "tab-por": [
        "por", "period of record", "zeitreihe", "analyse", "histogramm", "violin", 
        "asymmetrisch", "regression", "iteration", "steigung", "intercept", 
        "r2", "modell", "streuung", "scatter", "verlauf", "unsicherheit"
    ]
}


WEEKDAY_MAP = {
    "Mon": "Mo.",
    "Tue": "Di.",
    "Wed": "Mi.",
    "Thu": "Do.",
    "Fri": "Fr.",
    "Sat": "Sa.",
    "Sun": "So."
}

MONTH_MAP = {
    "January": "Januar",
    "February": "Februar",
    "March": "März",
    "April": "April",
    "May": "Mai",
    "June": "Juni",
    "July": "Juli",
    "August": "August",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Dezember"
}


METRIC_INFO = {
    "slope": {
        "metric_en": "Slope (GWh/(m/s))",
        "metric_de": "Steigung (GWh/(m/s))"
    },
    "intercept": {
        "metric_en": "Intercept (GWh)",
        "metric_de": "Achsenabschnitt (GWh)"
    },
    "r2": {
        "metric_en": "R-squared (R²)",
        "metric_de": "Bestimmtheitsmaß (R²)"
    },
    "mse": {
        "metric_en": "MSE (GWh²)",
        "metric_de": "MSE (GWh²)",
    },
    "aep_final": {
        "metric_en": "AEP (GWh/yr)",
        "metric_de": "AEP (GWh/a)"
    },
    "aep": {
        "metric_en": "AEP per Iteration (GWh/yr)",
        "metric_de": "AEP pro Iteration (GWh/a)"
    },
    "iav_nsim": {
        "metric_en": "IAV-Factor",
        "metric_de": "IAV-Faktor"
    },
    "iav": {
        "metric_en": "IAV-Energy",
        "metric_de": "IAV-Energie"
    },
    "iav_wind": {
        "metric_en": "IAV-Wind",
        "metric_de": "IAV-Wind"
    },
    "yearly_bias": {
        "metric_en": "Yearly Bias per Iteration (GWh/yr)",
        "metric_de": "Jährlicher Bias pro Iteration (GWh/a)"
    },
    "gps": {
        "metric_en": "Predicted POR-Gross-Energy (GWh/yr)",
        "metric_de": "Modellierte POR-Bruttoenergie (GWh/a)"
    },
    "outlier_threshold": {
        "metric_en": "Huber threshold",
        "metric_de": "Huber-Schwellenwert"
    },
    "energy": {
        "metric_en": "LT-Energy (GWh/yr)",
        "metric_de": "LT-Energie (GWh/a)"
    },
    "wind": {
        "metric_en": "Average LT-Windspeed (m/s)",
        "metric_de": "Durchschnittliche LT-Windgeschwindigkeit (m/s)"
    },
    "metered_energy_fraction": {
    "metric_en": "Metered Energy Correction Factor",
    "metric_de": "Faktor für Messzählungskorrektur"
    },
    "num_points": {
        "metric_en": "Number of Data Points",
        "metric_de": "Anzahl der Regressionspunkte"
    },
    "num_years_windiness": {
        "metric_en": "Number of Years for LT-Correction",
        "metric_de": "Anzahl der Jahre zur LT-Korrektur"
    }
}





















