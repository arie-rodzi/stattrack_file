from __future__ import annotations
import streamlit as st
from supabase import create_client, Client

CONFIG_PREFIX = "config/"
CRED = CONFIG_PREFIX + "credentials.csv"
USER_SUBJ = CONFIG_PREFIX + "user_subjects.csv"
SUBJECTS = CONFIG_PREFIX + "subjects.csv"
AJK_SUBJ = CONFIG_PREFIX + "ajk_subjects.csv"
LANTIKAN = CONFIG_PREFIX + "lantikan.csv"

@st.cache_resource(show_spinner=False)
def get_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

@st.cache_resource(show_spinner=False)
def get_admin_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role"]
    return create_client(url, key)

def bucket() -> str:
    return st.secrets.get("app", {}).get("bucket", "uitm-files")

