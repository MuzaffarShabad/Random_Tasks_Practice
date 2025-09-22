import os
import re
import pandas as pd

def extract_with_regex(folder_path, output_excel="asset_servicing_output.xlsx"):
    records = []

    # Regex patterns for intent, probability, and clientRequestId
    intent_pattern = re.compile(r'"intent"\s*:\s*"([^"]+)"', re.IGNORECASE)
    prob_pattern = re.compile(r'"probability"\s*:\s*([\d.]+)', re.IGNORECASE)
    client_id_pattern = re.compile(r'"clientRequestId"\s*:\s*"([^"]+)"', re.IGNORECASE)

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        # Find all intents
                        intents = intent_pattern.findall(line)
                        probs = prob_pattern.findall(line)
                        client_ids = client_id_pattern.findall(line)

                        # Pair them safely
                        for i, intent in enumerate(intents):
                            prob = probs[i] if i < len(probs) else None
                            client_id = client_ids[0] if client_ids else None
                            records.append({
                                "intent": intent,
                                "probability": prob,
                                "clientRequestId": client_id,
                                "source_file": file_name
                            })
                    except Exception as e:
                        print(f"Skipping bad line in {file_name}: {e}")
                        continue

    # Save to Excel
    df = pd.DataFrame(records)
    df.to_excel(output_excel, index=False)
    print(f"✅ Regex extraction complete. Saved {len(df)} rows to {output_excel}")


# Example usage
folder_path = r"C:\path\to\ndjson\files"
extract_with_regex(folder_path, "asset_servicing_regex_output.xlsx")
