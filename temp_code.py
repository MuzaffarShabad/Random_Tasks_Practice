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






import json
import pandas as pd

# Input/output files
merged_file = "merged_output.json"
output_excel = "client_case_ids.xlsx"

# Load merged JSON
with open(merged_file, "r", encoding="utf-8") as f:
    records = json.load(f)

# Extract CLIENT_CASE_ID from httpHeaders
results = []
for rec in records:
    http_headers = rec.get("httpHeaders", {})
    client_case_id = http_headers.get("CLIENT_CASE_ID")
    if client_case_id:
        results.append({"CLIENT_CASE_ID": client_case_id})

# Convert to DataFrame and save to Excel
df = pd.DataFrame(results)
df.to_excel(output_excel, index=False)

print(f"✅ Extracted {len(results)} CLIENT_CASE_ID values into {output_excel}")
