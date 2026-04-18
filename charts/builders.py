import plotly.graph_objects as go
import pandas as pd


def build_price_chart(data: dict, symbols: list) -> go.Figure:
    fig = go.Figure()
    for symbol in symbols:
        df = data[symbol]
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name=symbol,
            hovertemplate="%{x|%d %b %Y}<br>R$ %{y:.2f}<extra>%{fullData.name}</extra>",
        ))
    fig.update_layout(
        title="Preço de Fechamento (R$)",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
        legend_title="Ação",
    )
    return fig


def build_performance_chart(data: dict, symbols: list) -> go.Figure:
    fig = go.Figure()
    for symbol in symbols:
        close = data[symbol]["Close"].dropna()
        if close.empty:
            continue
        pct_change = ((close / close.iloc[0]) * 100) - 100
        fig.add_trace(go.Scatter(
            x=pct_change.index,
            y=pct_change,
            mode="lines",
            name=symbol,
            hovertemplate="%{x|%d %b %Y}<br>%{y:+.2f}%<extra>%{fullData.name}</extra>",
        ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(
        title="Performance % vs Jan 2025",
        xaxis_title="Data",
        yaxis_title="Retorno (%)",
        hovermode="x unified",
        legend_title="Ação",
    )
    return fig


def build_volume_chart(data: dict, symbol: str) -> go.Figure:
    df = data[symbol]
    fig = go.Figure(go.Bar(
        x=df.index,
        y=df["Volume"],
        name=symbol,
        marker_color="steelblue",
        hovertemplate="%{x|%d %b %Y}<br>Vol: %{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title=f"Volume Diário — {symbol}",
        xaxis_title="Data",
        yaxis_title="Volume",
    )
    return fig
