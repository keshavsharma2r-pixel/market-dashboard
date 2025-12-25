import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Market Dashboard", layout="wide")

st.title("📊 Market Dashboard")
st.caption("Step 0: Data loading check")

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

    st.write("Last 5 rows of data:")
    st.dataframe(df.tail())

    st.subheader("Price Chart")
    st.line_chart(df["Close"])

else:
    st.info("👈 Select index and click **Load Data**")
