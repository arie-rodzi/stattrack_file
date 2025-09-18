import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Diagnostics")
st.header("🔧 Diagnostics — Secrets & Supabase")

def has(path):
    cur = st.secrets
    for k in path:
        if k not in cur: 
            return False
        cur = cur[k]
    return True

st.subheader("Secrets check")
st.write("- supabase.url present:", has(["supabase","url"]))
st.write("- supabase.key present:", has(["supabase","key"]))
st.write("- supabase.service_role present:", has(["supabase","service_role"]))
st.write("- app.bucket present:", has(["app","bucket"]))

st.subheader("Supabase client test")
ok1, msg1 = False, ""
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    client = create_client(url, key)
    ok1 = True
    msg1 = "create_client OK"
except Exception as e:
    msg1 = f"create_client failed: {e}"
st.write("Anon client:", ("✅ " if ok1 else "❌ "), msg1)

st.subheader("Bucket test")
try:
    bucket = st.secrets.get("app",{}).get("bucket","uitm-files")
    items = client.storage.from_(bucket).list("config/")
    st.success(f"List 'config/' in '{bucket}': OK. Items: {len(items)}")
except Exception as e:
    st.error(f"Bucket list error: {e}")

st.caption("👉 If you see ❌ above, check your Streamlit Cloud secrets format and bucket name in Supabase.")
