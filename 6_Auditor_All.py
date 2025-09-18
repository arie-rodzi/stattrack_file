import streamlit as st
from lib.auth_local import is_logged_in, is_auditor
from lib.uploading import list_prefix

st.set_page_config(page_title="Auditor View")

st.header("Auditor — View All Files")
if not is_logged_in() or not is_auditor():
    st.error("Auditors only.")
    st.stop()

subject = st.text_input("Subject prefix (e.g., MAT602)", value="")
prefix = subject.strip().upper()
if not prefix:
    st.info("Enter a subject code or partial prefix to list.")
else:
    ok, items = list_prefix(prefix)
    if not ok:
        st.error(items)
    else:
        if not items:
            st.info("No items under that prefix.")
        else:
            for it in items:
                st.write(f"- {it.get('path','')}")
                st.link_button("Open", it.get("public_url",""))

