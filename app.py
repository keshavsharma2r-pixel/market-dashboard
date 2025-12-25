import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Crypto Live Dashboard", layout="wide")

st.title("🚀 Crypto Live Candle Dashboard")
st.caption("BTCUSDT • Live Spot Candles (Binance)")

# ---------------- SIDEBAR ----------------
symbol = "BTCUSDT"

timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ["1m", "5m", "15m"]
)

limit_map = {
    "1m": 100,
    "5m": 100,
    "15m": 100
}

# ---------------- BINANCE API ----------------
@st.cache_data(ttl=10)
def fetch_candles(symbol, interval, limit):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "Open", "High", "Low", "Close", "Volume",
        "close_time", "qav", "num_trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["Close"] = df["Close"].astype(float)

    return df

# ---------------- MAIN ----------------
st.info("Live data refreshes every 10 seconds")

df = fetch_candles(symbol, timeframe, limit_map[timeframe])

if df is None or df.empty:
    st.error("Failed to fetch data from Binance")
    st.stop()

# ---------------- DISPLAY ----------------
st.subheader(f"BTCUSDT — {timeframe} Live Candles")

st.line_chart(
    df.set_index("open_time")["Close"]
)

st.subheader("Latest Candles")
st.dataframe(df.tail(5), use_container_width=True)

# ---------------- AUTO REFRESH ----------------
time.sleep(10)
st.rerun()
