import os
import json
import pandas as pd

input_folder = "ndjson_files"   # 🔹 your folder name
all_records = []

# ---- Step 1: Loop through all files in folder ----
for file_name in os.listdir(input_folder):
    if file_name.endswith(".json") or file_name.endswith(".ndjson"):
        file_path = os.path.join(input_folder, file_name)
        print(f"Processing {file_path}...")

        # ---- Step 2: Read file line by line (NDJSON format) ----
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        obj = json.loads(line)
                        obj["source_file"] = file_name   # keep track of file source
                        all_records.append(obj)
                    except json.JSONDecodeError as e:
                        print(f"❌ Error parsing {file_name}: {e}")

# ---- Step 3: Flatten nested JSON ----
df = pd.json_normalize(all_records, sep="_")

# ---- Step 4: Save to Excel ----
df.to_excel("combined_output.xlsx", index=False)

print("✅ All NDJSON files processed. Output saved as combined_output.xlsx")
