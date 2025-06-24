import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.compute_stats import (
    compute_mean, 
    compute_lt_metrics, 
    filter_lt_data,
    get_iteration
)

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



def plot_reanalysis_timeseries(era5_ts, merra2_ts):
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
        title=dict(
            text="Rollierender 12-Monatsmittelwert",
            x=0.5,
            font=dict(size=16)
        ),
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






def plot_aep_comparison(stats, dataframes):
    fig = make_subplots(
        rows=2, cols=3,
        specs=[
            [{"type":"bar"}, {"type":"bar"}, {"type":"box"}],
            [{"colspan":2, "type":"scatter"}, None, {"type":"violin"}]
        ],
        subplot_titles=[
            "Mittelwert (GWh/yr)", "Unsicherheit (CV)", "Boxplots",
            "Jitterplot", "Violinplots"
        ],
        vertical_spacing=0.1,
        row_heights=[0.45, 0.55],
        column_widths=[0.25, 0.25, 0.5]
    )    
    colors = [COLOR_MAP.get(label, "gray") for label in stats["labels"]]
    
    fig.add_trace(
        go.Bar(
            x=stats["labels"],
            y=stats["mean_aep"],
            marker_color = colors,
            text=[f"{v:.2f}" for v in stats["mean_aep"]],
            textfont=dict(color=colors),
            textposition="outside",
            showlegend=False
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=stats["labels"],
            y=stats["aep_cv"],
            marker_color = colors,
            text=[f"{v:.2%}" for v in stats["aep_cv"]],
            textfont=dict(color=colors),
            textposition="outside",
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
            text="Prognosebandbreite der AEP",
            x=0.5,
            font=dict(size=16)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            title=dict(text=None),  # <- KEIN 'x' hier
            font=dict(size=12)
        )
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(range=[0, max(stats["mean_aep"]) * 1.2], row=1, col=1)
    fig.update_yaxes(range=[0, max(stats["aep_cv"]) * 1.2], row=1, col=2)
    
    apply_dark_mode_colors(fig)
    
        # Entferne X-Tick-Labels bei allen Subplots
    for row in [1, 2]:
        for col in [1, 2, 3]:
            try:
                fig.update_xaxes(showticklabels=False, row=row, col=col)
            except Exception:
                pass  # Falls ein Plot (z. B. col 2 unten) leer ist
    
    return fig



def plot_core_aep_iteration_analysis(filtered_dfs, metric = "aep_final"):
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{}, {}], [{"colspan":2}, None]],
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
            font=dict(size=16)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
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


def plot_lt_energy_evolution(dataframes, selected_labels, column="energy"):
    title_left = "LT-Bruttoenergie" if column == "energy" else "LT-Wind"
    title_right = "IAV-Energie" if column == "energy" else "IAV-Wind"
    
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
        title=dict(
            text="LT-Entwicklung",
            x=0.5,
            font=dict(size=16)
        ),
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



def plot_lt_energy_slope_comparison(left_df, right_df, selected_years, left_label, right_label):
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
        title=dict(
            text="Einfluss der Steigung auf die LT-Energie in Abhängigkeit der Windressourcen",
            x=0.5,
            font=dict(size=16)
        ),
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


def plot_reg_model_distribution(df1, df2, metric, label1, label2):
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
        title=dict(
            text=f"Verteilung der Modellgüte: {METRIC_INFO[metric]['metric_en']}",
            x=0.5,
            font=dict(size=16)
        ),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        xaxis=dict(title=METRIC_INFO[metric]["metric_en"]),
        yaxis=dict(title="Frequency"),
        yaxis2=dict(title=METRIC_INFO[metric]["metric_en"]),
    )
    
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    
    apply_dark_mode_colors(fig)
    
    return fig


