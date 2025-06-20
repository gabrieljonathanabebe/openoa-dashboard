#  OpenOA Dashboard – MC-Analyse & AEP-Auswertung

Ein interaktives Dashboard zur Analyse von Windenergie-Simulationen auf Basis der [OpenOA](https://github.com/NREL/OpenOA)-Bibliothek. Visualisiert werden Monte-Carlo-Simulationen, Modellkoeffizienten, Unsicherheiten und weitere Metriken im Zusammenhang mit Windparkprojekten.

---

##  Features

- MC-Analyse und Vergleich verschiedener Reanalyseprodukte (z. B. ERA5, MERRA2)
- Interaktive Verteilungsplots (Histogramme, Violinplots, Scatterplots, Heatmaps)
- Sensitivitätsanalyse & Korrelationen zwischen Modellmetriken
- Dunkel-/Hellmodus (Light/Dark Theme)
- Automatisch generierte Visualisierungen aus Simulationsergebnissen (CSV-Dateien)

---

##  Projektstruktur
├── app.py                 # Hauptanwendung (Dash)
├── assets/               # CSS für Styling & Themes
├── callbacks/            # Dash-Callbacks für Interaktivität
├── components/           # Layout-Teile pro Tab
├── data/
│   ├── raw/              # Output der Simulationen (z. B. mc_era5.csv)
│   └── config.py         # Farbzuordnung & Metrik-Infos
├── utils/                # Plot-Hilfsfunktionen & Statistiken
└── README.md             # Diese Datei

---

## ⚙ Voraussetzungen

- Python ≥ 3.8
- Empfohlen: virtuelles Environment

### Installation

bash
git clone git@github.com:gabrieljonathanabebe/openoa-dashboard.git
cd openoa-dashboard
pip install -r requirements.txt

Simulationen vorbereiten (optional)

Falls du eigene MC-Simulationen mit OpenOA durchführen möchtest:
	1.	Stelle sicher, dass du OpenOA installiert hast
	2.	Führe run_simulation.py aus, um CSVs unter data/raw/ zu erzeugen

Wenn du nur das Dashboard testen willst, reichen die vorhandenen CSV-Dateien im data/raw/-Ordner.

python app.py

Dann öffnet sich das Dashboard lokal unter:
http://127.0.0.1:8050

Lizenz

MIT License – siehe LICENSE

⸻

Autor

Gabriel Jonathan Abebe
gabrieljonathanabebe@gmail.com
Projekt im Rahmen einer eigenständigen Windenergieanalyse
