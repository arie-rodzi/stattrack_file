import streamlit as st
from lib.auth_local import is_logged_in, current_username, is_ajk
from lib.config_ops import read_ajk_subjects
from lib.uploading import list_prefix

st.set_page_config(page_title="AJK Reviews")

st.header("AJK — Review Assigned Subjects")
if not is_logged_in():
    st.error("Please login first.")
    st.stop()

if not is_ajk():
    st.warning("This page is for AJK only.")
    st.stop()

user = current_username().strip().lower()
df = read_ajk_subjects()
if df is None:
    st.info("No AJK assignment found. KP must assign first.")
    st.stop()

mine = df[df["username_norm"]==user]
if mine.empty:
    st.info("You have no assigned subjects yet.")
    st.stop()

subjects = sorted(mine["subject_code"].unique().tolist())
subject = st.selectbox("Subject Code", subjects)

ok, items = list_prefix(f"{subject}")
if not ok:
    st.error(items)
else:
    st.caption("Files under this subject:")
    if not items:
        st.info("No files found yet.")
    else:
        for it in items:
            st.write(f"- {it.get('path','')}")
            st.link_button("Open", it.get("public_url",""))

