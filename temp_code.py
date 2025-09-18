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

# Load the merged JSON file
with open("merged_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)   # this is a list of dicts

# Extract CLIENT_CASE_ID values
client_case_ids = []
for record in data:
    if "CLIENT_CASE_ID" in record:
        client_case_ids.append(record["CLIENT_CASE_ID"])

# Convert to DataFrame
df = pd.DataFrame(client_case_ids, columns=["CLIENT_CASE_ID"])

# Save to Excel
output_excel = "client_case_ids.xlsx"
df.to_excel(output_excel, index=False)

print(f"✅ Extracted {len(client_case_ids)} CLIENT_CASE_ID values into {output_excel}")

