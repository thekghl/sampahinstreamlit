import streamlit as st
import pandas as pd
from db import get_connection

def show():
    st.logo("data/geming.png", size="large")
    st.title("Laporan Sampahin")

    user = st.session_state.get("user", {})
    user_id = user.get("id_user")

    if user_id is not None:
        conn = get_connection()
        query = """
            SELECT 
                id_transaksi_sampah, id_admin, id_user, tanggal, total_sampah, total_pembayaran, status, jenis_sampah
            FROM transaksi_sampah
            WHERE id_user = %s
            ORDER BY tanggal DESC
        """
        df = pd.read_sql(query, conn, params=(user_id,))
        conn.close()

        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Laporan",
            data=csv,
            file_name="laporan_sampah.csv",
            mime="text/csv",
            key="download_report"
        )
    else:
        st.warning("User ID tidak ditemukan.")