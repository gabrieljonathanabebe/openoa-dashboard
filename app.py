import dash
from dash import html, dcc, Input, Output

import callbacks.core
import callbacks.lt
import callbacks.por
import callbacks.reg
import callbacks.ui

from layout.layout01_home import home_layout
from layout.layout02_data import data_layout
from layout.layout03_core import core_layout
from layout.layout04_lt import lt_layout
from layout.layout05_reg import reg_layout
from layout.layout06_por import por_layout
from layout.layout07_glossary import glossary_layout

# --- Dash-Initialisierung ---
external_stylesheets = [
    "/assets/styles.css",
    "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
]

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets
)

# --- Layout-Struktur ---
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="theme-store", storage_type="local", data="dark"),
    dcc.Interval(id="clock-interval", interval=60 * 1000, n_intervals=0),

    # --- Header ---
    html.Div([
        html.Div([
            html.I(
                className="fas fa-chart-bar",
                style={"marginRight": "8px"}
            ),
            "Windpark-Dashboard"
        ], style={
            "fontWeight": "bold",
            "fontSize": "20px",
            "display": "flex",
            "alignItems": "center"
        }),

        html.Div([
            html.Div([
                dcc.Input(
                    id="search-input",
                    placeholder="Suchen...",
                    style={
                        "padding": "10px",
                        "width": "250px",
                        "fontSize": "16px",
                        "borderRadius": "8px"
                    }
                ),
                html.Ul(
                    id="search-suggestions",
                    className="search-suggestions"
                )
            ], style={
                "position": "relative",
                "marginRight": "10px"
            }),

            html.I(
                className="fas fa-search",
                style={
                    "fontSize": "20px",
                    "marginRight": "15px"
                }
            ),
            html.I(
                id="theme-toggle",
                className="fas fa-sun",
                style={
                    "fontSize": "20px",
                    "cursor": "pointer",
                    "marginRight": "15px"
                }
            ),
            html.Div(
                id="current-time",
                className="current-time",
                style={
                    "fontSize": "16px",
                    "minWidth": "110px"
                }
            )
        ], style={
            "display": "flex",
            "alignItems": "center"
        })
    ], className="sticky-header"),

    # --- Hauptbereich: Sidebar + Inhalt ---
    html.Div([
        # --- Sidebar ---
        html.Div([
            html.Div([
                html.I(className="fas fa-compass", style={"marginRight": "8px"}),
                html.Span("Navigation")
            ], className="sidebar-header"),

            html.Div([
                html.I(className="fas fa-home", style={"marginRight": "8px"}),
                html.Span("Allgemein")
            ], className="sidebar-category"),
            dcc.Link("Projekt", href="/", id="link-home", className="sidebar-link"),

            html.Div([
                html.I(className="fas fa-database", style={"marginRight": "8px"}),
                html.Span("Datenquellen")
            ], className="sidebar-category"),
            dcc.Link("Reanalyse & Energie", href="/data", id="link-data", className="sidebar-link"),

            html.Div([
                html.I(className="fas fa-chart-line", style={"marginRight": "8px"}),
                html.Span("Ergebnisse")
            ], className="sidebar-category"),
            dcc.Link("Zentrale Ergebnisse", href="/core", id="link-core", className="sidebar-link"),
            dcc.Link("Langzeitanalyse", href="/lt", id="link-lt", className="sidebar-link"),
            dcc.Link("Modellgüte", href="/reg", id="link-reg", className="sidebar-link"),
            dcc.Link("POR-Analyse", href="/por", id="link-por", className="sidebar-link"),

            html.Div([
                html.I(className="fas fa-book", style={"marginRight": "8px"}),
                html.Span("Glossar")
            ], className="sidebar-category"),
            dcc.Link("Begriffe", href="/glossary", id="link-glossary", className="sidebar-link"),

            html.Div([
                html.A(
                    html.I(className="fab fa-github"),
                    href="https://github.com/gabrieljonathanabebe",
                    target="_blank",
                    className="social-icon"
                ),
                html.A(
                    html.I(className="fab fa-linkedin"),
                    href="https://www.linkedin.com/in/gabriel-jonathan-abebe-781b92316/",
                    target="_blank",
                    className="social-icon"
                ),
                html.A(
                    html.I(className="fas fa-envelope"),
                    href="mailto:jonathanabebe@outlook.de",
                    className="social-icon"
                ),
            ], className="sidebar-social")
        ], className="sidebar"),

        # --- Seiteninhalt ---
        html.Div([
            html.Div(id="page-content", className="main-content")
        ], className="scroll-wrapper")
    ], className="layout-container")
])

# --- Seitenrouting ---
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/data":
        return data_layout
    elif pathname == "/core":
        return core_layout
    elif pathname == "/lt":
        return lt_layout
    elif pathname == "/reg":
        return reg_layout
    elif pathname == "/por":
        return por_layout
    elif pathname == "/glossary":
        return glossary_layout
    else:
        return home_layout

# --- Sidebar-Link Highlighting ---
@app.callback(
    Output("link-home", "className"),
    Output("link-data", "className"),
    Output("link-core", "className"),
    Output("link-lt", "className"),
    Output("link-reg", "className"),
    Output("link-por", "className"),
    Output("link-glossary", "className"),
    Input("url", "pathname")
)
def highlight_active_link(pathname):
    def get_class(link_path):
        return "sidebar-link selected" if pathname == link_path else "sidebar-link"

    return (
        get_class("/"),
        get_class("/data"),
        get_class("/core"),
        get_class("/lt"),
        get_class("/reg"),
        get_class("/por"),
        get_class("/glossary")
    )

# --- App starten ---
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8051))
    app.run(debug=False, host="0.0.0.0", port=port)
    
    