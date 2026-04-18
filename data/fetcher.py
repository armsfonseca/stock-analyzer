import yfinance as yf
import pandas as pd
import streamlit as st

TICKERS = {
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
    "Petrobras (PETR4)": "PETR4.SA",
}

START_DATE = "2025-01-01"
END_DATE = "2026-04-30"


@st.cache_data(ttl=3600)
def fetch_all(start: str = START_DATE, end: str = END_DATE) -> dict:
    result = {}
    for label, symbol in TICKERS.items():
        df = yf.download(symbol, start=start, end=end, auto_adjust=True, progress=False)
        df.index = pd.to_datetime(df.index)
        # Flatten multi-level columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        result[symbol] = df
    return result
