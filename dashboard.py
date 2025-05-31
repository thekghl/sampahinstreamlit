import streamlit as st
from login import login_form
from admin_pages import admin_laporan, admin_manajemen_user, admin_settings
from pages import user_katalog, user_dashboard, user_laporan, user_settings

if "loginstate" not in st.session_state:
    st.session_state.loginstate = False

if not st.session_state.loginstate:
    login_form()
else:
    user = st.session_state.get("user", {})
    role = st.session_state.get("role", "")

    st.logo("data/geming.png", size="large")
    st.title("Dashboard Sampahin")
    st.success(f"Welcome, {user.get('nama_admin') if role == 'Admin' else user.get('nama_user', '')}!")

    # Sidebar navigation based on role
    if role == "Admin":
        menu = st.sidebar.radio(
            "Menu Admin",
            ("Dashboard","Laporan", "Manajemen User", "Settings")
        )
        if menu == "Dashboard":
            user_dashboard.show()
        elif menu == "Laporan":
            admin_laporan.show()
        elif menu == "Manajemen User":
            admin_manajemen_user.show()
        elif menu == "Settings":
            admin_settings.show()
    elif role == "User":
        menu = st.sidebar.radio(
            "Menu User",
            ("Dashboard", "Laporan", "Manajemen User", "Settings")
        )
        if menu == "Dashboard":
            user_dashboard.show()
        elif menu == "Laporan":
            user_laporan.show()
        elif menu == "Katalog":
            user_katalog.show()
        elif menu == "Settings":
            user_settings.show()
    else:
        st.error("Role tidak dikenali. Silakan login kembali.")

    if st.button("Logout"):
        st.session_state.loginstate = False
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()