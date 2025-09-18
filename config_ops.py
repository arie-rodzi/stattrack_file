from __future__ import annotations
import io, pandas as pd, streamlit as st
from .storage import get_client, get_admin_client, bucket, USER_SUBJ, SUBJECTS, AJK_SUBJ, LANTIKAN

def read_user_subjects() -> pd.DataFrame | None:
    try:
        stor = get_client().storage.from_(bucket())
        data = stor.download(USER_SUBJ)
        df = pd.read_csv(io.BytesIO(data))
        df["username_norm"] = df["username"].astype(str).str.strip().str.lower()
        df["subject_code"] = df["subject_code"].astype(str).str.strip().str.upper()
        df["role"] = df["role"].astype(str).str.strip().str.upper()
        return df
    except Exception:
        return None

def save_user_subjects_csv(csv_bytes: bytes):
    stor = get_admin_client().storage.from_(bucket())
    stor.upload(USER_SUBJ, csv_bytes, {"content-type":"text/csv", "upsert":"true"})

def read_subjects() -> list[str]:
    try:
        stor = get_client().storage.from_(bucket())
        data = stor.download(SUBJECTS)
        df = pd.read_csv(io.BytesIO(data))
        codes = df[df.columns[0]].astype(str).str.strip().str.upper().tolist()
        return sorted({c for c in codes if c})
    except Exception:
        return []

def save_subjects_csv(csv_bytes: bytes):
    stor = get_admin_client().storage.from_(bucket())
    stor.upload(SUBJECTS, csv_bytes, {"content-type":"text/csv", "upsert":"true"})

def read_ajk_subjects() -> pd.DataFrame | None:
    try:
        stor = get_client().storage.from_(bucket())
        data = stor.download(AJK_SUBJ)
        df = pd.read_csv(io.BytesIO(data))
        df["username_norm"] = df["username"].astype(str).str.strip().str.lower()
        df["subject_code"] = df["subject_code"].astype(str).str.strip().str.upper()
        return df
    except Exception:
        return None

def save_ajk_subjects_csv(csv_bytes: bytes):
    stor = get_admin_client().storage.from_(bucket())
    stor.upload(AJK_SUBJ, csv_bytes, {"content-type":"text/csv", "upsert":"true"})

def read_lantikan() -> pd.DataFrame | None:
    try:
        stor = get_client().storage.from_(bucket())
        data = stor.download(LANTIKAN)
        df = pd.read_csv(io.BytesIO(data))
        return df
    except Exception:
        return None

def save_lantikan_csv(csv_bytes: bytes):
    stor = get_admin_client().storage.from_(bucket())
    stor.upload(LANTIKAN, csv_bytes, {"content-type":"text/csv", "upsert":"true"})

