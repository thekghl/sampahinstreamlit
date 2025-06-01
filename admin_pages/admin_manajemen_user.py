import streamlit as st
import pandas as pd
from db import get_connection

st.logo("data/geming.png", size="large")

def show():
    st.write("Halaman Manajemen User untuk Admin")

    # Fetch all users
    conn = get_connection()
    df = pd.read_sql("SELECT id_user, nama_user, Username, Alamat, Password, telp FROM user", conn)
    conn.close()

    st.write("### Daftar User")
    if not df.empty:
        # Table headers
        header_cols = st.columns([1,2,2,3,2,2,1,1])
        headers = ["ID", "Nama", "Username", "Alamat", "Password", "Telp", "Update", "Delete"]
        for col, header in zip(header_cols, headers):
            col.markdown(f"**{header}**")

        # Table rows with editable fields and CRUD buttons
        for idx, row in df.iterrows():
            cols = st.columns([1,2,2,3,2,2,1,1])
            # Editable fields
            nama_user = cols[1].text_input("", value=row['nama_user'], key=f"nama_{row['id_user']}")
            username = cols[2].text_input("", value=row['Username'], key=f"username_{row['id_user']}")
            alamat = cols[3].text_input("", value=row['Alamat'], key=f"alamat_{row['id_user']}")
            password = cols[4].text_input("", value=row['Password'], key=f"password_{row['id_user']}")
            telp = cols[5].text_input("", value=row['telp'], key=f"telp_{row['id_user']}")

            cols[0].write(row['id_user'])

            # Update button
            if cols[6].button("🔄", key=f"update_{row['id_user']}"):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE user SET nama_user=%s, Username=%s, Alamat=%s, Password=%s, telp=%s WHERE id_user=%s",
                    (nama_user, username, alamat, password, telp, row['id_user'])
                )
                conn.commit()
                cursor.close()
                conn.close()
                st.success(f"User {row['id_user']} berhasil diupdate!")
                st.rerun()

            # Delete button
            if cols[7].button("🗑️", key=f"delete_{row['id_user']}"):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user WHERE id_user=%s", (row['id_user'],))
                conn.commit()
                cursor.close()
                conn.close()
                st.success(f"User {row['id_user']} berhasil dihapus!")
                st.rerun()

        st.markdown("---")
    else:
        st.info("Belum ada user.")

    # Add new user
    st.write("### Tambah User Baru")
    with st.form("add_user_form"):
        nama_user = st.text_input("Nama User")
        username = st.text_input("Username")
        alamat = st.text_input("Alamat")
        password = st.text_input("Password", type="password")
        telp = st.text_input("Telp")
        submitted = st.form_submit_button("Tambah User")
        if submitted:
            if nama_user and username and alamat and password and telp:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO user (nama_user, Username, Alamat, Password, telp) VALUES (%s, %s, %s, %s, %s)",
                    (nama_user, username, alamat, password, telp)
                )
                conn.commit()
                cursor.close()
                conn.close()
                st.success("User baru berhasil ditambahkan!")
                st.rerun()
            else:
                st.warning("Semua field harus diisi.")