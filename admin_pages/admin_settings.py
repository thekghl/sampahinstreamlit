import streamlit as st
from db import get_connection

st.logo("data/geming.png", size="large")

def show():
    st.write("Halaman Settings untuk Admin")
    admin = st.session_state.get("user", {})  # Use "user" for admin session as in user_settings
    admin_id = admin.get("id_admin")

    if admin_id is not None:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_admin, nama_admin, Username, Password FROM admin WHERE id_admin = %s", (admin_id,))
        admin_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin_data:
            st.write("### Data Admin")
            st.write(f"**ID Admin:** {admin_data['id_admin']}")
            st.write(f"**Nama Admin:** {admin_data['nama_admin']}")
            st.write(f"**Username:** {admin_data['Username']}")

            with st.expander("Ganti Password"):
                new_password = st.text_input("Password Baru", type="password")
                confirm_password = st.text_input("Konfirmasi Password Baru", type="password")
                if st.button("Simpan Password"):
                    if new_password and new_password == confirm_password:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE admin SET Password = %s WHERE id_admin = %s", (new_password, admin_id))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success("Password berhasil diubah!")
                    elif new_password != confirm_password:
                        st.error("Password tidak sama!")
                    else:
                        st.warning("Password tidak boleh kosong.")
        else:
            st.warning("Data admin tidak ditemukan.")
    else:
        st.warning("Admin ID tidak ditemukan.")