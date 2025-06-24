# OpenOA Dashboard – MC-Analyse & AEP-Auswertung

Ein interaktives Dashboard zur Visualisierung und Analyse von Windenergie-Simulationen basierend auf der OpenOA-Bibliothek. Es unterstützt Monte-Carlo-Auswertungen, Modellgütevergleiche, Unsicherheiten und Metriken im Rahmen von Windparkprojekten.

## Features

- Vergleich mehrerer Reanalyseprodukte (z. B. ERA5, MERRA2)
- Interaktive Visualisierungen (Histogramme, Violinplots, Scatterplots, Heatmaps, Zeitreihen)
- Analyse der Modellgüte (Korrelationen, Steigungen, CV, Bias usw.)
- Iterationsanalyse und Sensitivität
- Umschaltbarer Light-/Dark-Mode
- Automatisch generierte Plots auf Basis von CSV-Dateien
- Modularer Codeaufbau pro Auswertungsbereich

## Projektstruktur

<pre>
```
openoa-dashboard/
├── app.py                # Haupt-Dash-Anwendung
├── assets/               # CSS-Dateien (z. B. styles.css)
├── callbacks/            # Dash-Callbacks pro Tab (core.py, lt.py, etc.)
├── components/           # Layouts der Tabs
├── data/
│   ├── raw/              # Eingabedaten (CSV-Simulationsergebnisse)
│   ├── processed/              # Transformierte Eingabedaten
│   └── config.py         # Farben, Metrikdefinitionen
├── utils/
│   ├── plot_utils/       # Plotfunktionen pro Bereich (data.py, core.py etc.)
│   ├── compute_stats.py  # Statistische Hilfsfunktionen
│   ├── transform_lt.py   # LT-spezifische Transformationen
│   └── transform_por.py  # POR-spezifische Transformationen
├── requirements.txt      # Abhängigkeiten
└── README.md             # Diese Datei
```
</pre>


## Voraussetzungen

- Python >= 3.8
- Empfohlen: virtuelles Environment

## Installation

git clone https://github.com/gabrieljonathanabebe/openoa-dashboard.git
cd openoa-dashboard
pip install -r requirements.txt


## Start

python app.py

Das Dashboard ist dann erreichbar unter:
http://127.0.0.1:8050

## Lizenz

MIT License – siehe LICENSE

## Autor

Gabriel Jonathan Abebe  
jonathanabebe@outlook.de
Projekt im Rahmen einer eigenständigen Windenergieanalyse