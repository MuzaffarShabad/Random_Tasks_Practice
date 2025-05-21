import os
import glob
import pandas as pd

# === Step 1: Setup ===
main_folder = "main_folder"
columns_to_compare = ['t_date', 'column1', 'column2', 'column3']
sort_columns = ['t_date', 'column1']
sheet1 = 'line_output'
sheet2 = 'line_output_evaluation'

# === Step 2: Collect all matching Excel files ===
excel_files = []
for i in range(1, 17):  # Assuming invoice-1 to invoice-16
    folder_path = os.path.join(main_folder, f"invoice-{i}")
    matches = glob.glob(os.path.join(folder_path, "*_Data_output.xlsx"))
    if matches:
        excel_files.append(matches[0])  # Taking first match if multiple found

# === Step 3: Prepare output writer ===
summary_output = "summary_comparison_output.xlsx"
with pd.ExcelWriter(summary_output, engine='xlsxwriter') as writer:
    for file_path in excel_files:
        try:
            df1 = pd.read_excel(file_path, sheet_name=sheet1)
            df2 = pd.read_excel(file_path, sheet_name=sheet2)

            # Only keep columns that exist in both
            common_columns = [col for col in columns_to_compare if col in df1.columns and col in df2.columns]
            missing_sort = [col for col in sort_columns if col not in common_columns]
            if missing_sort:
                print(f"⚠️ Skipping file '{file_path}': sort columns {missing_sort} missing")
                continue

            df1_filtered = df1[common_columns].copy()
            df2_filtered = df2[common_columns].copy()

            # === Preprocessing
            for col in common_columns:
                if 'date' in col.lower():
                    df1_filtered[col] = pd.to_datetime(df1_filtered[col], errors='coerce')
                    df2_filtered[col] = pd.to_datetime(df2_filtered[col], errors='coerce')
                elif col.lower() == 'price':
                    df1_filtered[col] = pd.to_numeric(df1_filtered[col].astype(str).str.replace(',', ''), errors='coerce')
                    df2_filtered[col] = pd.to_numeric(df2_filtered[col].astype(str).str.replace(',', ''), errors='coerce')
                elif df1_filtered[col].dtype == object or df2_filtered[col].dtype == object:
                    df1_filtered[col] = df1_filtered[col].astype(str).str.lower().str.strip()
                    df2_filtered[col] = df2_filtered[col].astype(str).str.lower().str.strip()

            # === Sort by given sort_columns
            df1_sorted = df1_filtered.sort_values(by=sort_columns).reset_index(drop=True)
            df2_sorted = df2_filtered.sort_values(by=sort_columns).reset_index(drop=True)

            # === Comparison
            comparison_result = pd.DataFrame()
            for col in common_columns:
                comparison_result[f'{col}_match'] = df1_sorted[col] == df2_sorted[col]
                comparison_result[f'{col}_value_1'] = df1_sorted[col]
                comparison_result[f'{col}_value_2'] = df2_sorted[col]

            # === Write to Excel sheet named after the folder
            sheet_name = os.path.basename(os.path.dirname(file_path))[:31]  # Excel limit
            comparison_result.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"✅ Comparison added for {sheet_name}")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

print(f"\n📘 All comparisons saved to: {summary_output}")
