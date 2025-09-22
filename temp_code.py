import os
import json
import re
import pandas as pd

# 🔹 Folder containing your NDJSON .json files
INPUT_FOLDER = "ndjson_files"
OUTPUT_FILE = "intent_results.xlsx"

records = []

def clean_json_string(s):
    """Try to fix common JSON formatting issues in your files"""
    s = s.replace("(", "{").replace(")", "}")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("'", '"')
    s = re.sub(r",\s*}", "}", s)   # remove trailing commas
    s = re.sub(r",\s*]", "]", s)
    return s

# 🔹 Loop through all .json files
for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".json"):
        filepath = os.path.join(INPUT_FOLDER, file)
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    clean_line = clean_json_string(line)
                    data = json.loads(clean_line)

                    # Extract fields safely
                    intent = None
                    prob = None
                    client_req_id = data.get("clientRequestId", None)

                    intents_section = data.get("intents", {})
                    for _, intent_block in intents_section.items():
                        if isinstance(intent_block, dict):
                            inner_intent = intent_block.get("intent", {})
                            if isinstance(inner_intent, dict):
                                if inner_intent.get("intent"):
                                    intent = inner_intent.get("intent")
                                    prob = inner_intent.get("probability")
                                    break

                    records.append({
                        "filename": file,
                        "intent": intent,
                        "probability": prob,
                        "clientRequestId": client_req_id
                    })

                except Exception as e:
                    print(f"⚠️ Could not parse line in {file}: {e}")
                    continue

# 🔹 Save to Excel
df = pd.DataFrame(records)
df.to_excel(OUTPUT_FILE, index=False)

print(f"✅ Done. Extracted {len(df)} records. Results saved to {OUTPUT_FILE}")
