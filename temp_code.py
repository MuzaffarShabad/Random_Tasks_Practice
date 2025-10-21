
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
