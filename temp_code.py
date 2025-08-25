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
            df = pd.DataFrame([values.values], columns=keys.values)
            all_df = pd.concat([all_df, df], ignore_index=True)
            continue   # Skip normal processing for horizontal tables
        # ---------------------------------------------------

        # Try detecting valid columns/rows
        column_cols = get_valid_cols(
            list(df.iloc[:, 0].astype(str).str.replace(":", "").str.strip().str.lower()), 
            max_dist, col_mapping
        )
        row_cols = get_valid_cols(
            list(df.iloc[0].astype(str).str.replace(":", "").str.strip().str.lower()), 
            max_dist, col_mapping
        )

        if len(row_cols) == 0 and len(column_cols) == 0:
            print("Both row and col are zero")

        elif len(row_cols) < len(column_cols):
            print("Length of row < col, doing transpose", len(row_cols), len(column_cols))
            df = df.transpose().reset_index(drop=True)
            valid_cols = column_cols
            print("Table after transpose:\n", df)
        else:
            valid_cols = row_cols

        # First row as header
        df.columns = list(df.iloc[0].astype(str).str.replace(":", "").str.strip().str.lower())
        df = df[1:].reset_index(drop=True)

        # Rename + deduplicate
        rename_cols = get_priority_cols(valid_cols)
        df = df[list(rename_cols.keys())]
        df = df.loc[:, ~df.columns.duplicated()]
        if not df.empty:
            df.rename(columns=rename_cols, inplace=True)

        all_df = pd.concat([all_df, df], ignore_index=True)

    return all_df.dropna(how='all').reset_index(drop=True).dropna(how='all', axis=1)
