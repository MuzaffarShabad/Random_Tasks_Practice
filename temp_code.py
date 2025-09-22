import os
import re
import pandas as pd

def extract_asset_servicing_regex(folder_path, output_excel="asset_servicing_output.xlsx"):
    records = []

    # Regex to isolate the ASSET_SERVICING block
    asset_servicing_block = re.compile(r'ASSET[_\s]?SERVICING.*?}(?=[},]|$)', re.IGNORECASE | re.DOTALL)

    # Regex patterns inside ASSET_SERVICING
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
                        # First isolate ASSET_SERVICING section
                        asset_blocks = asset_servicing_block.findall(line)

                        for block in asset_blocks:
                            intents = intent_pattern.findall(block)
                            probs = prob_pattern.findall(block)

                            # ClientRequestId usually outside ASSET_SERVICING, check full line
                            client_ids = client_id_pattern.findall(line)

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
    print(f"✅ Extraction complete. Saved {len(df)} rows to {output_excel}")


# Example usage
folder_path = r"C:\path\to\ndjson\files"
extract_asset_servicing_regex(folder_path, "asset_servicing_regex_output.xlsx")
