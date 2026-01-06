import streamlit as st
import pandas as pd

st.title("Crypto Tech Agent Dashboard")

url = "https://raw.githubusercontent.com/cr7pto0-py/crypto-tech-agent/main/crypto_top20_ratings.csv"
df = pd.read_csv(url)

st.write("### CSV Columns Loaded:")
st.write(list(df.columns))

st.write("### Data Preview:")
st.dataframe(df)
