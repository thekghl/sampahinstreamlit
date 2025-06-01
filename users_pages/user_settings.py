import streamlit as st
from db import get_connection

def show():
    st.title("Pengaturan User (Settings)")

    user = st.session_state.get("user", {})
    user_id = user.get("id_user")

    if user_id is not None:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_user, nama_user, Username, Password FROM user WHERE id_user = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            st.write("### Data User")
            st.write(f"**ID User:** {user_data['id_user']}")
            st.write(f"**Nama User:** {user_data['nama_user']}")
            st.write(f"**Username:** {user_data['Username']}")

            with st.expander("Ganti Password"):
                new_password = st.text_input("Password Baru", type="password")
                confirm_password = st.text_input("Konfirmasi Password Baru", type="password")
                if st.button("Simpan Password"):
                    if new_password and new_password == confirm_password:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE user SET Password = %s WHERE id_user = %s", (new_password, user_id))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success("Password berhasil diubah!")
                    elif new_password != confirm_password:
                        st.error("Password tidak sama!")
                    else:
                        st.warning("Password tidak boleh kosong.")
        else:
            st.warning("Data user tidak ditemukan.")
    else:
        st.warning("User ID tidak ditemukan.")