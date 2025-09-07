import json
import pandas as pd

records = []

# ---- Step 1: Read line by line ----
with open("input.json", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():  # skip blank lines
            obj = json.loads(line)
            records.append(obj)

# ---- Step 2: Flatten nested JSON ----
df = pd.json_normalize(records, sep="_")

# ---- Step 3: Save to Excel ----
df.to_excel("output.xlsx", index=False)

print("✅ JSON file converted to Excel → output.xlsx")
