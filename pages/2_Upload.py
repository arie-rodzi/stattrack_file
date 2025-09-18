import time, streamlit as st
from lib.auth_local import is_logged_in, current_username
from lib.config_ops import read_user_subjects
from lib.uploading import upload_course_file

st.set_page_config(page_title="Upload Files")

st.header("Upload Course Files (LIC/RP)")
if not is_logged_in():
    st.error("Please login first.")
    st.stop()

user = current_username().strip().lower()

df = read_user_subjects()
if df is None:
    st.warning("user_subjects.csv not found. Ask admin to upload in Admin page.")
    st.stop()

mine = df[(df["username_norm"]==user) & (df["role"].isin(["LIC","RP"]))]
if mine.empty:
    st.info("No LIC/RP subject assigned to your username.")
    st.stop()

subjects = sorted(mine["subject_code"].unique().tolist())
subject = st.selectbox("Subject Code", subjects)
roles = sorted(mine[mine["subject_code"]==subject]["role"].unique().tolist())
role = st.selectbox("Role", roles)

file = st.file_uploader("Choose a file", type=["pdf","doc","docx","xls","xlsx","csv","png","jpg","jpeg","zip"])
note = st.text_input("Optional note")

if st.button("Upload", disabled=not file):
    ts = int(time.time())
    fname = file.name.replace("/", "_")
    path = f"{subject}/{role}/{user}/{ts}_{fname}"
    ok, url = upload_course_file(path, file.getvalue(), file.type)
    if ok:
        st.success("Upload success!")
        st.code(url, language="text")
        st.link_button("Open file", url=url)
    else:
        st.error(url)

