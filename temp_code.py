import os
import json
import pandas as pd

# Folder where all JSON files are stored
json_folder = './json_data'  # 🔁 Change to your folder path

all_records = []

# Loop over all files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(json_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if "res" in data and isinstance(data["res"], list):
                    all_records.extend(data["res"])
                else:
                    print(f"Skipping {filename} — no 'res' key or wrong format")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

# Convert all records into DataFrame
df = pd.DataFrame(all_records)

# Optional: Fill missing values
df.fillna('', inplace=True)

# Save to Excel
df.to_excel('combined_output.xlsx', index=False)

print("✅ All JSON files merged and saved as 'combined_output.xlsx'")
