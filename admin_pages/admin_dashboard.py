import streamlit as st

def show():
    st.write("Halaman Dashboard untuk Admin")
    st.metric("Total Pendapatan", 10000)
    st.metric("Total Transaksi", 50000)