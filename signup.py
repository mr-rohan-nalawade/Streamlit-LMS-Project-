import streamlit as st
import authenticate
import connection
import time

st.set_page_config(page_title="Add Admin", page_icon="📝", layout="centered")

st.title("📝Add New Admin!")
st.subheader("Fill all your credentials!")

conn, db_errors = connection.connect()
cursor = conn.cursor()
cursor.execute("SELECT * FROM ADMINISTRATION")
ad = cursor.fetchone()
a = 1000

with st.form("signup_form"):
    if ad is None:
        #admin_id = st.text_input('Your New ID', value=a, disabled=True)
        st.markdown(f"Your New ID: {a}")
        admin_id = a
    else:
        #admin_id = st.text_input("Your New ID", value=ad[0]+1, disabled=True)
        b = ad[0] + 1
        st.markdown(f"Your New ID: {b}")
        admin_id = b
    full_name = st.text_input("Full Name", placeholder="Enter your full Name")
    password = st.text_input("Password", type="password", placeholder="Enter your Password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
    submit = st.form_submit_button("Add")

    if submit:
        if all([admin_id, full_name, password, confirm_password]):
            is_valid, errors = authenticate.password(password)
            if is_valid:
                if password == confirm_password:
                    if conn:
                        cursor.execute("SELECT * FROM administration WHERE admin_id = (%s)",(admin_id,))
                        if cursor.fetchone():
                            st.error("Admin ID already exists!")
                        else:
                            cursor.execute("INSERT INTO administration (admin_id, admin_name,  password) VALUES (%s,%s,%s)",(admin_id, full_name, password))
                            conn.commit()
                            conn.close()
                            st.success("Added successfully! Redirecting you to login page...")
                            time.sleep(2)
                            st.switch_page("main.py")
                    else:
                        for errs in db_errors:
                            st.error(f"Database connection failed: {errs}")
                else:
                    st.error("Password does not match!")
            else:
                for err in errors:
                    st.error(f"Error: {err}")
        else:
            st.error("All fields are mandatory!")

if st.button("Back to Login Page"):
    st.switch_page("main.py")