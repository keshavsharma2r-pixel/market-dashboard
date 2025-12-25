import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Trader Intelligence", layout="wide")

st.title("🧠 Trader Market Intelligence")
st.caption("Bias first. Execution later.")

# ---------------- SIDEBAR ----------------
instrument = st.sidebar.selectbox(
    "Select Index",
    ["NIFTY 50", "SENSEX"]
)

symbol_map = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN"
}

if st.sidebar.button("Analyze Market"):

    df = yf.download(
        symbol_map[instrument],
        period="3y",
        interval="1d"
    )

    if df is None or df.empty:
        st.error("Data not available")
        st.stop()

    # ---------------- EMA ----------------
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["EMA200"] = df["Close"].ewm(span=200, adjust=False).mean()

    df = df.dropna()

    latest = df.tail(1).iloc[0]

    # ✅ SAFE SCALAR VALUES
    close = float(latest["Close"])
    ema50 = float(latest["EMA50"])
    ema200 = float(latest["EMA200"])

    # ---------------- BIAS LOGIC ----------------
    if close > ema50 and ema50 > ema200:
        bias = "BULLISH"
        instruction = "Only look for BUY setups"
        color = "green"
    elif close < ema50 and ema50 < ema200:
        bias = "BEARISH"
        instruction = "Only look for SELL setups"
        color = "red"
    else:
        bias = "NO-TRADE"
        instruction = "Market is mixed. Stay out."
        color = "orange"

    # ---------------- OUTPUT ----------------
    st.subheader(f"{instrument} — Market Bias")

    st.markdown(
        f"""
        <h1 style='color:{color};'>{bias}</h1>
        <h4>{instruction}</h4>
        """,
        unsafe_allow_html=True
    )

    st.caption("Bias calculated using EMA 50 & EMA 200 on daily closed candles")

else:
    st.info("👈 Select index and click **Analyze Market**")
