from __future__ import annotations
import streamlit as st
from .storage import get_client, bucket

def upload_course_file(path: str, data: bytes, content_type: str | None = None):
    try:
        storage = get_client().storage.from_(bucket())
        storage.upload(path, data, {"content-type": content_type} if content_type else None)
        url = storage.get_public_url(path)
        return True, url
    except Exception as e:
        return False, f"Upload error: {e}"

def list_prefix(prefix: str):
    try:
        storage = get_client().storage.from_(bucket())
        items = storage.list(prefix=prefix)
        out = []
        for it in items:
            d = dict(it)
            name = d.get("name","")
            p = prefix + ("" if prefix.endswith("/") else "/") + name
            d["path"] = p
            d["public_url"] = storage.get_public_url(p)
            out.append(d)
        return True, out
    except Exception as e:
        return False, f"List error: {e}"

