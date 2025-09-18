# app.py  — SAFE BOOT VERSION
import traceback, sys, os
import streamlit as st

st.set_page_config(page_title="UiTM Filing System — Safe Boot", layout="wide")
st.title("UiTM Filing System — Safe Boot")

# 1) check that supabase is installed
ok_supabase = False
try:
    from supabase import create_client  # noqa
    ok_supabase = True
    st.success("✅ Package check: supabase is installed.")
except Exception as e:
    st.error("❌ Package check: `supabase` not installed.")
    st.code(str(e))
    st.info("Fix: ensure `requirements.txt` (root) contains `supabase==2.4.0` and push; then Reboot app.")
    st.stop()

# 2) quick secrets sanity (don’t print actual values)
def has(path):
    cur = st.secrets
    for k in path:
        if k not in cur:
            return False
        cur = cur[k]
    return True

missing = []
for p in (["supabase","url"], ["supabase","key"], ["supabase","service_role"], ["app","bucket"]):
    if not has(p):
        missing.append(" -> ".join(p))

if missing:
    st.error("❌ Secrets missing/invalid:\n" + "\n".join(f"- {m}" for m in missing))
    st.write("Paste this in *Settings → Secrets* (change the three values marked ✅):")
    st.code(
        '[supabase]\n'
        'url = "https://YOUR-REF.supabase.co"        # ✅ API → Project URL\n'
        'key = "YOUR-ANON-KEY"                       # ✅ anon public key\n'
        'service_role = "YOUR-SERVICE-KEY"           # ✅ service_role key\n\n'
        '[app]\n'
        'bucket = "uitm-files"\n'
        'admin_usernames = "zahari"\n'
    )
    st.stop()

# 3) try connecting to Supabase (anon) and listing the bucket prefix
from supabase import create_client
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    client = create_client(url, key)
    bucket = st.secrets.get("app",{}).get("bucket","uitm-files")
    # attempt a benign list on config/
    _ = client.storage.from_(bucket).list("config/")
    st.success(f"✅ Supabase connection OK. Bucket: {bucket}")
except Exception as e:
    st.error("❌ Supabase connection failed.")
    st.code(str(e))
    st.info("Check: URL ends with .supabase.co (no trailing slash), keys not truncated, and bucket exists in Supabase Storage.")
    st.stop()

# 4) only now import your real app modules
try:
    from lib.auth_local import is_logged_in, current_username, current_role, sign_out
    st.caption("Imports OK — loading main links…")
except Exception as e:
    st.error("❌ Import error while loading lib/* modules.")
    st.code("".join(traceback.format_exception_only(type(e), e)).strip())
    st.write("Likely causes: missing `lib/__init__.py`, wrong file paths, or syntax error in a lib file.")
    st.write("Make sure your repo layout is:")
    st.code(
        "app.py\n"
        "lib/__init__.py\n"
        "lib/storage.py\n"
        "lib/auth_local.py\n"
        "lib/config_ops.py\n"
        "lib/lantikan.py\n"
        "lib/uploading.py\n"
        "pages/...\n"
        "requirements.txt\n"
    )
    st.stop()

# 5) Minimal home while you fix things
st.success(f"Logged in: {is_logged_in()}  |  Role (if logged): {current_role() if is_logged_in() else '-'}")
if is_logged_in():
    st.write(f"Hello **{current_username()}**")
    if st.button("Sign out"):
        sign_out(); st.rerun()

st.markdown("---")
st.subheader("Quick Links")
st.page_link("pages/1_Login.py", label="Login")
st.page_link("pages/2_Upload.py", label="Upload Files (LIC/RP)")
st.page_link("pages/3_My_Reviews.py", label="AJK: Review Assigned Subjects")
st.page_link("pages/5_KP_Lantikan_Import.py", label="KP: Import Lantikan (Excel)")
st.page_link("pages/5_KP_Assign_AJK.py", label="KP: Assign AJK to Subjects")
st.page_link("pages/6_Auditor_All.py", label="Auditor: View All Files")
st.page_link("pages/4_Dashboard_LIC_RP.py", label="Dashboard: LIC/RP & Lantikan")
