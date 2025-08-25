import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote

def extract_text_tables_html(json_body, json_subject, col_mapping):
    # Clean up HTML body
    json_body = unquote(json_body).replace("+", " ")
    soup = BeautifulSoup(json_body, "html.parser")
    json_subject_normalized = json_subject.replace("-", " ")

    # Remove tables for plain text extraction
    for table in soup.find_all("table"):
        table.decompose()

    text = soup.get_text(separator="\n").strip()
    text = text.replace("\t", "\n")
    text = "\n".join([line.lstrip() for line in text.splitlines()])

    # Extract all tables
    try:
        tables = pd.read_html(json_body, header=None)
    except Exception as ex:  # Raised when no tables are found
        print(f"No tables found: {ex}")
        tables = []

    processed_tables = []
    for df in tables:
        # --- Detect horizontal table (key-value style) ---
        if df.shape[1] in [2, 3]:
            keys = df.iloc[:, 0].astype(str).str.replace(":", "").str.strip().str.lower()
            values = df.iloc[:, -1].astype(str).str.strip()
            df = pd.DataFrame([values.values], columns=keys.values)

        # --- Extended header scan (up to 5 rows/cols) ---
        max_check_rows = min(5, df.shape[0])   # check up to 5 rows
        max_check_cols = min(5, df.shape[1])   # check up to 5 cols

        row_cols, header_row_idx = [], None
        for r in range(max_check_rows):
            candidate = df.iloc[r, :].astype(str).str.strip().tolist()
            row_cols = get_valid_cols(candidate, col_mapping)
            if row_cols:
                header_row_idx = r
                break

        column_cols, header_col_idx = [], None
        for c in range(max_check_cols):
            candidate = df.iloc[:, c].astype(str).str.strip().tolist()
            column_cols = get_valid_cols(candidate, col_mapping)
            if column_cols:
                header_col_idx = c
                break

        # --- Handle detection results ---
        if row_cols:
            df.columns = df.iloc[header_row_idx]
            df = df.drop(index=header_row_idx).reset_index(drop=True)
        elif column_cols:
            df.index = df.iloc[:, header_col_idx]
            df = df.drop(columns=header_col_idx).reset_index(drop=True)
        else:
            print("⚠️ No valid headers found in first 5 rows/cols")

        processed_tables.append(df)

    return json_subject_normalized + text, processed_tables
