def get_final_table(tables, col_mapping, max_dist=2):
    all_df = pd.DataFrame()

    for df in tables:
        # Ensure columns are numeric indices
        if 0 not in df.columns:
            df = pd.concat([pd.DataFrame(data=[df.columns], dtype=str), df], ignore_index=True)
            df.columns = range(len(df.columns))

        # --- 🔹 Detect horizontal (key-value style) tables ---
        if df.shape[1] in [2, 3]:  
            keys = df.iloc[:, 0].astype(str).str.replace(":", "").str.strip().str.lower()
            values = df.iloc[:, -1].astype(str).str.strip()

            # Convert to single-row DataFrame
            df = pd.DataFrame([values.values], columns=keys.values)
            all_df = pd.concat([all_df, df], ignore_index=True)
            continue   # Skip normal processing for horizontal tables
        # ---------------------------------------------------

        # --- 🔹 Extended header detection (check up to 5 rows/cols) ---
        max_check_rows = min(5, df.shape[0])   # check up to 5 rows
        max_check_cols = min(5, df.shape[1])   # check up to 5 columns

        row_cols, column_cols = [], []
        header_row_idx, header_col_idx = None, None

        # Try rows as header
        for r in range(max_check_rows):
            candidate = df.iloc[r, :].astype(str).str.replace(":", "").str.strip().tolist()
            row_cols = get_valid_cols(candidate, max_dist, col_mapping)
            if row_cols:   # stop if valid headers found
                header_row_idx = r
                break

        # Try columns as header
        for c in range(max_check_cols):
            candidate = df.iloc[:, c].astype(str).str.replace(":", "").str.strip().tolist()
            column_cols = get_valid_cols(candidate, max_dist, col_mapping)
            if column_cols:   # stop if valid headers found
                header_col_idx = c
                break
        # ------------------------------------------------------------

        # --- 🔹 Handle cases ---
        if len(row_cols) == 0 and len(column_cols) == 0:
            print("⚠️ Both row and col are zero, skipping table")
            continue

        elif len(row_cols) < len(column_cols):
            print(f"↔️ Row < Col, doing transpose ({len(row_cols)} < {len(column_cols)})")
            df = df.transpose().reset_index(drop=True)
            valid_cols = column_cols
        else:
            valid_cols = row_cols

        # --- 🔹 Assign header row ---
        if header_row_idx is not None:
            header = df.iloc[header_row_idx].astype(str).str.replace(":", "").str.strip().str.lower()
            df = df[header_row_idx + 1:].reset_index(drop=True)
        else:
            header = df.iloc[0].astype(str).str.replace(":", "").str.strip().str.lower()
            df = df[1:].reset_index(drop=True)

        df.columns = header

        # --- 🔹 Rename + deduplicate ---
        rename_cols = get_priority_cols(valid_cols)
        df = df[list(rename_cols.keys())]  # keep only mapped columns
        df = df.loc[:, ~df.columns.duplicated()]  # drop duplicates
        if not df.empty:
            df.rename(columns=rename_cols, inplace=True)

        all_df = pd.concat([all_df, df], ignore_index=True)

    # Final cleanup
    return all_df.dropna(how='all').reset_index(drop=True).dropna(how='all', axis=1)
