import streamlit as st
from db import get_connection

def check_login(username, password, role):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if role == "Admin":
        cursor.execute("SELECT * FROM admin WHERE Username=%s AND Password=%s", (username, password))
    else:
        cursor.execute("SELECT * FROM user WHERE Username=%s AND Password=%s", (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def login_form():
    st.title("Login Page")
    role = st.selectbox("Login as", ["Admin", "User"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")
    if login_btn:
        user = check_login(username, password, role)
        if user:
            st.session_state.loginstate = True
            st.session_state.user = user
            st.session_state.role = role
            st.success(f"Welcome, {user['nama_admin'] if role == 'Admin' else user['nama_user']}!")
            st.rerun()
        else:
            st.error("Invalid username or password")