import os
import json

input_folder = "ndjson_files"   # folder containing NDJSON files
output_file = "merged_output.json"

all_records = []

for filename in os.listdir(input_folder):
    if filename.endswith(".json") or filename.endswith(".ndjson"):
        file_path = os.path.join(input_folder, filename)
        with open(file_path, "r", encoding="utf-8") as infile:
            for line in infile:
                line = line.strip()
                if line:  # avoid blank lines
                    try:
                        record = json.loads(line)  # parse each NDJSON line
                        all_records.append(record)
                    except json.JSONDecodeError:
                        print(f"⚠️ Skipping invalid JSON line in {filename}: {line[:50]}...")

# Save all records into a single JSON array
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(all_records, outfile, indent=2, ensure_ascii=False)

print(f"✅ Merged {len(all_records)} records into {output_file}")






import os
import json
import pandas as pd

# Paths
input_folder = "ndjson_files"       # parent folder where ndjson/json files are stored
merged_file = "merged_output.json"  # previously created merged file
output_excel = "client_case_ids.xlsx"

# Step 1: Load merged JSON records
with open(merged_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Step 2: Traverse again through original files to find source
results = []
for subdir, dirs, files in os.walk(input_folder):
    for filename in files:
        if filename.endswith(".json") or filename.endswith(".ndjson"):
            file_path = os.path.join(subdir, filename)
            with open(file_path, "r", encoding="utf-8") as infile:
                for line in infile:
                    line = line.strip()
                    if line:
                        try:
                            record = json.loads(line)
                            if "CLIENT_CASE_ID" in record:
                                results.append({
                                    "CLIENT_CASE_ID": record["CLIENT_CASE_ID"],
                                    "Source_File": filename,
                                    "Subdirectory": os.path.relpath(subdir, input_folder)
                                })
                        except json.JSONDecodeError:
                            continue

# Step 3: Save to Excel
df = pd.DataFrame(results)
df.to_excel(output_excel, index=False)

print(f"✅ Extracted {len(results)} CLIENT_CASE_ID values into {output_excel}")

