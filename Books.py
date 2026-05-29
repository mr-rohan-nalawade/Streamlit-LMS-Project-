import connection
import streamlit as st
#import datetime
import time

st.set_page_config(page_title="Book Panel", page_icon="", layout="centered")

if 'admin_name' not in st.session_state:
    st.warning("Unauthorized Entry Encountered! Please Login First!")
    st.stop()

st.title("Update Books Shell")
st.subheader("Add New Book!")

conn, db_errors = connection.connect()
cursor = conn.cursor()
cursor.execute("SELECT * FROM BOOKS")
r = cursor.fetchone()
h = 3000
if r is None:
    st.markdown(f"New Member ID: {h}")
    book_id = h
else:
    k = r[0]+1
    st.markdown("New Member ID: {k}")
    book_id = k
title = st.text_input("Book Name", placeholder="Enter Name of the new book")
genre = st.selectbox("Select Genre of Book", ['fantasy', 'science fiction', 'mystery', 'thriller', 'romance', 'historical fiction', 'horror', 'Biography'])
author = st.text_input("Author", placeholder="Enter Name of Author")
total_copies = st.number_input("Total Copies", min_value=1)

with st.container():
    submit = st.button("Add Book", use_container_width=True)
    if submit:
        if all([book_id, title, genre, author, total_copies]):
            if conn:
                cursor.execute("INSERT INTO BOOKS (BOOK_ID, TITLE, AUTHOR, GENRE, TOTAL_COPIES, AVAILABLE_COPIES) VALUES (%s,%s,%s,%s,%s,%s)",(book_id, title, author, genre, total_copies, total_copies))
                st.success("Book Added Successfully!")
                conn.commit()
            else:
                for err in db_errors:
                    st.error(f"{err}")
        else:
            st.error("All Fields are mandatory!")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        back_to_login = st.button("Back to Login Page", use_container_width=True)
        if back_to_login:
            j = 1
            st.success("Going back to login page...")
            time.sleep(2)
            st.switch_page('main.py')
    with col2:
        view_books = st.button("View All Books", use_container_width=True)
        if view_books:
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM BOOKS")
                data = cursor.fetchall()
            if data:
                j = 2
            else:
                j = 3
        else:
            j = 4
    with col3:
        if st.button("Members Section"):
            j = 5
    with col4:
        if st.button("Transaction Section"):
            j = 6
            st.success("Heading to Transaction Section >>>")
    conn.close()
with st.container():
    if j == 2:
        st.dataframe(data, use_container_width=True)
    elif j == 3:
        st.warning("No Book listed Yet!")
    elif j == 4:
        for errs in db_errors:
            st.error(f"{errs}")
    elif j == 5:
        st.success("Heading to Members Section >>>")
        st.switch_page("pages/Members.py")

