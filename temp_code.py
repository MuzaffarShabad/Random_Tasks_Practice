import os
import json
import pandas as pd
import re

def clean_json(line: str) -> str:
    """
    Cleans up a malformed NDJSON line:
    - Replace single quotes with double quotes
    - Remove stray * or unicode escapes
    - Ensure proper commas
    """
    line = line.strip()

    # Replace single quotes with double quotes carefully
    line = re.sub(r"'", '"', line)

    # Fix trailing commas before closing braces/brackets
    line = re.sub(r",\s*}", "}", line)
    line = re.sub(r",\s*]", "]", line)

    # Remove stray asterisks or unicode placeholders
    line = line.replace("*", "").replace("u200a", "")

    return line


def extract_cash_office_intents(folder_path, output_excel="output_cash_office.xlsx"):
    """
    Extracts intent/probability/clientRequestId from CASH_SET_MIDDLE_OFFICE section.
    """
    records = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        cleaned = clean_json(line)
                        data = json.loads(cleaned)

                        intents = data.get("intents", {})
                        cash_office = intents.get("CASH_SET_MIDDLE_OFFICE", {})
                        intent_info = cash_office.get("intent", {})

                        intent = intent_info.get("intent", None)
                        probability = intent_info.get("probability", None)
                        client_request_id = data.get("clientReguestld", None) or data.get("clientRequestId", None)

                        records.append({
                            "intent": intent,
                            "probability": probability,
                            "clientRequestId": client_request_id,
                            "source_file": file_name
                        })

                    except Exception as e:
                        print(f"Skipping bad line in {file_name}: {e}")
                        continue

    df = pd.DataFrame(records)
    df.to_excel(output_excel, index=False)
    print(f"✅ CASH office extraction complete. Saved {len(df)} rows to {output_excel}")


def extract_asset_servicing_intents(folder_path, output_excel="output_asset_servicing.xlsx"):
    """
    Extracts specifically 'Payment Incorrect/Missing' intent with probability
    and clientRequestId from ASSET_SERVICING section.
    """
    records = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        cleaned = clean_json(line)
                        data = json.loads(cleaned)

                        intents = data.get("intents", {})
                        asset_servicing = intents.get("ASSET SERVICING", {})
                        intent_info = asset_servicing.get("intent", {})

                        intent = intent_info.get("intent", None)
                        probability = intent_info.get("probability", None)
                        client_request_id = data.get("clientReguestld", None) or data.get("clientRequestId", None)

                        # Only store if it's the Payment Incorrect/Missing intent
                        if intent and "Payment Incorrect/Missing" in intent:
                            records.append({
                                "intent": intent,
                                "probability": probability,
                                "clientRequestId": client_request_id,
                                "source_file": file_name
                            })

                    except Exception as e:
                        print(f"Skipping bad line in {file_name}: {e}")
                        continue

    df = pd.DataFrame(records)
    df.to_excel(output_excel, index=False)
    print(f"✅ Asset Servicing extraction complete. Saved {len(df)} rows to {output_excel}")


# Example usage:
folder_path = r"C:\path\to\ndjson\files"
extract_cash_office_intents(folder_path, "cash_office_output.xlsx")
extract_asset_servicing_intents(folder_path, "asset_servicing_output.xlsx")
