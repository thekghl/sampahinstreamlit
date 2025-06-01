import streamlit as st
import pandas as pd
from db import get_connection

st.logo("data/geming.png", size="large")

def show():
    st.write("Halaman Laporan untuk Admin")
    
    laporan = st.session_state.get("transaksi_sampah", {})
    laporan_id = laporan.get("id_transaksi_sampah")

    if laporan_id is not None:
        conn = get_connection()
        query = """
            SELECT * FROM transaksi_sampah
            ORDER BY tanggal DESC
        """
        df = pd.read_sql(query, conn, params=(laporan_id,))
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
        st.warning("Laporan ID tidak ditemukan.")