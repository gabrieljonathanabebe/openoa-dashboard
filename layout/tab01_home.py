from dash import html


tab_home_layout = html.Div([  
    html.H1("📊 Windpark-Ertragsanalyse mit Reanalyse-Daten", className="intro-title"),

    html.H3("🌬️ Projektüberblick", className="intro-subtitle"),
    html.P("""
        Diese interaktive Anwendung wurde im Rahmen einer Bachelorarbeit entwickelt und visualisiert die
        Auswirkungen verschiedener Reanalyse-Produkte (ERA5, MERRA-2, kombiniert) auf die Langzeitprognose
        der Energieproduktion eines Windparks. Mithilfe des OpenOA-Frameworks wurden die Daten analysiert
        und aufbereitet, um Unsicherheiten und Modellunterschiede nachvollziehbar darzustellen.
    """, className="intro-paragraph"),

    html.H3("🔍 Methodischer Fokus", className="intro-subtitle"),
    html.P("""
        Die Analyse umfasst die Korrektur historischer Energieerträge, Anwendung eines robusten Huber-Filters
        sowie die Kombination von Reanalyse-Datensätzen zur optimierten Unsicherheitsbewertung. Besonderes Augenmerk
        liegt auf der interannuellen Variabilität und der robusten Schätzung des Annual Energy Production (AEP).
    """, className="intro-paragraph"),

    html.H3("🧭 Navigation", className="intro-subtitle"),
    html.P("""
        Nutzen Sie die Tabs auf der linken Seite, um zentrale Kennzahlen, Scatterplots sowie
        die Langzeitanalyse interaktiv zu erkunden.
    """, className="intro-paragraph"),

    html.Hr(),

    html.H3("📬 Kontakt", className="intro-subtitle"),
    html.P("Gabriel Jonathan Abebe", className="intro-paragraph"),
    html.P("jonathan.abebe@hs-ansbach.de", className="intro-paragraph"),
    html.P("Bachelorarbeit – 2025, Hochschule Ansbach", className="intro-paragraph"),
    
    html.H3("🛠️ Technologien", className="intro-subtitle"),
    html.P("Erstellt mit Dash (Plotly), Pandas, Plotly Graph Objects und OpenOA.", className="intro-paragraph"),
    html.P("Version 1.0 – Stand: Juni 2025", className="intro-paragraph"),

    # Optional: Bild oder Logo einfügen
    # html.Img(src="/assets/unilogo.png", style={"width": "160px", "marginTop": "20px"})
])




