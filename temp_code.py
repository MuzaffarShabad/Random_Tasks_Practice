import os
import re
import pandas as pd

# 📂 Folder containing NDJSON files
folder_path = "path/to/your/folder"

records = []

# Regex patterns for extracting fields
intent_pattern = re.compile(r"'intent':\s*'([^']+)'", re.IGNORECASE)
prob_pattern = re.compile(r"'probability':\s*([\d.]+)", re.IGNORECASE)
client_pattern = re.compile(r"clientRequestld[:\s*'\*]+([A-Za-z0-9._-]+)")

for file_name in os.listdir(folder_path):
    if file_name.endswith(".ndjson"):
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # skip empty lines
                
                # Extract values
                intent_match = intent_pattern.search(line)
                prob_match = prob_pattern.search(line)
                client_match = client_pattern.search(line)

                intent_val = intent_match.group(1) if intent_match else None
                prob_val = float(prob_match.group(1)) if prob_match else None
                client_id = client_match.group(1) if client_match else None

                # Save only if found
                if intent_val or prob_val or client_id:
                    records.append({
                        "intent": intent_val,
                        "probability": prob_val,
                        "clientRequestId": client_id,
                        "file": file_name
                    })

# Convert to DataFrame
df = pd.DataFrame(records)

# Save to Excel
output_file = "extracted_intents.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Extracted {len(df)} rows and saved to {output_file}")
