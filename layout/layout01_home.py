from dash import html

# ------------------------------------------------------
# Layout: Startseite (Home)
# ------------------------------------------------------

home_layout = html.Div([

    html.Div([  # Innerer Wrapper für Inhalt

        # --- Titel / Kontext der Bachelorarbeit ---
        html.H2([
            html.I(className="fas fa-chart-bar", style={"marginRight": "10px"}),
            "Interaktives Analyse-Dashboard zur Windpark-Ertragsprognose"
        ], className="home-title"),

        html.P("""
            Diese Anwendung wurde im Rahmen der Bachelorarbeit
            „Windpark-Ertragsanalyse mit OpenOA und Untersuchung der Sensitivität ausgewählter Parameter“
            an der Hochschule Ansbach entwickelt. Ziel war es, ein Analysewerkzeug zur Bewertung
            meteorologischer Reanalyse-Daten auf die Langzeitprognose der Energieerträge bereitzustellen.
        """, className="home-paragraph"),

        # --- Ziel & Hintergrund ---
        html.H4([
            html.I(className="fas fa-bullseye", style={"marginRight": "10px"}),
            "Zielsetzung der Arbeit"
        ], className="home-subtitle"),

        html.P("""
            Im Zentrum der Untersuchung steht die Frage, wie sich die Nutzung verschiedener Reanalyse-Produkte
            – insbesondere ERA5 und MERRA-2 – auf die Prognosequalität des Annual Energy Production (AEP)
            eines Windparks auswirken. Das Dashboard erlaubt es, diese Sensitivität datenbasiert
            zu analysieren und Modellabweichungen interaktiv zu erkunden.
        """, className="home-paragraph"),

        # --- Methodischer Fokus & Datengrundlage ---
        html.H4([
            html.I(className="fas fa-search", style={"marginRight": "10px"}),
            "Untersuchung der Reanalyse-Daten"
        ], className="home-subtitle"),

        html.P("""
            In der zugrunde liegenden Bachelorarbeit wurden die Reanalyse-Produkte ERA5 und MERRA-2 hinsichtlich
            ihrer Modellcharakteristika, zeitlichen Auflösung und Eignung für die Langzeitkorrektur von
            Energieerträgen analysiert. Dabei zeigte sich, dass ERA5 zwar hochauflösende Windvariationen
            abbildet, jedoch langfristige Schwankungen teilweise überlagert. Im Gegensatz dazu bietet
            MERRA-2 stabilere Trends über lange Zeiträume, neigt jedoch zur Überbetonung einzelner Windjahre.
        """, className="home-paragraph"),

        html.P("""
            Zur Reduktion von Störeinflüssen wurde ein Huber-Filter auf die ERA5-Daten angewendet,
            der kurzfristige Ausreißer erfolgreich unterdrückt. Allerdings führte dieser zu einem
            leichten systematischen Bias. Als vielversprechender Ansatz erwies sich eine kombinierte
            Analyse beider Reanalyse-Produkte: Die jeweiligen Schwächen wurden so weitgehend kompensiert,
            was zu einer realistischeren und stabileren Bewertung der Unsicherheiten führte.
        """, className="home-paragraph"),

        # --- Funktion des Dashboards ---
        html.H4([
            html.I(className="fas fa-laptop-code", style={"marginRight": "10px"}),
            "Funktion des Dashboards"
        ], className="home-subtitle"),

        html.P("""
            Dieses Dashboard dient als interaktives Analysewerkzeug, um die Sensitivität
            ausgewählter Parameter visuell und nachvollziehbar zu untersuchen. Nutzer:innen
            können unter anderem Reanalyse-Kombinationen vergleichen, Modellmetriken
            einsehen, Scatterplots analysieren und die langfristige Entwicklung der
            Energieerträge nachvollziehen.
        """, className="home-paragraph"),

        # --- Ausblick ---
        html.H4([
            html.I(className="fas fa-lightbulb", style={"marginRight": "10px"}),
            "Ausblick"
        ], className="home-subtitle"),

        html.P("""
            Für weiterführende Analysen empfiehlt sich die Integration zusätzlicher meteorologischer
            Parameter sowie der Einsatz nichtlinearer Modelle und Methoden des maschinellen Lernens,
            um Unsicherheiten noch robuster abzubilden.
        """, className="home-paragraph"),

        html.Hr(),

        # --- Kontaktinformationen ---
        html.H4([
            html.I(className="fas fa-envelope", style={"marginRight": "10px"}),
            "Kontakt"
        ], className="home-subtitle"),

        html.P("Gabriel Jonathan Abebe", className="home-paragraph"),
        html.P("jonathanabebe@outlook.de", className="home-paragraph"),
        html.P("Bachelorarbeit – Hochschule Ansbach, 2025", className="home-paragraph"),

        # --- Technologien & Version ---
        html.H4([
            html.I(className="fas fa-tools", style={"marginRight": "10px"}),
            "Technologien"
        ], className="home-subtitle"),

        html.P("""
            Erstellt mit Python, Dash (Plotly), Pandas, Plotly Graph Objects und dem OpenOA-Framework.
        """, className="home-paragraph"),
        html.P("Version 3.0 – erste stabile Veröffentlichung – Stand: Juni 2025", className="home-paragraph")

    ], className="main-content")
])