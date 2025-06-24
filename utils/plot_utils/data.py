import plotly.graph_objects as go
from utils.plot_utils.shared import apply_dark_mode_colors
from data.config import COLOR_MAP


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
        height=500,
        showlegend=True,
        title=dict(
            text="Rollierender 12-Monatsmittelwert",
            x=0.5,
            font=dict(size=16)
        ),
        xaxis=dict(
            title="Jahr",
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(
            title="Normierte Windgeschwindigkeit"
        )
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='gray', mirror=True)

    apply_dark_mode_colors(fig)

    return fig