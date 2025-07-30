import os
import json
import pandas as pd

# Folder where your JSON files are stored
json_folder = './json_data'  # <-- Change this to your actual folder path
all_data = []

# Read and parse each JSON file
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(json_folder, filename)
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
                # If the JSON file contains a list of dicts
                if isinstance(data, list):
                    all_data.extend(data)
                # If it contains a single dict
                elif isinstance(data, dict):
                    all_data.append(data)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

# Optional: Save the merged JSON (if you want to keep a backup)
with open('merged_output.json', 'w') as f_out:
    json.dump(all_data, f_out, indent=4)

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Fill missing keys with blanks (if any file has different keys)
df.fillna('', inplace=True)

# Export to Excel
df.to_excel('merged_output.xlsx', index=False)

print("✅ Done! JSON values saved to 'merged_output.xlsx' with keys as column headers.")
