import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.compute_stats import compute_mean, compute_lt_metrics, filter_lt_data

from data.config import COLOR_MAP, METRIC_INFO


def add_mean_x_line(fig, x_vals, y_vals, row=None, col=None,color="#FF1493", name="Mittelwert X"):
    mean_x = compute_mean(x_vals)
    
    trace = go.Scatter(
        x=[mean_x, mean_x],
        y=[y_vals.min(), y_vals.max()],
        mode="lines",
        name=name,
        line=dict(
            color=color,
            dash="dash",
            width=2
        )
    )
    
    if row is not None and col is not None:
        fig.add_trace(trace, row=row, col=col)
    else:
        fig.add_trace(trace)
    return fig


def add_mean_y_line(fig, x_vals, y_vals, row=None, col=None, color="#FF1493", name="Mittelwert Y"):
    mean_y = compute_mean(y_vals)
    
    trace = go.Scatter(
        x=[x_vals.min(), x_vals.max()],
        y=[mean_y, mean_y],
        mode="lines",
        name=name,
        line=dict(
            color=color,
            dash="dot",
            width=2
        )
    )
    
    if row is not None and col is not None:
        fig.add_trace(trace, row=row, col=col)
    else:
        fig.add_trace(trace)
    return fig



def get_time_series_plot(era5_ts, merra2_ts):
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=era5_ts["Date"],
            y=era5_ts["norm"],
            name="ERA5",
            mode="lines",
            line=dict(width=1.5, color=COLOR_MAP["ERA5"])
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=merra2_ts["Date"],
            y=merra2_ts["norm"],
            name="MERRA2",
            mode="lines",
            line=dict(width=1.5, color=COLOR_MAP["MERRA2"])
        )
    )
    
    fig.update_layout(
        height = 500,
        showlegend=True,
        xaxis=dict(
            title="Jahr",
            rangeslider=dict(visible=True),
            type="date"  # optional, sorgt für saubere Achsen-Skalierung
        ),
        yaxis=dict(
            title="Normierte Windgeschwindigkeit"
        )
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    apply_dark_mode_colors(fig)
    
    return fig



def get_aep_compare_plots(stats, dataframes):
    fig = make_subplots(
        rows=2, cols=3,
        specs=[
            [{"type":"bar"}, {"type":"bar"}, {"type":"box"}],
            [{"colspan":2, "type":"scatter"}, None, {"type":"violin"}]
        ],
        subplot_titles=[
            "Mittelwert", "Unsicherheit(CV)", "Boxplots",
            "Jitterplot", "Violinplots"
        ],
        vertical_spacing=0.15,
        row_heights=[0.45, 0.55],
        column_widths=[0.25, 0.25, 0.5]
    )    
    colors = [COLOR_MAP.get(label, "gray") for label in stats["labels"]]
    
    fig.add_trace(
        go.Bar(
            x=stats["labels"],
            y=stats["mean_aep"],
            marker_color = colors,
            showlegend=False
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=stats["labels"],
            y=stats["aep_cv"],
            marker_color = colors,
            showlegend=False
        ),
        row=1, col=2
    )
    
    for label in stats["labels"]:
        fig.add_trace(
            go.Box(
                y=dataframes[label]["aep_final"],
                name=label,
                marker=dict(
                    color=COLOR_MAP.get(label, "grey"),
                    symbol="x",
                    size=6
                ),
                boxpoints="outliers",
                line=dict(width=0.5),
                marker_color=COLOR_MAP.get(label, "grey"),
                boxmean=True
            ),
            row=1, col=3
        )
        
    jittered_x = []
    jittered_y = []
    jittered_labels = []
    
    for i, label in enumerate(stats["labels"]):
        x_jitter = np.random.normal(loc=i, scale=0.1, size=len(dataframes[label]))
        jittered_x.extend(x_jitter)
        jittered_y.extend(dataframes[label]["aep_final"])
        jittered_labels.extend([label] * len(dataframes[label]))
        
    fig.add_trace(
        go.Scatter(
            x=jittered_x,
            y=jittered_y,
            mode="markers",
            showlegend=False,
            marker=dict(
                color=[COLOR_MAP.get(l, "gray") for l in jittered_labels],
                size=4,
                opacity=0.5
            )
        ),
        row=2, col=1
    )
    
    for label in stats["labels"]:
        fig.add_trace(
            go.Violin(
                y=dataframes[label]["aep_final"],
                name=label,
                line_color=COLOR_MAP.get(label, "gray"),
                box_visible=True,
                meanline_visible=True,
                showlegend=False
            ),
            row=2, col=3
        )   
    
    fig.update_layout(
        height = 750,
        showlegend=True,
        title=dict(
            text="Unsicherheitsanalyse der AEP",
            x=0.5,
            font=dict(size=20)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            title=dict(text=None),  # <- KEIN 'x' hier
            font=dict(size=12)
        )
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    apply_dark_mode_colors(fig)
    
        # Entferne X-Tick-Labels bei allen Subplots
    for row in [1, 2]:
        for col in [1, 2, 3]:
            try:
                fig.update_xaxes(showticklabels=False, row=row, col=col)
            except Exception:
                pass  # Falls ein Plot (z. B. col 2 unten) leer ist
    
    return fig



def get_aep_analysis_plot(filtered_dfs, metric = "aep_final"):
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{}, {}], [{"colspan":2}, None]],
        subplot_titles=["Histogramm", "AEP vs. IAV-Faktor", "AEP je Iteration"],
        vertical_spacing=0.1,
        row_heights=[0.5, 0.5]        
    )
    
    for label, df in filtered_dfs.items():
        # Histogramm (oben links)
        fig.add_trace(
            go.Histogram(
                x=df[metric],
                name=label,
                marker=dict(color=COLOR_MAP.get(label, "white")),
                opacity=0.6,
                nbinsx=100,
                showlegend=False
            ),
            row=1, col=1
        )
        #Scatterplot (oben rechts)
        fig.add_trace(
            go.Scatter(
                x=df["iav_nsim"],
                y=df[metric],
                name=label,
                mode="markers",
                showlegend=False,
                marker=dict(
                    color="rgba(0,0,0,0)",  # Keine Füllung
                    size=6,
                    opacity=0.6,
                    line=dict(
                        color=COLOR_MAP.get(label, "white"),  # Randfarbe
                        width=1.5
                    )
                )
            ),
            row=1, col=2
        )      
        #Linienplot unten über die gesamte Breite
        fig.add_trace(
            go.Scatter(
                x=df["i"],
                y=df[metric],
                name=label,
                mode="lines",
                showlegend=False,
                line=dict(color=COLOR_MAP.get(label, "white"), width=0.5),
                opacity=0.2
            ),
            row=2, col=1
        )
        
        rolling = df[metric].rolling(window=50, center=True).mean()

        # Linienplot unten über die gesamte Breite (Rolling Mean)
        fig.add_trace(
            go.Scatter(
                x=df["i"],
                y=rolling,
                name=label,
                mode="lines",
                line=dict(color=COLOR_MAP.get(label, "white"), dash="dot", width=2),
                showlegend=True,
            ),
            row=2, col=1
        )
    #Layouteinstellungen
    fig.update_layout(
        height = 750,
        title=dict(
            text="Iterationsspezifische Analyse der AEP",
            x=0.5,
            font=dict(size=20)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            title=None,
            font=dict(size=12)
        ),
        barmode="overlay",
        xaxis=dict(title=METRIC_INFO[metric]["metric_en"]),
        yaxis=dict(title="Frequency"),
        xaxis2=dict(title="IAV-Factor"),
        yaxis2=dict(title=METRIC_INFO[metric]["metric_en"]),
        xaxis3=dict(title="Iteration"),
        yaxis3=dict(title=METRIC_INFO[metric]["metric_en"]),
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    apply_dark_mode_colors(fig)
    
    return fig


def get_lt_evolution_plot(dataframes, selected_labels, column="energy"):
    title_left = "Entwicklung LT-Bruttoenergie" if column == "energy" else "Entwicklung LT-Wind"
    title_right = "Entwicklung IAV-Energie" if column == "energy" else "Entwicklung IAV-Wind"
    
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[title_left, title_right],
        shared_xaxes=False
    )
    
    for label in selected_labels:
        df = dataframes[label]
        years, non_cum_mean, cum_mean, cum_cv = compute_lt_metrics(df, column=column)
        # Links: kumulierter Mittelwert (Vordergrund)
        fig.add_trace(
            go.Scatter(
                x=years ,
                y=cum_mean,
                mode="lines",
                name=label,
                hovertemplate=(
                    "Jahr: %{x}<br>" +
                    "Energie (kumuliert): %{y:.2f} GWh/yr"
                ),                
                line=dict(color=COLOR_MAP.get(label, "gray"))
            ),
            row=1, col=1
        )
        # Links: nicht kumulierter Mittelwert (Hintergrund)
        fig.add_trace(
            go.Scatter(
                x=years ,
                y=non_cum_mean,
                mode="lines",
                name=label,
                hovertemplate=(
                    "Jahr: %{x}<br>" +
                    "Energie: %{y:.2f} GWh/yr"
                ),
                opacity=0.5,
                line=dict(color=COLOR_MAP.get(label, "gray"), dash="dot"),
                showlegend=False
            ),
            row=1, col=1
        )
        # Rechts: Kumulierte IAV
        fig.add_trace(
            go.Scatter(
                x=years,
                y=cum_cv,
                mode="lines",
                name=label,
                hovertemplate=(
                    "Jahr: %{x}<br>" +
                    "IAV: %{y:.2f} %"
                ),
                line=dict(color=COLOR_MAP.get(label, "gray"))
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        height = 500,
        showlegend=False,
        xaxis=dict(title="Jahr"),
        yaxis=dict(title="LT-Energy (GWh/yr)" if column == "energy" else "Average LT-Windspeed (m/s)"),
        xaxis2=dict(title="Jahr"),
        yaxis2=dict(title="IAV-Energy (%)" if column == "energy" else"IAV-Wind (%)") 
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    
    apply_dark_mode_colors(fig)
    
    return fig



def get_slope_energy_plot(left_df, right_df, selected_years, left_label, right_label):
    # Daten filtern:
    left_filtered = filter_lt_data(left_df, selected_years)
    right_filtered = filter_lt_data(right_df, selected_years)
    
    x_min, x_max = get_global_axis_range("slope", left_filtered, right_filtered)
    color_min, color_max = get_global_color_scale_bounds("wind", left_filtered, right_filtered)
    
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[
            f"{left_label}",
            f"{right_label}"
        ],
        shared_xaxes=True,
        shared_yaxes=True
    )
    # Linker Subplot
    fig.add_trace(
        go.Scatter(
            x=left_filtered["slope"],
            y=left_filtered["energy"],
            mode="markers",
            marker=dict(
                color=left_filtered["wind"],
                colorscale="RdBu",
                cmin=color_min,
                cmax=color_max,
                colorbar=dict(
                    title=dict(
                        text="Average LT-Windspeed (m/s)",
                        side="right"   # ← vertikal anzeigen
                    )
                ),
                showscale=True,
                size=5,
                line=dict(
                    color="rgba(255,255,255,0.4)",
                    width=0.2
                )
            ),
            name=left_label,
            customdata=np.stack((left_filtered["year"],), axis=-1),
            hovertemplate=(
                "Jahr: %{customdata[0]}<br>" +
                "Steigung: %{x:.3f} GWh/(m/s)<br>" +
                "Energie: %{y:.2f} GWh/yr<br>" +
                "Wind: %{marker.color:.2f} m/s<br>" +
                "<extra></extra>"
            ),
            showlegend=False
        ),
        row=1, col=1
    )
    # Rechter Subplot
    fig.add_trace(
        go.Scatter(
            x=right_filtered["slope"],
            y=right_filtered["energy"],
            mode="markers",
            marker=dict(
                color=right_filtered["wind"],
                colorscale="RdBu",                
                showscale=False,
                size=5,    
                line=dict(             # <- Randfarbe und Dicke
                    color="rgba(255,255,255,0.5)",  # z. B. halbtransparent weiß
                    width=0.2
                )
            ),
            name=right_label,
            customdata=np.stack((right_filtered["year"],), axis=-1),
            hovertemplate=(
                "Jahr: %{customdata[0]}<br>" +
                "Steigung: %{x:.3f} GWh/(m/s)<br>" +
                "Energie: %{y:.2f} GWh/yr<br>" +
                "Wind: %{marker.color:.2f} m/s<br>" +
                "<extra></extra>"
            ),
            showlegend=False
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height = 500,
        showlegend=False,
        xaxis=dict(title="Slope (GWh/ (m/s))", range=[x_min, x_max]),        
        yaxis=dict(title="LT-Energy (GWh/yr)"),
        xaxis2=dict(title="Slope (GWh/ (m/s))", range=[x_min, x_max]),
        yaxis2=dict(title="LT-Energy (GWh/yr)")
    )
    
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    apply_dark_mode_colors(fig)
    
    return fig


def get_model_comparison_plot(df1, df2, metric, label1, label2):
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Histogramm", "Split-Violinplot"],
        specs=[[{"type":"histogram"}, {"type":"violin"}]],
        column_widths=[0.5, 0.5],
    )
    for df, label, color, side in zip(
            [df1, df2],
            [label1, label2],
            [COLOR_MAP.get(label1,"gray"), COLOR_MAP.get(label2,"gray")],
            ["negative", "positive"]   
    ):  # Histogramm
        fig.add_trace(
            go.Histogram(
                x=df[metric],
                name=label,
                opacity=0.6,
                marker_color=color,
                showlegend=False
            ),
            row=1, col=1
        )
        # Violinplot
        fig.add_trace(
            go.Violin(
                y=df[metric],
                x=["Vergleich"] * len(df),
                side=side,
                name=label,
                line_color=color,
                fillcolor=color,
                opacity=0.7,
                meanline_visible=True,
                showlegend=True,
                points="all"
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        height = 500,
        barmode="overlay",
        violinmode="overlay",
        title=f"Verteilung der Modellgüte: {metric}",
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        xaxis=dict(title=METRIC_INFO[metric]["metric_en"]),
        yaxis=dict(title="Frequency"),
        yaxis2=dict(title=METRIC_INFO[metric]["metric_en"]),
    )
    
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    
    apply_dark_mode_colors(fig)
    
    return fig


def get_model_scatter_plot(df1, df2, x_metric, y_metric, z_metric, label1, label2):
    x_min, x_max = get_global_axis_range(x_metric, df1, df2)
    y_min, y_max = get_global_axis_range(y_metric, df1, df2)
    
    cmin, cmax = get_global_color_scale_bounds(z_metric, df1, df2)  
    
    fig = make_subplots(
        rows=1,
        cols=2,
        column_titles=[label1, label2],
        column_widths=[0.5, 0.5],
        shared_xaxes=True,
        shared_yaxes=True,
    )
    
    fig.add_trace(
        go.Scatter(
            x=df1[x_metric],
            y=df1[y_metric],
            mode="markers",
            name=label1,
            showlegend=False,
            marker=dict(
                size=5,
                color=df1[z_metric],
                colorscale = "RdYlGn",
                cmin=cmin,
                cmax=cmax,
                showscale=False,
                opacity=0.7
            ) 
        ),
        row=1, col=1  
    )
    
    fig.add_trace(
        go.Scatter(
            x=df2[x_metric],
            y=df2[y_metric],
            mode="markers",
            name=label2,
            showlegend=False,
            marker=dict(
                size=5,
                color=df2[z_metric],
                colorscale="RdYlGn",
                cmin=cmin,
                cmax=cmax,
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text=z_metric,
                        side="right"
                    )
                ),
                opacity=0.7
            )
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height = 450,
        title= f"Zusammenhang zwischen {x_metric}, {y_metric} und {z_metric}",
        xaxis=dict(title=METRIC_INFO[x_metric]["metric_en"], range=[x_min, x_max]), 
        xaxis2=dict(title=METRIC_INFO[x_metric]["metric_en"], range=[x_min, x_max]),
        yaxis=dict(title=METRIC_INFO[y_metric]["metric_en"], range=[y_min, y_max]),
        yaxis2=dict(title=METRIC_INFO[y_metric]["metric_en"], range=[y_min, y_max]),
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    
    apply_dark_mode_colors(fig)
    
    return fig


def get_por_hist_violin_plot(df1, df2, label1, label2, observed_value, options):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Histogramm", "Split-Violinplot"],
        specs=[[{"type": "histogram"}, {"type": "violin"}]],
        column_widths=[0.5, 0.5]
    )

    for df, label, color, side in zip(
            [df1, df2],
            [label1, label2],
            [COLOR_MAP.get(label1, "gray"), COLOR_MAP.get(label2, "gray")],
            ["negative", "positive"]
    ):
        gps_vals = df["gps"]
        mean_val = np.mean(gps_vals)

        # Beschriftung mit Mittelwert im Namen
        label_with_mean = f"{label} (μ={mean_val:.2f})"

        # Histogramm (ohne Legende)
        fig.add_trace(
            go.Histogram(
                x=gps_vals,
                name=label,  # Nur Legende im Violinplot zeigen
                marker_color=color,
                opacity=0.6,
                showlegend=False
            ),
            row=1, col=1
        )

        # Mittelwertlinie im Histogramm
        if "show-means" in options:
            fig.add_vline(
                x=mean_val,
                line=dict(color=color, dash="dash"),
                row=1, col=1
            )

        # Violinplot (Legende mit Mittelwert im Namen)
        fig.add_trace(
            go.Violin(
                y=gps_vals,
                x=["Vergleich"] * len(gps_vals),
                side=side,
                name=label_with_mean,  # ⬅️ Mittelwert in Legende
                line_color=color,
                fillcolor=color,
                opacity=0.7,
                points="all",
                meanline_visible=True,
                showlegend=True
            ),
            row=1, col=2
        )

        # Mittelwertlinie im Violinplot
        if "show-means" in options:
            fig.add_hline(
                y=mean_val,
                line=dict(color=color, dash="dash"),
                row=1, col=2
            )

        # Beobachtete Werte als Linien + Annotation
        if "show-observed" in options:
            # Histogramm: Vertikale Linie + Text
            fig.add_vline(
                x=observed_value,
                line=dict(color="white", dash="dash"),
                annotation_text=f"μ Beobachtet: {observed_value:.2f}",
                annotation_position="top left",
                annotation=dict(font=dict(color="white")),
                row=1, col=1
            )
        
            # Violinplot: Horizontale Linie + Text
            fig.add_hline(
                y=observed_value,
                line=dict(color="white", dash="dash"),
                annotation_text=f"μ Beobachtet: {observed_value:.2f}",
                annotation_position="top right",
                annotation=dict(font=dict(color="white")),
                row=1, col=2
            )

    fig.update_layout(
        height = 500,
        title=dict(
            text="Verteilung der modellierten Jahresenergie (GPS)",
            x=0.5,
            font=dict(size=20)
        ),
        barmode="overlay",
        violinmode="overlay",
        xaxis=dict(title=METRIC_INFO["gps"]["metric_en"]),
        yaxis=dict(title="Frequency"),
        yaxis2=dict(title=METRIC_INFO["gps"]["metric_en"]),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    

    apply_dark_mode_colors(fig)
    return fig


def get_correlation_matrices(left_df, right_df, title_left, title_right, metrics):
    def compute_corr(df):
        return df[metrics].corr()

    corr_left = compute_corr(left_df)
    corr_right = compute_corr(right_df)
    
    x_labels = [break_label(METRIC_INFO[m]["metric_en"]) for m in metrics]
    y_labels = [break_label(METRIC_INFO[m]["metric_en"]) for m in metrics]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[title_left, title_right],
        horizontal_spacing=0.05  # Standard ist 0.2
    )
    heatmap_kwargs = dict(
        zmin=-1,
        zmax=1,
        colorscale=[(0, "red"), (0.5, "white"), (1, "green")],
        colorbar=dict(title="Korrelation")
    )

    # Linke Matrix
    fig.add_trace(
        go.Heatmap(
            z=corr_left.values,
            x=x_labels,
            y=y_labels,
            text=[[f"{val:.2f}" for val in row] for row in corr_left.values],
            texttemplate="%{text}",
            **heatmap_kwargs
        ),
        row=1, col=1
    )

    # Rechte Matrix
    fig.add_trace(
        go.Heatmap(
            z=corr_right.values,
            x=x_labels,
            y=y_labels,
            text=[[f"{val:.2f}" for val in row] for row in corr_right.values],
            texttemplate="%{text}",
            **{**heatmap_kwargs, "showscale": False}  # zweite Skala ausblenden
        ),
        row=1, col=2
    )

    fig.update_layout(
        height = 500,
        title="Korrelationen zwischen Modellkoeffizienten",
        title_x=0.5
    )
    
    fig.update_yaxes(showticklabels=False, row=1, col=2)

    apply_dark_mode_colors(fig)
    return fig
        

def apply_dark_mode_colors(fig):
    layout_updates = {
        "plot_bgcolor": "#2c2c2c",
        "paper_bgcolor": "#2c2c2c",
        "font": dict(family="Roboto", color="white"),
        "legend": dict(font=dict(color="white")),
    }

    # Alle x- und y-Achsen anpassen
    for i in range(1, 10):  # falls mehr Subplots folgen
        layout_updates[f"xaxis{i}"] = dict(color="white", gridcolor="#444444")
        layout_updates[f"yaxis{i}"] = dict(color="white", gridcolor="#444444")

    # Fallback für einfache Layouts (z. B. fig = go.Figure())
    layout_updates["xaxis"] = dict(color="white", gridcolor="#444444")
    layout_updates["yaxis"] = dict(color="white", gridcolor="#444444")

    fig.update_layout(**layout_updates)
    return fig

def break_label(text, threshold=10):
    if len(text) > threshold:
        return text.replace(" ", "<br>", 1)  # Nur erstes Leerzeichen umbrechen
    return text




def get_global_axis_range(column, *dfs, padding_factor=0.05):
    all_values = pd.concat([df[column] for df in dfs])
    min_val = all_values.min()
    max_val = all_values.max()

    range_span = max_val - min_val
    padding = range_span * padding_factor

    return min_val - padding, max_val + padding


def get_global_color_scale_bounds(column, *dfs):
    all_values = pd.concat([df[column] for df in dfs])
    return all_values.min(), all_values.max()



