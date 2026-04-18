# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app
python -m streamlit run app.py --browser.gatherUsageStats=false

# Install dependencies
pip install -r requirements.txt
```

The app runs at `http://localhost:8501`. Streamlit hot-reloads on file save.

## Architecture

Three-layer structure:

- **[app.py](app.py)** — Streamlit entry point. Handles UI layout, sidebar widgets, and metric cards. Calls `fetch_all()` and passes data to chart builders.
- **[data/fetcher.py](data/fetcher.py)** — Downloads OHLCV data from Yahoo Finance via `yfinance`. Results are cached with `@st.cache_data(ttl=3600)` to avoid repeated API calls. Tickers use the `.SA` suffix for B3 (Brazilian exchange). `START_DATE`/`END_DATE` constants define the 2025–2026 window.
- **[charts/builders.py](charts/builders.py)** — Pure functions that receive `data: dict[symbol → DataFrame]` and return `plotly.graph_objects.Figure`. Three charts: closing price (line), % performance normalized to Jan 2025 baseline (line), and daily volume (bar).

## Key conventions

- `TICKERS` dict in `fetcher.py` maps display labels → Yahoo Finance symbols. Add new stocks here.
- Chart functions are stateless — they take data and return figures, no side effects.
- `yf.download()` can return multi-level columns; `fetcher.py` flattens them to single-level before returning.
- Performance chart normalizes all series to 0% at `close.iloc[0]` (first trading day of the period).
