import streamlit as st
import pandas as pd
from db import get_connection

st.logo("data/geming.png", size="large")

def show():
    st.write("Halaman Laporan untuk Admin")

    conn = get_connection()
    query = """
        SELECT id_transaksi_sampah, id_admin, id_user, tanggal, total_sampah, total_pembayaran, status, jenis_sampah
        FROM transaksi_sampah
        ORDER BY tanggal DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:
        st.write("### Daftar Transaksi (Status dapat diubah langsung di tabel)")
        # Add column headers
        header_cols = st.columns([1,1,1,2,1,2,2,2])
        headers = [
            "ID Transaksi", "ID Admin", "ID User", "Tanggal",
            "Total Sampah", "Total Pembayaran", "Status", "Jenis Sampah"
        ]
        for col, header in zip(header_cols, headers):
            col.markdown(f"**{header}**")

        # Show table with editable status
        for idx, row in df.iterrows():
            cols = st.columns([1,1,1,2,1,2,2,2])
            cols[0].write(row['id_transaksi_sampah'])
            cols[1].write(row['id_admin'])
            cols[2].write(row['id_user'])
            cols[3].write(str(row['tanggal']))
            cols[4].write(row['total_sampah'])
            cols[5].write(row['total_pembayaran'])
            # Dropdown for status
            new_status = cols[6].selectbox(
                "",
                options=['proses', 'selesai', 'batal'],
                index=['proses', 'selesai', 'batal'].index(row['status']),
                key=f"status_{row['id_transaksi_sampah']}"
            )
            cols[7].write(row['jenis_sampah'])
            # Update button per row
            if new_status != row['status']:
                if cols[6].button("Update", key=f"update_{row['id_transaksi_sampah']}"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE transaksi_sampah SET status = %s WHERE id_transaksi_sampah = %s",
                        (new_status, row['id_transaksi_sampah'])
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    st.success(f"Status transaksi {row['id_transaksi_sampah']} berhasil diubah menjadi {new_status}")
                    st.rerun()
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Laporan",
            data=csv,
            file_name="laporan_sampah.csv",
            mime="text/csv",
            key="download_report"
        )
    else:
        st.warning("Tidak ada data transaksi.")