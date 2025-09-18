import streamlit as st, pandas as pd
from lib.config_ops import read_lantikan

st.set_page_config(page_title="Dashboard LIC/RP")

st.header("Dashboard — Siapa LIC/RP & Tempoh Lantikan")
df = read_lantikan()

if df is None or df.empty:
    st.info("Tiada data lantikan. KP perlu import Excel di 'KP: Import Lantikan (Excel)'.")
    st.stop()

# only LIC/RP
mask = df["role_std"].isin(["LIC","RP"])
dfv = df.loc[mask].copy()

# simple filters
col1, col2, col3 = st.columns(3)
with col1:
    subj = st.text_input("Cari Subject Code", "")
with col2:
    role = st.selectbox("Role", ["All","LIC","RP"])
with col3:
    nameq = st.text_input("Cari Nama", "")

if subj:
    dfv = dfv[dfv["subject_code"].str.contains(subj.strip().upper(), na=False)]
if role != "All":
    dfv = dfv[dfv["role_std"]==role]
if nameq:
    dfv = dfv[dfv["lecturer_name"].str.contains(nameq, case=False, na=False)]

dfv = dfv.rename(columns={
    "subject_code":"Subject",
    "subject_name":"Course Name",
    "role_std":"Role",
    "lecturer_name":"Lecturer",
    "appointment_period":"Tempoh Lantikan"
})[["Subject","Course Name","Role","Lecturer","Tempoh Lantikan"]]

st.dataframe(dfv, use_container_width=True)

