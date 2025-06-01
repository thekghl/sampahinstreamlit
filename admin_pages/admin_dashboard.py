import streamlit as st

st.logo("data/geming.png", size="large")

def show():
    st.write("Halaman Dashboard untuk Admin")
    st.metric("Total Pendapatan", 10000)
    st.metric("Total Transaksi", 50000)