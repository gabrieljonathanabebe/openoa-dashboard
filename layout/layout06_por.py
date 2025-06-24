from dash import dcc, html
from data.config import DATAFRAMES, POR_DATAFRAMES

por_layout = html.Div([

    html.H2([
        html.I(className="fas fa-chart-area", style={"marginRight": "10px"}),
        "Analyse der POR-Modellierung"
    ], className="home-title"),

    html.Div([

        # Oberer Textabschnitt
        html.Div([
            html.P("""
                In dieser Ansicht wird untersucht, wie präzise die modellierte Jahresenergie (GPS) 
                der Period of Record (POR) über alle Iterationen hinweg berechnet wurde – unabhängig 
                von der Modellgüte der Bootstrapping-Stichprobe. Die POR-Modellierung basiert auf der 
                Anwendung des trainierten Modells auf die vollständige Datenbasis (nicht nur das Trainingssample) 
                und liefert damit eine realitätsnahe Einschätzung der Prognosekraft jeder Analyse.
            """, className="home-paragraph"),

            html.H3("Verteilung der modellierten Jahresenergie (GPS)", className="home-subtitle"),

            html.P("""
                Links ist die Verteilung der simulierten GPS-Werte zweier ausgewählter Analysen als Histogramm dargestellt. 
                Rechts visualisiert ein Violinplot die Dichteverteilung und Streuung einzelner Simulationen – 
                ein hilfreiches Werkzeug, um die Stabilität der Prognoseergebnisse besser einzuordnen.
            """, className="home-paragraph"),

            html.P("""
                Über die Optionen lassen sich ergänzende Informationen einblenden: 
                darunter die tatsächliche Energieproduktion im POR-Zeitraum (gestrichelte Linie) 
                und die Mittelwerte der Simulationen – um potenzielle Modellabweichungen frühzeitig zu erkennen.
            """, className="home-paragraph mb-40")
        ]),

        # Plot + Dropdowns nebeneinander
        html.Div([

            # Linke Steuerungsleiste
            html.Div([
                html.Label("MC-Analyse 1:"),
                dcc.Dropdown(
                    id="por-label-1-dropdown",
                    options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                    value="ERA5",
                    clearable=False
                ),
                html.Br(),

                html.Label("MC-Analyse 2:"),
                dcc.Dropdown(
                    id="por-label-2-dropdown",
                    options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                    value="ERA5 gefiltert",
                    clearable=False
                ),

                html.Br(),

                html.Label("Optionen:"),
                dcc.Checklist(
                    id="por-options",
                    options=[
                        {"label": "Beobachteter Wert", "value": "show-observed"},
                        {"label": "Mittelwerte der MC-Analysen", "value": "show-means"},
                    ],
                    value=[],
                    labelStyle={"display": "block", "marginBottom": "0px", "fontSize": "15px", "marginTop": "10px"}
                )
            ], style={"flex": "1", "minWidth": "200px"}, className="centered-column-flex sidebar-dropdown-group"),

            # Rechte Seite: Plot
            html.Div([
                dcc.Loading(
                    id="por-histogram-loading",
                    type="circle",
                    children=dcc.Graph(id="por-histogram-violin-plot")
                )
            ], style={"flex": "5"}, className="plot-container")

        ], style={
            "display": "flex",
            "gap": "20px",
            "alignItems": "center",
        })
    ]),

    html.Div([
        html.Div([
            html.H3("Regressionsbasierte Modellanalyse nach Iteration", className="home-subtitle mt-40"),

            html.P("""
                Dieser Abschnitt erlaubt eine gezielte Analyse einzelner Iterationen auf Basis verschiedener 
                Regressionsmetriken. Für zwei ausgewählte MC-Analysen wird jeweils die Iteration angezeigt, 
                die – abhängig von der gewählten Metrik – beispielsweise den höchsten oder niedrigsten Wert erreicht.
            """, className="home-paragraph"),

            html.P("""
                Die Diagramme zeigen dabei die Datenpunkte aus dem Trainings- (grün) und Testbereich (rot). 
                Die gestrichelte Linie repräsentiert das trainierte Regressionsmodell. 
                Ergänzend werden Kennwerte wie R², MSE und Bias oberhalb der Grafiken eingeblendet.
            """, className="home-paragraph mb-40"),
        ]),

        html.Div([

            html.Div([
                html.Label("Metrik:", className="home-paragraph"),
                dcc.Dropdown(
                    id="por-metric-dropdown",
                    options=[
                        {"label": "Slope (GWh/(m/s))", "value": "slope"},
                        {"label": "Intercept (GWh)", "value": "intercept"},
                        {"label": "R Squared (R²)", "value": "r2"},
                        {"label": "Mean Squared Error (MSE)", "value": "mse"},
                        {"label": "Bias (GWh/yr)", "value": "yearly_bias"}
                    ],
                    value="slope",
                    clearable=False
                ),
                html.Label("Wert:", className="home-paragraph"),
                dcc.Dropdown(
                    id="por-metric-value-dropdown",
                    options=[
                        {"label": "Maximum", "value": "max"},
                        {"label": "3. Quantil", "value": "q3"},
                        {"label": "Median", "value": "median"},
                        {"label": "1. Quantil", "value": "q1"},
                        {"label": "Minimum", "value": "min"},
                    ],
                    value="max",
                    clearable=False
                )
            ], style={"flex": "1"}, className="sidebar-dropdown-group"),

            html.Div([
                html.Div([
                    html.Div([
                        html.Label("MC-Analyse links:", className="home-paragraph"),
                        dcc.Dropdown(
                            id="reg-scatter-label-dropdown-1",
                            options=[
                                {"label": label, "value": label} for label in POR_DATAFRAMES.keys()
                            ],
                            value="ERA5",
                            clearable=False
                        )
                    ], style={"flex": "1"}),
                    html.Div([
                        html.Label("MC-Analyse rechts:", className="home-paragraph"),
                        dcc.Dropdown(
                            id="reg-scatter-label-dropdown-2",
                            options=[
                                {"label": label, "value": label} for label in POR_DATAFRAMES.keys()
                            ],
                            value="MERRA2",
                            clearable=False
                        )
                    ], style={"flex": "1"}),
                ], style={"display": "flex"}, className="plot-dropdown-container"),

                html.Div([
                    dcc.Loading(
                        id="reg-scatter-loading",
                        type="circle",
                        fullscreen=False,
                        children=dcc.Graph(id="reg-scatter")
                    )
                ], className="plot-container")
            ], style={"flex": "7"})
        ], className="centered-flex-row"),

        html.Div([
            html.P("""
                Die Darstellung ermöglicht ein besseres Verständnis dafür, wie stark die Regressionsparameter innerhalb 
                einzelner Iterationen variieren und welche Datenbereiche maßgeblich das Modellverhalten beeinflussen. 
                Besonders beim Vergleich unterschiedlicher Reanalyseprodukte lassen sich hier wichtige Unterschiede erkennen.
            """, className="home-paragraph mt-40"),
        ])
    ]),

    html.Div([

        html.Div([
            html.H3("Zeitlicher Verlauf der modellierten Energie", className="home-subtitle"),

            html.P("""
                Diese Ansicht zeigt die simulierte monatliche Energieproduktion über den gesamten POR-Zeitraum hinweg.
                Dabei wird das trainierte Modell jeweils auf die komplette Datengrundlage angewendet – ganz ohne Bootstrapping –, 
                um potenzielle Verzerrungen auszuschließen.
            """, className="home-paragraph"),

            html.P("""
                Mehrere Analysen können gleichzeitig dargestellt werden, um Unterschiede im zeitlichen Verlauf zu erkennen. 
                Die weiße Referenzlinie zeigt die tatsächliche Energieproduktion auf Basis der SCADA-Daten.
            """, className="home-paragraph mb-40"),
        ]),

        html.Div([

            html.Div([

                html.Label("Metrik:", className="home-paragraph"),
                dcc.Dropdown(
                    id="timeseries-metric-dropdown",
                    options=[
                        {"label": "Slope (GWh/(m/s))", "value": "slope"},
                        {"label": "Intercept (GWh)", "value": "intercept"},
                        {"label": "R²", "value": "r2"},
                        {"label": "MSE", "value": "mse"},
                        {"label": "Bias", "value": "yearly_bias"}
                    ],
                    value="slope",
                    clearable=False
                ),

                html.Label("Wert:", className="home-paragraph"),
                dcc.Dropdown(
                    id="timeseries-metric-method-dropdown",
                    options=[
                        {"label": "Maximum", "value": "max"},
                        {"label": "3. Quantil", "value": "q3"},
                        {"label": "Median", "value": "median"},
                        {"label": "1. Quantil", "value": "q1"},
                        {"label": "Minimum", "value": "min"},
                    ],
                    value="median",
                    clearable=False
                )
            ], style={"flex": "1"}, className="sidebar-dropdown-group"),

            html.Div([
                html.Div([
                    html.Label("MC-Analysen (mehrfach wählbar):", className="home-paragraph"),
                    dcc.Dropdown(
                        id="timeseries-labels-dropdown",
                        options=[{"label": label, "value": label} for label in POR_DATAFRAMES.keys()],
                        value=["ERA5"],
                        multi=True,
                        clearable=False
                    )
                ], className="plot-dropdown-container"),
                html.Div([
                    dcc.Loading(
                        id="timeseries-plot-loading",
                        type="circle",
                        children=dcc.Graph(id="timeseries-energy-plot")
                    )
                ])
            ], style={"flex": "7"}, className="plot-container")

        ], className="centered-flex-row"),

        html.Div([
            html.P("""
                Die Grafik hilft dabei, saisonale Muster, konsistente Abweichungen oder auffällige Trends in der modellierten 
                Energieentwicklung zu erkennen.
            """, className="home-paragraph mt-40")
        ])

    ])

], className="main-content")