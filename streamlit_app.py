import streamlit as st
import pandas as pd

st.title("Crypto Tech Agent Dashboard")

url = "https://raw.githubusercontent.com/cr7pto0-py/crypto-tech-agent/main/crypto_top20_ratings.csv"

df = pd.read_csv(url)

st.subheader("Top 20 Crypto Ratings")
st.dataframe(df)

st.subheader("Score by Asset")
st.bar_chart(df.set_index("symbol")["score"])
