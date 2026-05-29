import streamlit as st
import connection
from datetime import datetime, timedelta

st.set_page_config(page_title='Record Page', page_icon='', layout='centered')

if 'admin_name' not in st.session_state:
    st.warning("Unautorized Entry Encountered! Please Login First!")
    st.stop()
user = st.session_state["admin_name"]
st.title("Transaction Page!")
#st.subheader("Here you can issue books...")
st.markdown(f"Admin: {user}")
conn, db_errors = connection.connect()
cursor = conn.cursor(dictionary=True)
query = conn.cursor()
query.execute("SELECT * FROM TRANSACTIONS")
ck = cursor.fetchone()
kc = 4000
with st.container():
    if conn:
        st.subheader('Books Inventory')
        cursor.execute("SELECT * FROM Books")
        Bdata = cursor.fetchall()
        if Bdata:
            st.dataframe(Bdata)
        else:
            st.markdown("No Book in the Shell")
        st.subheader("Members List")
        cursor.execute("SELECT * FROM Members")
        Mdata = cursor.fetchall()
        if Mdata:
            st.dataframe(Mdata)
        else:
            st.markdown("No Member is Listed!")
        st.subheader('Issued and Returned Books')
        cursor.execute('select * from TRANSACTIONS')
        Idata = cursor.fetchall()
        if Idata:
            st.dataframe(Idata)
        else:
            st.markdown('No Book is Issued Yet!')
    else:
        for t in db_errors:
            st.error(f'{t}')
# --- Issue New Book Form ---
with st.form("issue_book_form"):
    st.markdown("### Issue New Book")
    if Idata is None:
        st.markdown(f"New Issue ID: {kc}")
        issue_id = kc
    else:
        tc = ck[0]+1
        st.markdown(f"New Issue ID: {tc}")
        issue_id = tc
    book_id = st.text_input('Book ID', placeholder="Enter Book ID")
    member_id = st.text_input('Member ID', placeholder="Enter Member ID")
    quantity = st.number_input("Enter Quantity", min_value=1, key="quantity")
    issue_date = st.date_input('Issue Date', value=datetime.now(), key="issue_date")
    due_date = st.date_input('Due Date', value=datetime.now() + timedelta(days=14), key="due_date")


    issue_submit = st.form_submit_button("Issue", use_container_width=True)

    if issue_submit:
        query.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
        Cdata = query.fetchone()
        if Cdata and Cdata[5] <= Cdata[4]:
            if quantity <= Cdata[5]:
                query.execute("SELECT * FROM Members WHERE member_id = %s", (member_id,))
                Ddata = cursor.fetchone()
                if Ddata:
                    if book_id == Bdata[0]:
                        if member_id == Mdata[0]:
                            query.execute(
                                "INSERT INTO TRANSACTIONS (issue_id, book_id, member_id, issue_date, due_date, IssuedQuantity) VALUES (%s,%s, %s, %s, %s, %s)",
                                (issue_id, book_id, member_id, issue_date, due_date, quantity)
                            )
                            query.execute(f"UPDATE Books SET AVAILABLE_COPIES = AVAILABLE_COPIES - {quantity} WHERE book_id = %s", (book_id,))
                            conn.commit()
                            st.success("Book Issued and Inventory Updated!")
                        else:
                            st.error("Unkown Member ID")
                    else:
                        st.error("Unknown Book ID")
                else:
                    st.error(f"Member with ID {member_id} not found.")
            else:
                st.error(f"Sorry! Available copies are {Cdata[5]} and you are asking for {quantity} which cannot be fulfilled at the moment.")
        else:
            st.error("Book not found in inventory.")

with st.form("return_book_form"):
    st.markdown("### Return Book")
    issue_id = st.number_input('Issuing ID', min_value=1, key="return_issue_id")
    book_id = st.number_input('Book ID', min_value=1, key="return_book_id")
    returninQTY = st.number_input("Returning Quantity", min_value=1, key="returningQTY")
    member_id = st.number_input('Member ID', min_value=1, key="return_member_id")
    issue_date = st.date_input('Issue Date', value=datetime.now() - timedelta(days=14), key="return_issue_date")
    return_date = st.date_input('Return Date', value=datetime.now(), key="return_date")

    return_submit = st.form_submit_button("Return", use_container_width=True)

    if return_submit:
        query.execute("SELECT * FROM TRANSACTIONS WHERE issue_id = %s", (issue_id,))
        Rdata = query.fetchone()
        st.success('Fetch Success')
        qty = Rdata[6]
        if Rdata:
            if returninQTY <= qty:
                duration = (return_date - issue_date).days
                st.markdown(f"The book was returned after **{duration} days**.")
                st.markdown(f"Total issued quntity was {qty}, Returning {returninQTY}, Now Remaining {qty-returninQTY}")
                query.execute(f"UPDATE Books SET AVAILABLE_COPIES = AVAILABLE_COPIES + {returninQTY} WHERE book_id=%s", (book_id,))
                query.execute(f"UPDATE TRANSACTIONS SET RETURN_DATE={return_date}, Returned={returninQTY}, ToBeReturned={qty-returninQTY} WHERE ISSUE_ID={issue_id}")
                conn.commit()
                st.success('Dump Success')
            else:
                st.error(f"Total {qty} books were issued. Can't Accept Additional.")
        else:
            st.error("No such issue record found.")
    conn.close()