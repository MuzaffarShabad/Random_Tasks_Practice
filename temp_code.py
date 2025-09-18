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
