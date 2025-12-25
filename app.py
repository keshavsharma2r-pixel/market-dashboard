import streamlit as st
import yfinance as yf
import pandas as pd

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Market Dashboard", layout="wide")

st.title("📊 Market Dashboard")
st.caption("Step 1: Price + EMA")

# ---------------- SIDEBAR ----------------
instrument = st.sidebar.selectbox(
    "Select Index",
    ["NIFTY 50", "SENSEX"]
)

symbol_map = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN"
}

# ---------------- ACTION ----------------
if st.sidebar.button("Load Data"):

    st.info("Fetching market data...")

    df = yf.download(
        symbol_map[instrument],
        period="1y",
        interval="1d"
    )

    if df is None or df.empty:
        st.error("No data received.")
        st.stop()

    st.success("Data loaded successfully ✅")

    # ---------------- EMA CALCULATION ----------------
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

    # ---------------- DISPLAY ----------------
    st.subheader(f"{instrument} Price with EMA 20")

    chart_df = df[["Close", "EMA20"]]

    st.line_chart(chart_df)

    st.subheader("Latest Data")
    st.dataframe(df.tail())

else:
    st.info("👈 Select index and click **Load Data**")
