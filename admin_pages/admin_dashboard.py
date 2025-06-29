import streamlit as st
from db import get_connection

def get_admin_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    # Total Pendapatan hanya transaksi dengan status 'selesai'
    cursor.execute("SELECT COALESCE(SUM(total_pembayaran), 0) FROM transaksi_sampah WHERE status = 'selesai'")
    total_pendapatan = cursor.fetchone()[0]

    # Total Barang
    cursor.execute("SELECT COALESCE(SUM(total_sampah), 0) FROM transaksi_sampah")
    total_barang = cursor.fetchone()[0]

    # Total User
    cursor.execute("SELECT COUNT(*) FROM user")
    total_user = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return total_pendapatan, total_barang, total_user

def show():
    total_pendapatan, total_barang, total_user = get_admin_metrics()
    st.write("Halaman Dashboard untuk Admin")
    st.metric(
        "Total Dibayarkan",
        "Rp. " + str("{:,}".format(int(total_pendapatan)).replace(",", ".")) + ",-"
    )
    st.metric(
        "Total Barang",
        str("{:,}".format(int(total_barang)).replace(",", ".")) + " kg"
    )
    st.metric(
        "Total User",
        str(total_user)
    )