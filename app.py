import streamlit as st
from data.fetcher import fetch_all, TICKERS
from charts.builders import build_price_chart, build_performance_chart, build_volume_chart

st.set_page_config(page_title="Analisador B3", layout="wide")
st.title("Analisador de Ações B3 — 2025/2026")
st.caption("Itaú (ITUB4) · Vale (VALE3) · Petrobras (PETR4)")

st.sidebar.header("Configurações")
selected_labels = st.sidebar.multiselect(
    "Selecionar ações",
    options=list(TICKERS.keys()),
    default=list(TICKERS.keys()),
)

with st.spinner("Buscando dados da Yahoo Finance..."):
    data = fetch_all()

if not selected_labels:
    st.warning("Selecione pelo menos uma ação no painel lateral.")
    st.stop()

selected_symbols = [TICKERS[label] for label in selected_labels]

volume_label = st.sidebar.selectbox("Ação para gráfico de volume", options=selected_labels)
volume_symbol = TICKERS[volume_label]

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(build_price_chart(data, selected_symbols), use_container_width=True)
with col2:
    st.plotly_chart(build_performance_chart(data, selected_symbols), use_container_width=True)

st.plotly_chart(build_volume_chart(data, volume_symbol), use_container_width=True)

st.subheader("Resumo")
cols = st.columns(len(selected_symbols))
for col, symbol in zip(cols, selected_symbols):
    close = data[symbol]["Close"].dropna()
    if close.empty:
        col.metric(label=symbol, value="Sem dados")
        continue
    total_return = ((close.iloc[-1] / close.iloc[0]) - 1) * 100
    col.metric(
        label=symbol,
        value=f"R$ {float(close.iloc[-1]):.2f}",
        delta=f"{total_return:+.1f}% desde Jan 2025",
    )
