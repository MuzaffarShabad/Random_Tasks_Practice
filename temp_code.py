import os
import json

# Folder containing your JSON files
json_folder = './json_data'   # Change this to your folder path

# Master list to hold all data
merged_data = []

# Loop through all files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(json_folder, filename)
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    merged_data.append(data)
            except Exception as e:
                print(f"⚠️ Error reading {filename}: {e}")

# Save to master.json
output_file = 'master.json'
with open(output_file, 'w') as out_f:
    json.dump(merged_data, out_f, indent=4)

print(f"✅ Merged {len(merged_data)} records into {output_file}")
