from __future__ import annotations
import pandas as pd

def parse_lantikan_excel(xls_bytes: bytes) -> pd.DataFrame:
    # Try sheet names that exist; heuristics for header row
    xl = pd.ExcelFile(xls_bytes)
    sheets = xl.sheet_names
    frames = []
    for sh in sheets:
        df = xl.parse(sh, header=None)
        # find row containing "BIL" and "KOD KURSUS"
        header_row = None
        for i in range(min(10, len(df))):
            row = df.iloc[i].astype(str).str.upper().tolist()
            if "BIL" in row and "KOD KURSUS" in " ".join(row):
                header_row = i
                break
        if header_row is None:
            continue
        hdr = df.iloc[header_row].tolist()
        body = df.iloc[header_row+1:].copy()
        # trim columns to header length
        body = body.iloc[:, :len(hdr)]
        body.columns = [str(h).strip() for h in hdr]
        # normalize expected cols
        rename_map = {}
        for col in list(body.columns):
            up = col.upper().strip()
            if up == "KOD KURSUS" or up.startswith("KOD KURSUS"):
                rename_map[col] = "subject_code"
            elif up == "NAMA KURSUS":
                rename_map[col] = "subject_name"
            elif up == "IN CHARGE":
                rename_map[col] = "role"
            elif up == "NAMA":
                rename_map[col] = "lecturer_name"
            elif "TEMPOH" in up:
                rename_map[col] = "appointment_period"
        body = body.rename(columns=rename_map)
        # keep relevant and drop rows without code or role/name
        keep_cols = ["subject_code","subject_name","role","lecturer_name","appointment_period"]
        for c in keep_cols:
            if c not in body.columns: body[c] = None
        tmp = body[keep_cols].copy()
        tmp["subject_code"] = tmp["subject_code"].astype(str).str.replace(" ","").str.upper().str.replace(" ","")
        tmp["role"] = tmp["role"].astype(str).str.upper().str.strip()
        tmp["lecturer_name"] = tmp["lecturer_name"].astype(str).str.strip()
        tmp["appointment_period"] = tmp["appointment_period"].astype(str).str.strip()
        tmp = tmp[(tmp["subject_code"]!="") & (tmp["lecturer_name"]!="") & (tmp["role"]!="")]
        frames.append(tmp)
    if not frames:
        return pd.DataFrame(columns=["subject_code","subject_name","role","lecturer_name","appointment_period"])
    df_all = pd.concat(frames, ignore_index=True)
    # standardize role to LIC/RP/OTHER
    df_all["role_std"] = df_all["role"].apply(lambda x: "LIC" if "LIC" in x else ("RP" if "RP" in x else x))
    return df_all

