from dash import dcc, html
from data.config import DATAFRAMES
from utils.plot_utils import get_aep_compare_plots, get_aep_analysis_plot
from utils.compute_stats import get_aep_stats, filter_dataframes_by_labels

tab_core_layout = html.Div([
    html.H2("📈 Zentrale Ergebnisse"),
        
    # Barplotbereich
    html.Div([
        dcc.Graph(
            id="aep-barplot",
            figure=get_aep_compare_plots(get_aep_stats(DATAFRAMES), DATAFRAMES),
        )
    ], className="plot-container"),
    
    html.Div([
        html.H3("AEP-Unsicherheitsanalyse"),
        
        dcc.Dropdown(
            id="mc-dropdown",
            options=[
                {"label":"ERA5", "value":"ERA5"},
                {"label":"MERRA2", "value":"MERRA2"},
                {"label":"Kombiniert", "value":"Kombiniert"},
                {"label":"ERA5 gefiltert", "value":"ERA5 gefiltert"},
                {"label": "MERRA2 gefiltert", "value": "MERRA2 gefiltert"},
            ],
            value=["ERA5"],
            clearable=False,
            multi=True
        ),
        
        html.Div([  # ← Wrapper mit className
            dcc.Loading(
                id="aep-analysis-loading",
                type="circle",
                fullscreen=False,
                children=dcc.Graph(id="aep-analysis-plot")
            )
        ], className="plot-container")  # ← hier anwenden
        
    ], style={"padding":"20px"})
], className="content-wrapper")