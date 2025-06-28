import streamlit as st
from datetime import date
from db import get_connection

def show():

    st.write("### Pelaporan Sampah")
    with st.form("form_laporan_sampah"):
        jenis_sampah = st.selectbox("Jenis Sampah", ["logam", "plastik", "karet", "kertas"])
        total_sampah = st.number_input("Total Sampah (kg)", min_value=0.0, step=0.1)
        if jenis_sampah == "logam":
            total_harga = total_sampah * 2160
        elif jenis_sampah == "plastik":
            total_harga = total_sampah * 50
        elif jenis_sampah == "karet":
            total_harga = total_sampah * 1400
        elif jenis_sampah == "kertas":
            total_harga = total_sampah * 3000
        formatted_total = f"{total_harga:,}".replace(",", ".")
        st.write(f"Total Harga Sampah: Rp. {formatted_total}")
        
        submitted = st.form_submit_button("Kirim Laporan")
        if submitted:
            if jenis_sampah and total_sampah > 0:
                conn = get_connection()
                cursor = conn.cursor()
                user_id = st.session_state.get("admin", {}).get("id_admin")
                today = date.today()
                status = "proses"
                id_admin = 1
                cursor.execute(
                    "INSERT INTO transaksi_sampah (id_admin, id_admin, jenis_sampah, total_sampah, tanggal, status, total_pembayaran) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (id_admin, user_id, jenis_sampah, total_sampah, today, status, total_harga)
                )
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Laporan sampah berhasil dikirim!")
            else:
                st.error("Jenis sampah dan total sampah harus diisi dengan benar.")