from dash import dcc, html
from data.config import TIMESERIES_DATAFRAMES
from utils.compute_stats import compute_normalized_timeseries
from utils.plot_utils import get_time_series_plot


tab_data_layout = html.Div([
        html.H2("🌍 Reanalyse- & Energiedatenbasis", className="intro-title"),
        
        html.H4("📌 Windparkdaten: La Haute Borne", className="intro-subtitle"),
        html.P("""
            Der untersuchte Windpark „La Haute Borne“ liegt in Nordfrankreich und umfasst vier Windturbinen.
            Die Standortwahl erfolgte aufgrund der hohen Datenqualität und der dokumentierten saisonalen
            Windvariabilität. Der Windpark wird in verschiedenen Forschungsprojekten als Referenzstandort verwendet.
        """, className="intro-paragraph"),
        html.P("""
            Für die Analyse wurden SCADA-Daten zur monatlichen Energieproduktion im Zeitraum
            von Januar 2014 bis Dezember 2015 herangezogen. Nach Aggregation standen 24 Monatswerte zur Verfügung,
            die als Basis für die Modellierung der Beziehung zwischen Windgeschwindigkeit und Energieertrag dienten.
        """, className="intro-paragraph"),
        
        html.H4("🌬️ Reanalyse-Datensätze", className="intro-subtitle"),
        html.P("""
            Zur Erzeugung langjähriger Windzeitreihen wurden zwei Reanalyse-Produkte eingesetzt:
            ERA5 (bereitgestellt vom Copernicus Climate Change Service) sowie MERRA-2 (entwickelt von der NASA).
            Beide beruhen auf numerischen Wettermodellen, unterscheiden sich jedoch hinsichtlich räumlicher
            Auflösung, Assimilationstechniken und Modellcharakteristika.
        """, className="intro-paragraph"),
        html.P("""
            ERA5 bietet eine hohe zeitliche (1-stündlich) und räumliche (31 km) Auflösung und
            eignet sich insbesondere für die Analyse hochfrequenter Windvariationen. MERRA-2 hingegen
            liefert robustere Langzeittrends, zeigt jedoch eine stärkere Glättung kurzfristiger Schwankungen.
            Diese Unterschiede beeinflussen die Langzeitprognose signifikant.
        """, className="intro-paragraph"),
        
        html.Div([
            html.H3("Rollierender 12-Monatsmittelwert"),
            dcc.Graph(
                id="line-plot-windspeed",
                figure=get_time_series_plot(*compute_normalized_timeseries())
            )
        ], className="plot-container"),

        
        html.P("""
            Die obige Grafik zeigt den rollierenden 12-Monats-Mittelwert der normalisierten Windgeschwindigkeit
            für beide Reanalyse-Datensätze über einen Zeitraum von 20 Jahren. Die Linien wurden jeweils
            auf einen Mittelwert von 1 normalisiert, um relative Schwankungen besser vergleichbar zu machen.
        """, className="intro-paragraph"),
        html.P("""
            Auffällig ist, dass ERA5 stärker auf kurzfristige Windschwankungen reagiert, während MERRA-2
            glattere Verläufe zeigt. Diese strukturellen Unterschiede haben Einfluss auf die Modellgüte
            bei der Langzeitkorrektur von Energieerträgen – ein zentraler Aspekt dieser Analyse.
        """, className="intro-paragraph"),
])