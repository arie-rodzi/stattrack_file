import streamlit as st
from lib.auth_local import sign_in, is_logged_in, sign_out

st.set_page_config(page_title="Login")
st.header("Login (Username & Password)")

if is_logged_in():
    st.success("Already logged in.")
    if st.button("Sign out"):
        sign_out()
        st.rerun()
    st.stop()

with st.form("login"):
    username = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    ok = st.form_submit_button("Sign in")
    if ok:
        ok2, msg = sign_in(username, pw)
        (st.success if ok2 else st.error)(msg)
        if ok2:
            st.rerun()

