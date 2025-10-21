from fastapi import UploadFile, File
import json
import pandas as pd
from datetime import datetime
import os

@app.post("/bulk_intent/")
async def bulk_intent(file: UploadFile = File(...)):
    """
    Process a bulk NDJSON file for Asset Servicing LOB and store all probabilities in JSON + Excel.
    """
    try:
        # Step 1: Read NDJSON file
        content = await file.read()
        lines = content.decode("utf-8").strip().split("\n")

        results = []
        for line in lines:
            try:
                # Parse JSON line
                data = json.loads(line)

                # Default LOB to Asset Servicing
                data["header"] = data.get("header", {})
                data["header"]["lob"] = "Asset Servicing"

                # Extract NLP_CLIENT_CASE_ID if exists
                case_id = None
                if "httpHeaders" in data and "NLP CLIENT CASE ID" in data["httpHeaders"]:
                    case_id = data["httpHeaders"]["NLP CLIENT CASE ID"]

                # Simulate FastAPI Request for handle_intent_request()
                req = Request(scope={"type": "http"})
                req._body = json.dumps(data).encode("utf-8")

                # Call your existing handler
                response = await handle_intent_request(req)

                # Flatten response into dict
                if hasattr(response, "__dict__"):
                    response_dict = response.__dict__
                else:
                    response_dict = response

                # Add case_id to output
                response_dict["NLP_CLIENT_CASE_ID"] = case_id

                results.append(response_dict)

            except Exception as e:
                results.append({
                    "error": str(e),
                    "raw_line": line
                })

        # Step 2: Save output files
        os.makedirs("bulk_output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        json_path = f"bulk_output/bulk_results_{timestamp}.json"
        excel_path = f"bulk_output/bulk_results_{timestamp}.xlsx"

        # Save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        # Save Excel (flatten nested dicts if needed)
        df = pd.json_normalize(results, sep="_")
        df.to_excel(excel_path, index=False)

        return {
            "message": f"Processed {len(results)} records successfully.",
            "json_output": json_path,
            "excel_output": excel_path
        }

    except Exception as e:
        return {"error": f"Failed to process bulk file: {str(e)}"}






uvicorn your_filename:app --reload --port 8092




import requests

# The URL where your Uvicorn server is running
url = "http://localhost:8092/bulk_intent/"

# Path to your NDJSON file
file_path = r"path/to/your/data.ndjson"

# Open the file in binary mode
with open(file_path, "rb") as f:
    files = {"file": (file_path, f, "application/x-ndjson")}
    response = requests.post(url, files=files)

# Print the API response
print("Status Code:", response.status_code)
print("Response:")
print(response.json())






uvicorn your_main_file:app --reload --port 8092


python send_bulk_request.py















































































































def predict_intent_by_model(pre_processed_inquiry, lob):
    if lob == ASSET_SERVICING_LOB:
        model = as_model
    else:
        model = cash_set_mo_model

    # Get prediction and probabilities
    prediction = model.predict(pre_processed_inquiry)
    proba = model.predict_proba(pre_processed_inquiry)[0]  # first sample

    # Get all class labels
    class_labels = model.classes_

    # Combine into dictionary
    all_probabilities = {label: round(prob * 100, 2) for label, prob in zip(class_labels, proba)}

    intent = {
        'sentence': 'N/A',
        'intent': prediction[0],
        'probability': round(max(proba) * 100, 2),
        'all_probabilities': all_probabilities,   # ⬅️ added this line
        'source': 'model'
    }

    return intent
































import os
import json
import requests
import pandas as pd

# URL of your running uvicorn FastAPI service
API_URL = "http://127.0.0.1:8000/intent"

# Folder containing your JSON files
INPUT_FOLDER = "data/json_inputs"
OUTPUT_FOLDER = "data/json_outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# For storing all results in one Excel later
results = []

for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json"):
        file_path = os.path.join(INPUT_FOLDER, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"Processing {filename}...")
        try:
            response = requests.post(API_URL, json=data, timeout=120)
            if response.status_code == 200:
                output = response.json()

                # Save output as JSON file
                output_path = os.path.join(OUTPUT_FOLDER, f"out_{filename}")
                with open(output_path, "w", encoding="utf-8") as out_f:
                    json.dump(output, out_f, indent=2)

                # Optional: Flatten for Excel export
                results.append({
                    "file": filename,
                    "request_id": data.get("735411639"),
                    "message": output.get("message"),
                    "intents": json.dumps(output.get("intents")),
                    "statistics": json.dumps(output.get("statistics")),
                })
            else:
                print(f"Failed for {filename}: {response.status_code}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save summary as Excel
if results:
    df = pd.DataFrame(results)
    df.to_excel(os.path.join(OUTPUT_FOLDER, "intent_summary.xlsx"), index=False)
    print("✅ All done! Results saved to intent_summary.xlsx")
