from __future__ import annotations
import streamlit as st
from supabase import create_client, Client

CONFIG_PREFIX = "config/"
CRED = CONFIG_PREFIX + "credentials.csv"
USER_SUBJ = CONFIG_PREFIX + "user_subjects.csv"
SUBJECTS = CONFIG_PREFIX + "subjects.csv"
AJK_SUBJ = CONFIG_PREFIX + "ajk_subjects.csv"
LANTIKAN = CONFIG_PREFIX + "lantikan.csv"

def _require(path):
    cur = st.secrets
    for k in path:
        if k not in cur:
            raise RuntimeError(f"Missing secret: {' -> '.join(path)}")
        cur = cur[k]
    return cur

@st.cache_resource(show_spinner=False)
def get_client() -> Client:
    url = _require(["supabase","url"])
    key = _require(["supabase","key"])
    if not (isinstance(url, str) and url.endswith(".supabase.co")):
        raise RuntimeError("Supabase url looks invalid (must end with .supabase.co, no trailing slash).")
    if not key or len(key) < 20:
        raise RuntimeError("Supabase anon key looks invalid (too short).")
    return create_client(url, key)

@st.cache_resource(show_spinner=False)
def get_admin_client() -> Client:
    url = _require(["supabase","url"])
    key = _require(["supabase","service_role"])
    if not key or len(key) < 20:
        raise RuntimeError("Supabase service_role key looks invalid (too short).")
    return create_client(url, key)

def bucket() -> str:
    b = st.secrets.get("app",{}).get("bucket","uitm-files")
    if not b: raise RuntimeError("Bucket name missing: set [app] bucket in secrets.")
    return b
