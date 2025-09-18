import streamlit as st, pandas as pd, io
from lib.auth_local import is_logged_in, is_kp
from lib.lantikan import parse_lantikan_excel
from lib.config_ops import save_lantikan_csv

st.set_page_config(page_title="KP Import Lantikan")
st.header("KP — Import Lantikan (Excel -> CSV)")

if not is_logged_in() or not is_kp():
    st.error("KP only.")
    st.stop()

f = st.file_uploader("Upload fail Excel lantikan (contoh: Lantikan LIC Mac 2024.xlsx)", type=["xlsx"])
if f and st.button("Process & Save"):
    df = parse_lantikan_excel(f.read())
    if df.empty:
        st.error("Tak jumpa jadual lantikan dalam Excel.")
    else:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        save_lantikan_csv(csv_bytes)
        st.success(f"Siap! {len(df)} rekod disimpan ke config/lantikan.csv")
        st.dataframe(df.head(50), use_container_width=True)
        st.download_button("Download lantikan.csv (preview)", data=csv_bytes, file_name="lantikan.csv", mime="text/csv")

