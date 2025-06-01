import streamlit as st
from db import get_connection

st.logo("data/geming.png", size="large")

def show():
    st.write("Halaman Settings untuk Admin")
    admin = st.session_state.get("admin", {})
    admin_id = admin.get("id_admin")

    if admin_id is not None:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_admin, nama_admin, adminname, Password FROM admin WHERE id_admin = %s", (admin_id,))
        admin_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin_data:
            st.write("### Data admin")
            st.write(f"**ID admin:** {admin_data['id_admin']}")
            st.write(f"**Nama admin:** {admin_data['nama_admin']}")
            st.write(f"**adminname:** {admin_data['adminname']}")

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
        st.warning("admin ID tidak ditemukan.")