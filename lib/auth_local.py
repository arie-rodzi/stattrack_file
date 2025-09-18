from __future__ import annotations
import io, pandas as pd, streamlit as st
from .storage import get_client, get_admin_client, bucket, CRED

def _admin_usernames() -> set[str]:
    raw = st.secrets.get("app", {}).get("admin_usernames", "")
    return {u.strip().lower() for u in raw.split(",") if u.strip()}

def _read_credentials_df() -> pd.DataFrame:
    client = get_client()
    storage = client.storage.from_(bucket())
    data = storage.download(CRED)  # bytes
    df = pd.read_csv(io.BytesIO(data))
    if "role" not in df.columns:
        df["role"] = "USER"
    df["username_norm"] = df["username"].astype(str).str.strip().str.lower()
    df["role_norm"] = df["role"].astype(str).str.strip().str.upper()
    return df

def sign_in(username: str, password: str):
    try:
        df = _read_credentials_df()
        u = (username or "").strip().lower()
        row = df.loc[df["username_norm"]==u]
        if row.empty:
            return False, "Username not found."
        real_pw = str(row["temp_password"].iloc[0])
        if (password or "") != real_pw:
            return False, "Wrong password."
        st.session_state["username"] = row["username"].iloc[0]
        st.session_state["name"] = row["name"].iloc[0] if "name" in row else row["username"].iloc[0]
        st.session_state["role"] = row["role_norm"].iloc[0]
        if st.session_state["username"].lower() in _admin_usernames():
            st.session_state["role"] = "KP"
        return True, f"Welcome, {st.session_state['name']} ({st.session_state['role']})"
    except Exception as e:
        return False, f"Auth error: {e}. Admin must upload credentials.csv in Admin page."

def sign_out():
    st.session_state.pop("username", None)
    st.session_state.pop("name", None)
    st.session_state.pop("role", None)

def is_logged_in() -> bool:
    return bool(st.session_state.get("username"))

def current_username() -> str:
    return st.session_state.get("username","")

def current_role() -> str:
    return st.session_state.get("role","USER")

def is_kp() -> bool:
    return current_role() == "KP"

def is_ajk() -> bool:
    return current_role() == "AJK"

def is_auditor() -> bool:
    return current_role() == "AUDITOR"

# expose for KP page
def _read_credentials_df_internal() -> pd.DataFrame:
    return _read_credentials_df()

