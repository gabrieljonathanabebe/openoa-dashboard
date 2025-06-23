from dash import html

tab_glossary_layout = html.Div([
    html.H2([
        html.I(className="fas fa-scroll", style={"marginRight": "10px"}),
        "Glossar & Definitionen"
    ], className="home-title"),

    html.H3("Zentrale Begriffe der Analyse", className="home-subtitle"),

    html.P("""
        Im Folgenden werden die wichtigsten Begriffe und Kennzahlen erläutert, 
        die im Rahmen der Analyse und Visualisierung dieser Anwendung verwendet werden. 
        Die Definitionen dienen dem besseren Verständnis der dargestellten Inhalte.
    """, className="home-paragraph"),

    html.H4("AEP (Annual Energy Production)", className="glossary-term"),
    html.P("Die erwartete jährliche Energieproduktion eines Windparks. Sie dient als zentrale "
           "Größe für die Bewertung der Energieausbeute und wird im Rahmen der Simulationen geschätzt.",
           className="home-paragraph"),

    html.H4("Huber-Threshold", className="glossary-term"),
    html.P("Ein Schwellwert zur Erkennung und Abschwächung von Ausreißern in den Eingangsdaten. "
           "Werte außerhalb dieses Bereichs werden bei der Regressionsanalyse weniger gewichtet.",
           className="home-paragraph"),

    html.H4("Intercept", className="glossary-term"),
    html.P("Der Achsenabschnitt der Regressionsgeraden. Er zeigt an, welche Energieproduktion das Modell "
           "vorhersagt, wenn kein Windsignal vorhanden wäre.",
           className="home-paragraph"),

    html.H4("IAV (Interannual Variability)", className="glossary-term"),
    html.P("Die natürliche Schwankung des Windpotentials von Jahr zu Jahr. Sie beeinflusst die Unsicherheit "
           "in der langfristigen Energieprognose.",
           className="home-paragraph"),

    html.H4("IAV-Faktor", className="glossary-term"),
    html.P("Ein in der Monte-Carlo-Simulation zufällig gesampelter Faktor, mit dem die AEP modifiziert wird, "
           "um die Auswirkungen der interannuellen Variabilität zu berücksichtigen.",
           className="home-paragraph"),

    html.H4("Langzeit-Energie", className="glossary-term"),
    html.P("Die auf ein Jahr normalisierte Energieproduktion, basierend auf langjährigen Winddaten. "
           "Sie wird genutzt, um eine stabile Schätzung der erwarteten Produktion zu erhalten.",
           className="home-paragraph"),

    html.H4("LT-Wind (Long-Term Wind)", className="glossary-term"),
    html.P("Der jährlich gemittelte Windgeschwindigkeitswert aus den historischen Reanalyse-Daten. "
           "Er bildet die Basis für die Langzeitkorrektur.",
           className="home-paragraph"),

    html.H4("Monte-Carlo-Simulation", className="glossary-term"),
    html.P("Ein statistisches Verfahren, bei dem zufällige Kombinationen von Unsicherheiten wiederholt simuliert werden. "
           "Ziel ist es, robuste Aussagen über die Verteilung möglicher Ergebnisse zu treffen.",
           className="home-paragraph"),

    html.H4("MSE (Mean Squared Error)", className="glossary-term"),
    html.P("Ein Maß für die durchschnittliche quadratische Abweichung zwischen Modellvorhersagen und realen Werten. "
           "Niedrigere Werte deuten auf ein besseres Modell hin.",
           className="home-paragraph"),

    html.H4("POR (Period of Record)", className="glossary-term"),
    html.P("Der Zeitraum, für den tatsächliche Produktionsdaten des Windparks vorliegen. "
           "Er dient als Grundlage für die Modellierung und Validierung.",
           className="home-paragraph"),

    html.H4("Predicted POR-Gross Energy", className="glossary-term"),
    html.P("Die geschätzte Bruttoenergieproduktion im Zeitraum des POR. Wird für den Vergleich mit Messwerten verwendet.",
           className="home-paragraph"),

    html.H4("R² (Bestimmtheitsmaß)", className="glossary-term"),
    html.P("Ein statistisches Maß, das angibt, wie gut ein Modell die beobachteten Daten erklärt. "
           "Ein R²-Wert nahe 1 signalisiert eine gute Modellanpassung.",
           className="home-paragraph"),

    html.H4("Slope", className="glossary-term"),
    html.P("Die Steigung der Regressionslinie. Sie gibt an, wie stark sich die Energieproduktion mit dem "
           "Reanalyse-Windsignal verändert.",
           className="home-paragraph"),

    html.H4("Yearly Bias", className="glossary-term"),
    html.P("Die durchschnittliche Abweichung zwischen modellierten und gemessenen POR-Jahreserträgen. "
           "Ein Indikator für systematische Fehler im Modell.",
           className="home-paragraph"),

    html.H4("Variationskoeffizient (CV)", className="glossary-term"),
    html.P("Ein dimensionsloses Maß für die relative Streuung der AEP-Schätzungen. "
           "Er erlaubt den Vergleich von Unsicherheiten unabhängig von der absoluten Ertragshöhe.",
           className="home-paragraph"),
    
    html.Br(),

    html.P("""
        Weitere mathematische Formeln, ausführliche Prozessbeschreibungen sowie zusätzliche Begriffe 
        finden sich in der zugehörigen Bachelorarbeit. Dieses Glossar bietet lediglich eine kompakte Übersicht 
        der wichtigsten Elemente zur Orientierung innerhalb der Anwendung.
    """, className="home-paragraph")
], className="main-content")