import streamlit as st
from db import get_connection

def get_admin_metrics(admin_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(total_pembayaran), 0) FROM transaksi_sampah WHERE id_user = %s", (admin_id,)
    )
    total_pendapatan = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transaksi_sampah WHERE id_user = %s", (admin_id,)
    )
    total_transaksi = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total_pendapatan, total_transaksi

def show():
    admin = st.session_state.get("admin", {})
    admin_id = admin.get("id_admin")
    if admin_id is not None:
        total_pendapatan, total_transaksi = get_admin_metrics(admin_id)
        st.write("Halaman Laporan untuk Admin")
        st.metric(
            "Total Pendapatan",
            "Rp. " + str("{:,}".format(int(total_pendapatan)).replace(",", ".")) + ",-"
        )
        st.metric("Total Transaksi", total_transaksi)
    else:
        st.warning("Admin ID tidak ditemukan.")
