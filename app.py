import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Trader Intelligence", layout="wide")

st.title("🧠 Trader Market Intelligence")
st.caption("Bias + Market State (Closed candle logic)")

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

    # ---- SAFE SCALARS ----
    close = float(latest["Close"])
    ema50 = float(latest["EMA50"])
    ema200 = float(latest["EMA200"])

    # ---------------- BIAS ----------------
    if close > ema50 and ema50 > ema200:
        bias = "BULLISH"
        bias_color = "green"
        bias_instruction = "Only look for BUY setups"
    elif close < ema50 and ema50 < ema200:
        bias = "BEARISH"
        bias_color = "red"
        bias_instruction = "Only look for SELL setups"
    else:
        bias = "NO-TRADE"
        bias_color = "orange"
        bias_instruction = "Market structure mixed. Stay out."

    # ---------------- MARKET STATE ----------------
    separation_pct = abs(ema50 - ema200) / close * 100

    if separation_pct > 0.5:
        market_state = "TRENDING"
        state_color = "green"
        state_instruction = "Trend is healthy. Trend-following trades allowed."
    else:
        market_state = "RANGE"
        state_color = "orange"
        state_instruction = "Market is compressed. Avoid aggressive trades."

    # ---------------- OUTPUT ----------------
    st.subheader(f"{instrument} — Market Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <h3>Market Bias</h3>
            <h1 style='color:{bias_color};'>{bias}</h1>
            <p>{bias_instruction}</p>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <h3>Market State</h3>
            <h1 style='color:{state_color};'>{market_state}</h1>
            <p>{state_instruction}</p>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Bias & State calculated using EMA 50 & EMA 200 on daily closed candles"
    )

else:
    st.info("👈 Select index and click **Analyze Market**")
