import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

st.set_page_config(page_title="Market Dashboard", layout="wide")

st.title("📊 Market Dashboard")
st.caption("Step 1: Price vs EMA (Clear View)")

# Sidebar
instrument = st.sidebar.selectbox(
    "Select Index",
    ["NIFTY 50", "SENSEX"]
)

symbol_map = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN"
}

if st.sidebar.button("Load Data"):

    df = yf.download(
        symbol_map[instrument],
        period="1y",
        interval="1d"
    )

    if df is None or df.empty:
        st.error("No data received.")
        st.stop()

    # EMA
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df = df.reset_index()

    st.success("Data loaded successfully")

    # ----- PRICE LINE -----
    price_line = alt.Chart(df).mark_line(color="black").encode(
        x="Date:T",
        y="Close:Q",
        tooltip=["Date:T", "Close:Q"]
    )

    # ----- EMA LINE -----
    ema_line = alt.Chart(df).mark_line(color="red").encode(
        x="Date:T",
        y="EMA20:Q",
        tooltip=["Date:T", "EMA20:Q"]
    )

    chart = (price_line + ema_line).properties(
        height=450,
        title=f"{instrument} — Price (Black) vs EMA 20 (Red)"
    )

    st.altair_chart(chart, use_container_width=True)

else:
    st.info("👈 Select index and click **Load Data**")
