import streamlit as st
import pandas as pd
from agent import run_agent

st.set_page_config(
    page_title="Crypto Technical Analysis Agent",
    layout="wide"
)

st.title("📊 Crypto Technical Analysis Agent")
st.caption("Multi-timeframe trend-following model (1D / 4H / 1H)")

# Currency selection
currency = st.selectbox(
    "Select currency",
    ["usd", "eur", "chf"],
    index=2
)

st.write(f"Using **{currency.upper()}** as base currency")

# Run agent button
if st.button("🔄 Refresh Data"):
    with st.spinner("Fetching data and computing indicators..."):
        df = run_agent(vs_currency=currency)
        st.session_state["results"] = df

# Load results if available
if "results" in st.session_state:
    df = st.session_state["results"]

    st.subheader("Top 20 Crypto Ratings")
    st.dataframe(df.sort_values("overall_rating", ascending=False), use_container_width=True)

    # CSV export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV for Power BI",
        data=csv,
        file_name="crypto_top20_ratings.csv",
        mime="text/csv"
    )

    # Indicator breakdown
    st.subheader("Indicator Breakdown (Blended Timeframes)")
    indicator_cols = [
        "macd_score", "adx_score", "ma_cross_score", "ao_score",
        "rsi_score", "cci_score", "williams_r_score", "swing_index_score"
    ]

    st.dataframe(
        df[["symbol"] + indicator_cols].sort_values("macd_score", ascending=False),
        use_container_width=True
    )

else:
    st.info("Click **Refresh Data** to load the latest crypto analysis.")