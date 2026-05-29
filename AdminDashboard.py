import streamlit as st

st.set_page_config(page_title="Administration Dashboard", page_icon="", layout='centered')

if 'admin_name' not in st.session_state:
    st.warning('Unauthorised Entry Encountered! Please Login First!')
    st.stop()

name = st.session_state['admin_name']
st.title("Administration Dashboard")
st.subheader(f"Welcome, {name}!")


with st.container():
    if st.button('Books Section', use_container_width=True):
        st.switch_page('pages/Books.py')
    if st.button('Members Section', use_container_width=True):
        st.switch_page("pages/Members.py")
    if st.button("Transaction Section", use_container_width=True):
        st.switch_page('pages/Transaction.py')