import connection
import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Member Panel", page_icon="", layout="centered")

if 'admin_name' not in st.session_state:
    st.warning("Unauthorized Entry Encountered! Please Login First!")
    st.stop()

st.title("Update Member List!")
st.subheader("Add Member")

conn, db_errors = connection.connect()
cursor = conn.cursor()
cursor.execute("SELECT * FROM MEMBERS")
d = cursor.fetchone()
s = 2000
with st.container():
    if d is None:
        st.markdown(f"Your New Member ID: {s}")
        member_id = s
    else:
        t = d[0]+1
        st.markdown(f"Your New Member ID: {t}")
        member_id = t
    member_name = st.text_input("Member Name", placeholder="Enter Name of the new member")
    email = st.text_input("Email", placeholder="Enter email of the member")
    join_date = st.date_input("Join Date", value=datetime.now())
    status = st.selectbox("Status", ['Active', 'Inactive'])
    submit = st.button("Add Member", use_container_width=True)
    back_to_login = st.button("Back to Login Page", use_container_width=True)
    view_members = st.button("View All Existing Members", use_container_width=True)
    conn, db_errors = connection.connect()

    if submit:
        if all([member_id, member_name, email, join_date, status]):
            if conn:
                cursor.execute("SELECT * FROM MEMBERS WHERE MEMBER_ID = %s", (member_id,))
                check = cursor.fetchone()
                if check == None or check[0] != member_id:
                    cursor.execute("INSERT INTO MEMBERS (MEMBER_ID, MEMBER_NAME, EMAIL, JOIN_DATE, STATUS) VALUES (%s, %s, %s, %s, %s)", (member_id, member_name, email, join_date, status))
                    conn.commit()
                    st.success("Member Added Successfully!")
                else:
                    st.error('Member ID Already Exists!')
            else:
                for err in db_errors:
                    st.error(f"{err}")
        else:
            st.error("All Fields are Mandatory!")

    if back_to_login:
            st.success("Redirecting you to Login Page...")
            time.sleep(2)
            st.switch_page("main.py")

    if conn:
        if view_members:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM MEMBERS")
            data = cursor.fetchall()
            if data:
                st.markdown('Members List')
                st.dataframe(data)
            else:
                st.error("No Member Data Found!")
    else:
        for errs in db_errors:
            st.error(f"{errs}")
    conn.close()