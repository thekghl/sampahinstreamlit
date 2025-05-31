import streamlit as st
import pandas as pd

df = pd.read_csv("data/ccdata.csv")

st.logo("data/geming.png", size="large")

st.title("Laporan Sampahin")

st.selectbox("Filter", options=["mamakmu", "mamakku", "mamaknya"])
st.dataframe(df, use_container_width=True)
st.button("Download Laporan", key="download_report")