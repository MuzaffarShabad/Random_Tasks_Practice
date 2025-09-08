import os
import re
import pandas as pd

def extract_fields_from_folder(folder_path, output_excel="output.xlsx"):
    records = []

    # Regex patterns to capture intent, probability, clientRequestId
    intent_pattern = re.compile(r"'intent':\s*'([^']+)'")
    prob_pattern = re.compile(r"'probability':\s*([\d\.]+)")
    client_id_pattern = re.compile(r"clientReguestld[:\s'\"]+([^\s,'\"]+)")

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    # Extract using regex
                    intent_match = intent_pattern.search(line)
                    prob_match = prob_pattern.search(line)
                    client_id_match = client_id_pattern.search(line)

                    intent = intent_match.group(1) if intent_match else None
                    probability = prob_match.group(1) if prob_match else None
                    client_request_id = client_id_match.group(1) if client_id_match else None

                    if intent or probability or client_request_id:
                        records.append({
                            "intent": intent,
                            "probability": probability,
                            "clientRequestId": client_request_id,
                            "source_file": file_name
                        })

    # Save to Excel
    df = pd.DataFrame(records)
    df.to_excel(output_excel, index=False)
    print(f"✅ Extraction complete. Saved {len(df)} rows to {output_excel}")


# Example usage
folder_path = r"C:\path\to\ndjson\files"
extract_fields_from_folder(folder_path, "intents_output.xlsx")
