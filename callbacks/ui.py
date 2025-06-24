from dash import callback, Output, Input, State, ALL, ctx
from dash import html
import dash
import datetime

from data.config import TAB_KEYWORDS, WEEKDAY_MAP, MONTH_MAP

# -------------------------------------
# Uhrzeit-Aktualisierung (jede Minute)
# -------------------------------------
@callback(
    Output("current-time", "children"),
    Input("clock-interval", "n_intervals")
)
def update_clock(n):
    now = datetime.datetime.now()
    weekday_de = WEEKDAY_MAP.get(now.strftime("%a"), now.strftime("%a"))
    month_de = MONTH_MAP.get(now.strftime("%B"), now.strftime("%B"))
    time = now.strftime("%H:%M")

    return f"{weekday_de} {now.day}. {month_de} {time}"


# -------------------------------------
# Suchvorschläge generieren
# -------------------------------------
@callback(
    Output("search-suggestions", "children"),
    Input("search-input", "value"),
    prevent_initial_call=True
)
def update_search_suggestions(query):
    if not query:
        return []

    query = query.lower()
    suggestions = []

    for tab_id, keywords in TAB_KEYWORDS.items():
        score = sum(1 for kw in keywords if query in kw.lower())
        if score > 0:
            suggestions.append((score, tab_id))

    suggestions.sort(reverse=True)

    tab_labels = {
        "tab-home": "Projekt",
        "tab-data": "Reanalyse und Energie",
        "tab-core": "Zentrale Ergebnisse",
        "tab-lt": "Langzeitanalyse",
        "tab-sensitivity": "Modellgüte",
        "tab-por": "POR-Analyse"
    }

    return [
        html.Div(
            tab_labels.get(tab_id, tab_id),
            id={"type": "suggestion", "tab": tab_id},
            className="search-suggestion-item",
            n_clicks=0
        )
        for _, tab_id in suggestions
    ]


# -------------------------------------
# Klick auf Suchvorschlag → Tab wechseln
# -------------------------------------
@callback(
    Output("main-tabs", "value"),
    Input({"type": "suggestion", "tab": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def switch_tab_by_click(n_clicks_list):
    if not ctx.triggered or all(n in [0, None] for n in n_clicks_list):
        return dash.no_update

    clicked = ctx.triggered_id
    return clicked["tab"]


# -------------------------------------
# Dark/Light Theme-Toggle (clientseitig über Dash)
# -------------------------------------


# Setzt das Theme im HTML-DOM
dash.clientside_callback(
    """
    function(theme) {
        if (theme) {
            document.documentElement.setAttribute("data-theme", theme);
            const icon = document.getElementById("theme-toggle");
            if (icon) {
                icon.classList.remove("fa-sun", "fa-moon");
                icon.classList.add(theme === "dark" ? "fa-sun" : "fa-moon");
            }
        }
        return "";
    }
    """,
    Output("theme-toggle", "title"),
    Input("theme-store", "data")
)

# Umschalten des Themes bei Klick auf das Icon
dash.clientside_callback(
    """
    function(n_clicks, current_theme) {
        if (!n_clicks) {
            return current_theme || "dark";
        }
        return current_theme === "dark" ? "light" : "dark";
    }
    """,
    Output("theme-store", "data"),
    Input("theme-toggle", "n_clicks"),
    State("theme-store", "data")
)