def plot_reg_model_metric_scatter(df1, df2, x_metric, y_metric, z_metric, label1, label2):
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
                        text=f"{METRIC_INFO[z_metric]['metric_en']}",
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
        title=dict(
            text=f"Zusammenhang zwischen {METRIC_INFO[x_metric]['metric_en']}, {METRIC_INFO[y_metric]['metric_en']} und {METRIC_INFO[z_metric]['metric_en']}",
            x=0.5,
            font=dict(size=16)
        ),
        xaxis=dict(title=METRIC_INFO[x_metric]["metric_en"], range=[x_min, x_max]), 
        xaxis2=dict(title=METRIC_INFO[x_metric]["metric_en"], range=[x_min, x_max]),
        yaxis=dict(title=METRIC_INFO[y_metric]["metric_en"], range=[y_min, y_max]),
        yaxis2=dict(title=METRIC_INFO[y_metric]["metric_en"], range=[y_min, y_max]),
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    
    
    apply_dark_mode_colors(fig)
    
    return fig


def plot_reg_model_correlation_matrix(left_df, right_df, title_left, title_right, metrics):
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
        title_x=0.5,
    )
    
    fig.update_yaxes(showticklabels=False, row=1, col=2)

    apply_dark_mode_colors(fig)
    return fig


def plot_por_energy_distribution(df1, df2, label1, label2, observed_value, options):
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
            font=dict(size=16)
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





