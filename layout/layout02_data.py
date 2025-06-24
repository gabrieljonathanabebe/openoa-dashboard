from dash import dcc, html

from utils.compute_stats import compute_normalized_timeseries
from utils.plot_utils.data import plot_reanalysis_timeseries


# ------------------------------------------------------
# Layout: Reanalyse-Daten & Windparkbeschreibung
# ------------------------------------------------------

data_layout = html.Div([

    # --- Seitentitel ---
    html.H2([
        html.I(className="fas fa-database", style={"marginRight": "10px"}),
        "Datenquellen"
    ], className="home-title"),

    # ------------------------------------------------------
    # Windparkdaten
    # ------------------------------------------------------
    html.H4([
        html.I(className="fas fa-bolt", style={"marginRight": "8px"}),
        "Windpark: La Haute Borne"
    ], className="home-subtitle"),

    html.P("""
        Die Energiedaten stammen aus dem Windpark La Haute Borne in Nordfrankreich.
        Der Park besteht aus vier Windturbinen, deren SCADA-Systeme kontinuierlich Betriebsdaten erfassen.
        Diese beinhalten neben der Energieproduktion auch weitere Betriebsparameter.
    """, className="home-paragraph"),

    html.P("""
        La Haute Borne gilt als gut dokumentierter Standort, der aufgrund der hohen Datenqualität
        regelmäßig für Forschungszwecke herangezogen wird (Perr-Sauer et al., 2021).
        Die geographische Lage begünstigt eine deutliche saisonale Windvariabilität,
        was ihn für Untersuchungen zur interannuellen Variabilität (IAV) besonders relevant macht.
    """, className="home-paragraph"),

    html.P("""
        Die Energiedaten decken den Zeitraum vom 1. Januar 2014 bis zum 31. Dezember 2015 ab.
        Nach Aggregation stehen 24 monatliche Werte pro Iteration für die Regression zur Verfügung.
        Diese Zeitreihe dient als Referenz für die Modellierung der Beziehung zwischen
        Windgeschwindigkeit und Energieproduktion und bildet die Grundlage zur Bewertung der Modellgüte.
    """, className="home-paragraph"),

    # ------------------------------------------------------
    # Reanalyse-Daten
    # ------------------------------------------------------
    html.H4([
        html.I(className="fas fa-cloud", style={"marginRight": "8px"}),
        "Reanalyse-Datensätze"
    ], className="home-subtitle"),

    html.P("""
        Zur Erzeugung der Windzeitreihen werden zwei Reanalyse-Produkte eingesetzt, die auf
        globalen numerischen Wettermodellen basieren. Beide liefern rekonstruierte historische
        Winddaten mit unterschiedlicher räumlicher und zeitlicher Auflösung.
    """, className="home-paragraph"),

    html.P([
        html.B("ERA5: "),
        "Bereitgestellt vom ECMWF im Rahmen des Copernicus Climate Change Service (C3S). ",
        "ERA5 bietet eine räumliche Auflösung von etwa 31 km sowie eine stündliche zeitliche Auflösung. ",
        "Dank seiner hohen Auflösung eignet sich ERA5 besonders zur Erfassung kurzzeitiger Windschwankungen ",
        "(Setchell, 2020). Dies macht es geeignet für Analysen, bei denen hochfrequente Variabilität eine ",
        "zentrale Rolle spielt."
    ], className="home-paragraph"),

    html.P([
        html.B("MERRA-2: "),
        "Ein Reanalyse-Produkt der NASA (GMAO), das mit einer räumlichen Auflösung von ca. 50 km und ",
        "ebenfalls stündlicher Auflösung langfristige atmosphärische Entwicklungen abbildet. ",
        "MERRA-2 zeichnet sich durch eine geglättete Darstellung kurzfristiger Schwankungen aus, ",
        "betont dafür jedoch langfristige Windtrends stärker."
    ], className="home-paragraph mb-40"),

    # ------------------------------------------------------
    # Vergleichsgrafik: Zeitreihe Windgeschwindigkeit
    # ------------------------------------------------------
    html.Div([
        dcc.Graph(
            id="line-plot-windspeed",
            figure=plot_reanalysis_timeseries(*compute_normalized_timeseries()),
        )
    ], className="plot-container"),

    html.P("""
        Die obige Grafik zeigt den rollierenden 12-Monats-Mittelwert der normalisierten Windgeschwindigkeit
        für beide Reanalyse-Datensätze über einen Zeitraum von 20 Jahren. Die Linien wurden jeweils
        auf einen Mittelwert von 1 normalisiert, um relative Schwankungen besser vergleichbar zu machen.
    """, className="home-paragraph mt-40"),

    html.P("""
        Auffällig ist, dass die blaue ERA5-Kurve ein wenig feiner verläuft, während die MERRA-2-Kurve
        die Trends in den langfristigen Windressourcen ein bisschen stärker betont und die Grafik
        somit die Charakteristik beider Produkte widerspiegelt.
    """, className="home-paragraph")

], className="main-content")
           
           