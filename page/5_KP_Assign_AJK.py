import io, streamlit as st, pandas as pd
from lib.auth_local import is_logged_in, is_kp, _read_credentials_df_internal
from lib.config_ops import read_subjects, save_subjects_csv, read_ajk_subjects, save_ajk_subjects_csv

st.set_page_config(page_title="KP Assign AJK")
st.header("KP — Assign AJK to Subjects")
if not is_logged_in() or not is_kp():
    st.error("KP only.")
    st.stop()

st.subheader("Step 1 — Subjects list")
subs = read_subjects()
st.caption("Jika kosong, upload subjects.csv (satu kolum: subject_code).")
uploaded_subs = st.file_uploader("subjects.csv", type=["csv"])
if uploaded_subs and st.button("Save subjects.csv"):
    save_subjects_csv(uploaded_subs.read())
    st.success("subjects.csv saved.")

if subs:
    st.write(f"Subjects found: {len(subs)}")

st.markdown("---")
st.subheader("Step 2 — Assign AJK")
df_cred = _read_credentials_df_internal()
ajk_users = df_cred.loc[df_cred["role_norm"]=="AJK","username"].astype(str).tolist()
if not ajk_users:
    st.warning("Tiada pengguna role AJK dalam credentials.csv")
    st.stop()

existing = read_ajk_subjects()
current_map = {}
if existing is not None:
    for _, r in existing.iterrows():
        current_map.setdefault(r["subject_code"], set()).add(r["username_norm"])

sel_subject = st.selectbox("Subject", subs or [])
sel_ajk = st.multiselect("Assign AJK usernames", ajk_users, default=sorted(list(current_map.get(sel_subject, set()))))

if st.button("Save assignment"):
    rows = []
    if existing is not None:
        for _, r in existing.iterrows():
            if r["subject_code"] != sel_subject:
                rows.append({"subject_code": r["subject_code"], "username": r["username_norm"]})
    for u in sel_ajk:
        rows.append({"subject_code": sel_subject, "username": u})
    out = pd.DataFrame(rows).drop_duplicates()
    csv_bytes = out.to_csv(index=False).encode("utf-8")
    save_ajk_subjects_csv(csv_bytes)
    st.success("AJK assignment saved.")
    st.download_button("Download ajk_subjects.csv", data=csv_bytes, file_name="ajk_subjects.csv", mime="text/csv")

