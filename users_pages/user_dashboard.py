import streamlit as st
from db import get_connection

def get_user_metrics(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Only sum total_pembayaran where status is 'selesai'
    cursor.execute(
        "SELECT COALESCE(SUM(total_pembayaran), 0) FROM transaksi_sampah WHERE id_user = %s AND status = 'selesai'", (user_id,)
    )
    total_pendapatan = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transaksi_sampah WHERE id_user = %s", (user_id,)
    )
    total_transaksi = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total_pendapatan, total_transaksi

def show():
    user = st.session_state.get("user", {})
    user_id = user.get("id_user")
    if user_id is not None:
        total_pendapatan, total_transaksi = get_user_metrics(user_id)
        st.write("Halaman Laporan untuk User")
        st.metric(
            "Total Pendapatan",
            "Rp. " + str("{:,}".format(int(total_pendapatan)).replace(",", ".")) + ",-"
        )
        st.metric("Total Transaksi", total_transaksi)
    else:
        st.warning("User ID tidak ditemukan.")