import streamlit as st
import connection
import time

st.set_page_config(page_title="Library Management System", page_icon="", layout="centered")

st.title("Welcome to Library Management System!")
#st.subheader("Please log in before proceeding further...")

#col1, col2 = st.columns(2)
admin_i = 99
conn, db_errors = connection.connect()
cursor = conn.cursor()
with st.container():
    admin_id = st.text_input("Admin ID", placeholder="Enter Admin ID")
    password = st.text_input("Password", type='password', placeholder='Enter your password')
    col1, col2 = st.columns(2)
    with col1:
        login_btn = st.button('Log In', use_container_width=True)
        if login_btn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM administration where admin_id = %s", (admin_id,))
                result = cursor.fetchone()
                if result != None or result[0] == admin_id:
                    if result[2] == password:
                        st.session_state['admin_name'] = result[1]
                        st.success(f"Log in successful! Redirecting you to Administration Dasboard...")
                        time.sleep(2)
                        st.switch_page("pages/AdminDashboard.py")
                    else:
                         st.error('Password Not Match')
                else:
                     st.error('Unregistered Admin ID')
            else:
                for i in db_errors:
                    st.error(f"{i}")
    with col2:
        sign_up_btn = st.button('New Admin?', use_container_width=True)
        if sign_up_btn:
            st.switch_page("pages/signup.py")