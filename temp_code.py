import os
import json
import pandas as pd
import re

input_folder = "ndjson_files"
all_records = []
bad_records = []

# Simple regex: starts with { and ends with }
json_pattern = re.compile(r'^\s*\{.*\}\s*$')

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

                        # Quick regex check: only attempt if it looks like JSON
                        if not json_pattern.match(line):
                            bad_records.append((file_name, line, "Regex fail"))
                            continue

                        # Fix common JSON issues
                        fixed_line = (
                            line.replace("'", '"')
                                .replace("None", '"None"')
                                .replace("True", "true")
                                .replace("False", "false")
                                .rstrip(",")
                        )

                        try:
                            obj = json.loads(fixed_line)
                            obj["source_file"] = file_name
                            all_records.append(obj)
                        except json.JSONDecodeError as e:
                            bad_records.append((file_name, line, str(e)))
                break  # Stop after first successful encoding
            except UnicodeDecodeError:
                continue

# Save good records
if all_records:
    df = pd.json_normalize(all_records, sep="_")
    df.to_excel("combined_output.xlsx", index=False)
    print("✅ All NDJSON files processed. Output saved as combined_output.xlsx")

# Save bad records for manual review
if bad_records:
    with open("bad_records.log", "w", encoding="utf-8") as f:
        for file_name, line, err in bad_records:
            f.write(f"File: {file_name}\nError: {err}\nLine: {line}\n\n")
    print(f"⚠️ {len(bad_records)} bad records skipped. See bad_records.log for details.")
