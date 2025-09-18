import streamlit as st
from lib.auth_local import is_logged_in, current_username, current_role, sign_out

st.set_page_config(page_title="UiTM Filing System", page_icon="🗂️", layout="wide")
st.title("UiTM Filing System (Username Login + Roles + Dashboard)")

if is_logged_in():
    st.success(f"Logged in as {current_username()} ({current_role()})")
    if st.button("Sign out", type="secondary"):
        sign_out()
        st.rerun()
else:
    st.info("Please login from the 'Login' page in the sidebar.")

st.divider()
st.subheader("Quick Links")
st.page_link("pages/1_Login.py", label="Login")
st.page_link("pages/2_Upload.py", label="Upload Files (LIC/RP)")
st.page_link("pages/3_My_Reviews.py", label="AJK: Review Assigned Subjects")
st.page_link("pages/5_KP_Lantikan_Import.py", label="KP: Import Lantikan (Excel)")
st.page_link("pages/5_KP_Assign_AJK.py", label="KP: Assign AJK to Subjects")
st.page_link("pages/6_Auditor_All.py", label="Auditor: View All Files")
st.page_link("pages/4_Dashboard_LIC_RP.py", label="Dashboard: LIC/RP & Lantikan")

