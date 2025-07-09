from dash import dcc, html
from data.config import DATAFRAMES, METRIC_INFO

# ------------------------------------------------------
# Layout: Regressionsanalyse
# ------------------------------------------------------

reg_layout = html.Div([

    # --- Titel ---
    html.H2([
        html.I(className="fas fa-chart-line", style={"marginRight": "10px"}),
        "Einfluss der Regressionsparameter"
    ], className="home-title"),

    # --- Einleitung ---
    html.P("""
        Dieser Abschnitt beleuchtet, wie verschiedene Regressionsmetriken – etwa Steigung, Achsenabschnitt, 
        Bestimmtheitsmaß (R²) und mittlerer quadratischer Fehler (MSE) – die AEP-Prognose beeinflussen. 
        Im Fokus steht der Vergleich zwischen klassischen Regressionsansätzen und dem robusteren Huber-Verfahren. 
        Ziel ist es, mögliche Unterschiede in der Modellgüte und der Sensitivität gegenüber Ausreißern sichtbar zu machen.
    """, className="home-paragraph"),

    # --- Histogramm & Violinplot ---
    html.H3("Verteilung der Modellkoeffizienten", className="home-subtitle"),

    html.P("""
        Auf der linken Seite lassen sich gezielt zwei Analysen auswählen und miteinander vergleichen. 
        Zusätzlich kann ein Regressionsparameter festgelegt werden, dessen Verteilung im Histogramm dargestellt wird. 
        Der asymmetrische Violinplot ergänzt das Bild um Dichteinformationen und zeigt einzelne Simulationen. 
        So wird deutlich, wie stark zentrale Modellparameter über verschiedene Ansätze hinweg streuen.
    """, className="home-paragraph mb-40"),

    html.Div([

        # Steuerung
        html.Div([
            html.Label("Regressionsmetrik:"),
            dcc.Dropdown(
                id="metric-dropdown",
                options=[
                    {"label": "Steigung (GWh/(m/s))", "value": "slope"},
                    {"label": "Achsenabschnitt (GWh)", "value": "intercept"},
                    {"label": "Bestimmtheitsmaß (R²)", "value": "r2"},
                    {"label": "Mean Squared Error (MSE)", "value": "mse"}
                ],
                value="r2",
                clearable=False
            ),

            html.Br(),

            html.Label("Analyse 1:"),
            dcc.Dropdown(
                id="label-1-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="ERA5",
                clearable=False,
            ),

            html.Br(),

            html.Label("Analyse 2:"),
            dcc.Dropdown(
                id="label-2-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="MERRA2",
                clearable=False,
            ),
        ], style={"flex": "1"}, className="sidebar-dropdown-group"),

        # Grafik
        html.Div([
            dcc.Loading(
                id="model-comparison-plot-loading",
                type="circle",
                children=dcc.Graph(id="model-comparison-plot")
            )
        ], style={"flex": "5"}, className="plot-container")

    ], className="centered-flex-row"),

    # --- Scatteranalyse ---
    html.H3("Zusammenhänge zwischen Modellparametern", className="home-subtitle mt-40"),

    html.P("""
        In der folgenden Darstellung lassen sich zwei beliebige Regressionsmetriken gegenüberstellen. 
        Eine dritte Kennzahl wird dabei als Farbcodierung eingebunden – etwa R², der AEP-Wert oder der IAV-Faktor. 
        So entstehen interaktive 3D-artige Analysen, mit denen komplexe Abhängigkeiten sichtbar werden.
    """, className="home-paragraph"),

    html.P("""
        Interessant ist vor allem der Vergleich zweier Monte-Carlo-Simulationen: 
        Lassen sich bestimmte Muster ausschließlich in einer Analyse beobachten? 
        Oder zeigen sich Unterschiede auch im Zusammenspiel mit Filtern wie dem Huber-Verfahren?
    """, className="home-paragraph mb-40"),

    html.Div([

        # Steuerung
        html.Div([
            html.Label("X-Achse:"),
            dcc.Dropdown(
                id="x-metric-dropdown",
                options=[{"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()],
                value="mse",
                clearable=False
            ),

            html.Br(),

            html.Label("Y-Achse:"),
            dcc.Dropdown(
                id="y-metric-dropdown",
                options=[{"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()],
                value="r2",
                clearable=False
            ),

            html.Br(),

            html.Label("Farbmetrik (Z):"),
            dcc.Dropdown(
                id="z-metric-dropdown",
                options=[{"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()],
                value="slope",
                clearable=False
            ),
            
            html.Br(),
            
            html.Label("Größenmetrik (Bubble Size):"),
            dcc.Dropdown(
                id="size-metric-dropdown",
                options=[{"label": info["metric_en"], "value": key} for key, info in METRIC_INFO.items()],
                value="intercept",  # Standardwert
                clearable=False
            )
        ], style={"flex": "1"}, className="sidebar-dropdown-group"),

        # Grafik
        html.Div([
            html.Div([
                html.Div([
                    html.Label("Analyse links:"),
                    dcc.Dropdown(
                        id="scatter-label-1-dropdown",
                        options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                        value="ERA5",
                        clearable=False
                    )
                ], style={"flex": "1"}),

                html.Div([
                    html.Label("Analyse rechts:"),
                    dcc.Dropdown(
                        id="scatter-label-2-dropdown",
                        options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                        value="MERRA2",
                        clearable=False
                    )
                ], style={"flex": "1"})
            ], style={"display": "flex"}, className="plot-dropdown-container"),

            html.Div([
                dcc.Loading(
                    id="model-scatter-loading",
                    type="circle",
                    children=dcc.Graph(id="modell-scatterplot")
                )
            ], className="plot-container")

        ], style={"flex": "5"})
    ], className="centered-flex-row"),

    # --- Korrelationsmatrix ---
    html.H3("Korrelationsmatrix der Modellmetriken", className="home-subtitle mt-40"),

    html.P("""
        Die untenstehenden Heatmaps zeigen die Korrelationen zwischen den zentralen Modellkennzahlen. 
        So lässt sich auf einen Blick erkennen, welche Metriken miteinander zusammenhängen – beispielsweise, 
        ob ein hoher R²-Wert mit geringer Unsicherheit oder hohem AEP korreliert.
    """, className="home-paragraph"),

    html.P("""
        Der direkte Vergleich zweier Analysen ermöglicht zusätzlich eine Einschätzung, 
        ob sich bestimmte Korrelationen auf spezifische Datenquellen beschränken oder in beiden Fällen auftreten.
    """, className="home-paragraph mb-40"),

    html.Div([
        html.Div([
            html.Label("Analyse links:"),
            dcc.Dropdown(
                id="corr-left-label-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="ERA5"
            )
        ], style={"flex": "1"}),

        html.Div([
            html.Label("Analyse rechts:"),
            dcc.Dropdown(
                id="corr-right-label-dropdown",
                options=[{"label": label, "value": label} for label in DATAFRAMES.keys()],
                value="MERRA2"
            )
        ], style={"flex": "1"})
    ], style={"display": "flex"}, className="plot-dropdown-container"),

    html.Div([
        dcc.Loading(
            type="circle",
            children=dcc.Graph(id="correlation-matrix")
        )
    ], className="plot-container")

], className="main-content")