# Regressionsplot
def plot_por_regression_analysis(df1, df2, metric, value, label1, label2):
    # Hilfsfunktion für Punkte
    def add_trace(fig, df, source, color, symbol, name, row=1, col=1, showlegend=True):
        filtered = df[df["source"] == source]
        fig.add_trace(
            go.Scatter(
                x=filtered["wind_speed"],
                y=filtered["energy"],
                mode="markers",
                marker=dict(color=color, symbol=symbol, size=7),
                name=name,
                showlegend=showlegend
            ),
            row=row, col=col
        )

    # Iterationen bestimmen
    iter1 = get_iteration(df1, metric, method=value)
    iter2 = get_iteration(df2, metric, method=value)

    df1_filtered = df1[df1["iteration"] == iter1]
    df2_filtered = df2[df2["iteration"] == iter2]

    # Axis-Limits
    x_min, x_max = get_global_axis_range("wind_speed", df1_filtered, df2_filtered)
    y_min, y_max = get_global_axis_range("energy", df1_filtered, df2_filtered)

    # Plot initialisieren
    fig = make_subplots(rows=1, cols=2, subplot_titles=[label1, label2], horizontal_spacing=0.05)

    # Scatterpunkte & Regressionslinie – links
    add_trace(fig, df1_filtered, "bootstrap", "green", "circle", "Bootstrap", col=1, showlegend=True)
    add_trace(fig, df1_filtered, "non-bootstrap", "red", "x", "Non-Bootstrap", col=1, showlegend=True)

    slope1 = df1_filtered["slope"].iloc[0]
    intercept1 = df1_filtered["intercept"].iloc[0]
    x_vals1 = np.linspace(x_min, x_max, 100)
    y_vals1 = slope1 * x_vals1 + intercept1

    fig.add_trace(
        go.Scatter(
            x=x_vals1,
            y=y_vals1,
            mode="lines",
            line=dict(color="green", dash="dash"),
            name="",  # wichtig!
            showlegend=False
        ),
        row=1, col=1
    )

    # Scatterpunkte & Regressionslinie – rechts
    add_trace(fig, df2_filtered, "bootstrap", "green", "circle", "Bootstrap", col=2, showlegend=False)
    add_trace(fig, df2_filtered, "non-bootstrap", "red", "x", "Non-Bootstrap", col=2, showlegend=False)

    slope2 = df2_filtered["slope"].iloc[0]
    intercept2 = df2_filtered["intercept"].iloc[0]
    x_vals2 = np.linspace(x_min, x_max, 100)
    y_vals2 = slope2 * x_vals2 + intercept2

    fig.add_trace(
        go.Scatter(
            x=x_vals2,
            y=y_vals2,
            mode="lines",
            line=dict(color="green", dash="dash"),
            name="",
            showlegend=False
        ),
        row=1, col=2
    )

    # Annotations für Metriken
    metrics1 = f"y = {slope1:.3f}x {intercept1:.2f}<br>" \
               f"R² = {df1_filtered['r2'].iloc[0]:.2f}<br>" \
               f"MSE = {df1_filtered['mse'].iloc[0]:.3f}<br>" \
               f"Bias = {df1_filtered['yearly_bias'].iloc[0]:.3f}"

    metrics2 = f"y = {slope2:.3f}x {intercept2:.2f}<br>" \
               f"R² = {df2_filtered['r2'].iloc[0]:.2f}<br>" \
               f"MSE = {df2_filtered['mse'].iloc[0]:.3f}<br>" \
               f"Bias = {df2_filtered['yearly_bias'].iloc[0]:.3f}"


    fig.add_annotation(
        text=metrics1,
        xref="paper", yref="paper",
        x=0.02, y=0.95,
        showarrow=False,
        align="left",
        font=dict(color="white", size=12),
        bgcolor="rgba(0,0,0,0)"
    )

    fig.add_annotation(
        text=metrics2,
        xref="paper", yref="paper",
        x=0.60, y=0.95,
        showarrow=False,
        align="left",
        font=dict(color="white", size=12),
        bgcolor="rgba(0,0,0,0)"
    )

    # Layout
    fig.update_layout(
        height=450,
        title=dict(
            text="Regressionplots einer ausgewählten Iteration",
            x=0.5,
            font=dict(size=16)
        ),
        xaxis=dict(title="POR-Windspeed (m/s)"),
        yaxis=dict(title="POR-Gross-Energy (GWh/m)"),
        xaxis2=dict(title="POR-Windspeed (m/s)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True, range=[x_min, x_max])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True, range=[y_min, y_max])

    apply_dark_mode_colors(fig)
    return fig



def plot_por_energy_timeseries(df_dict, selected_labels, metric="r2", method="max"):
    fig = go.Figure()

    for label in selected_labels:
        df_label = df_dict[label]  # <-- hier wird's richtig gemacht

        # Beste Iteration finden
        best_iter = get_iteration(df_label, metric, method)
        df_iter = df_label[df_label["iteration"] == best_iter].copy().sort_values("time")

        fig.add_trace(go.Scatter(
            x=df_iter["time"],
            y=df_iter["pred_energy"],
            mode="lines+markers",
            name=f"{label} (modelliert)",
            line=dict(color=COLOR_MAP.get(label, "gray"), width=2),
            marker=dict(size=6)
        ))

    # Referenzlinie (nur einmal)
    any_df = list(df_dict.values())[0]
    ref = (
        any_df.groupby("time", as_index=False)["gross_energy_gwh"]
        .first()
        .sort_values("time")
    )

    fig.add_trace(go.Scatter(
        x=ref["time"],
        y=ref["gross_energy_gwh"],
        mode="lines+markers",
        name="Beobachtete Energie (Referenz)",
        line=dict(color="white", width=2, dash="dot"),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=dict(
            text="Zeitreihe der modellierten monatlichen Energie im POR-Zeitraum",
            x=0.5,
            font=dict(size=16)
        ),
        height=450,
        xaxis=dict(
            title="Monat",
            rangeslider=dict(visible=True),
            type="date"  # optional, sorgt für saubere Achsen-Skalierung
        ),
        yaxis_title="Energie (GWh)",
        legend=dict(orientation="h", y=-0.8, x=0.5, xanchor="center")
    )
    

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

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


def break_label(text, threshold=10):
    if len(text) > threshold:
        return text.replace(" ", "<br>", 1)  # Nur erstes Leerzeichen umbrechen
    return text




