import streamlit as st

st.logo("data/geming.png", size="large")

st.title("Dashboard Sampahin")

st.metric("Total Pendapatan", 10000, delta=None, delta_color="normal", help=None, label_visibility="visible", border=True)
st.metric("Total Transaksi", 10000, delta=None, delta_color="inverse", help=None, label_visibility="visible", border=True)
