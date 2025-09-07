import os
import json
import pandas as pd
import ast

input_folder = "ndjson_files"
all_records = []
bad_records = []

for file_name in os.listdir(input_folder):
    if file_name.endswith(".json") or file_name.endswith(".ndjson"):
        file_path = os.path.join(input_folder, file_name)
        print(f"Processing {file_path}...")

        for enc in ["utf-8", "latin-1"]:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue

                        try:
                            # Try normal JSON first
                            obj = json.loads(line)
                        except Exception:
                            try:
                                # Fallback: try Python dict parsing
                                obj = ast.literal_eval(line)
                            except Exception as e:
                                bad_records.append((file_name, line, str(e)))
                                continue

                        # Add filename for traceability
                        obj["source_file"] = file_name
                        all_records.append(obj)
                break  # stop retrying encodings if success
            except UnicodeDecodeError:
                continue

# Save to Excel
if all_records:
    df = pd.json_normalize(all_records, sep="_")
    df.to_excel("combined_output.xlsx", index=False)
    print("✅ Output saved as combined_output.xlsx")

if bad_records:
    with open("bad_records.log", "w", encoding="utf-8") as f:
        for file_name, line, err in bad_records:
            f.write(f"File: {file_name}\nError: {err}\nLine: {line}\n\n")
    print(f"⚠️ {len(bad_records)} bad records logged in bad_records.log")
