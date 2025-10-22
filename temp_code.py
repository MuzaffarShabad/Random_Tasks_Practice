import json
import requests
import pandas as pd
import os
import glob

# --- Configuration ---
API_URL = "http://127.0.0.1:8092/intent"
INPUT_FOLDER = r"C:\Projects_Local_Small_Tasks\extracted_json_bodies_1" # Folder containing your JSON files
OUTPUT_FILE = "combined_api_responses.xlsx"
# ---------------------

def process_json_folder_to_excel(input_dir, api_url, output_file):
    """
    Sends each JSON file in the input directory to the API endpoint,
    collects the responses, and saves them to a single Excel file.
    """
    
    # 1. Find all JSON files in the input folder
    file_pattern = os.path.join(input_dir, '*.json')
    json_files = glob.glob(file_pattern)

    if not json_files:
        print(f"❌ Error: No .json files found in the directory: {input_dir}")
        return

    all_responses = []
    success_count = 0
    
    print(f"Found {len(json_files)} files to process. Starting API calls...")

    # 2. Iterate through each file and send the POST request
    for file_path in json_files:
        file_name = os.path.basename(file_path)
        print(f"  Processing: {file_name}...")
        
        try:
            # Load the JSON data from the file
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Send data to FastAPI
            response = requests.post(api_url, json=data)
            
            # Raise an HTTPError if the status code is 4xx or 5xx
            response.raise_for_status() 

            # Get the JSON response from the API
            json_response = response.json()
            
            # --- IMPORTANT: Standardize the response structure ---
            # FastAPI often returns a list of objects or a single object.
            # We assume it returns a list or a dictionary. If it returns a list, 
            # we extend the main list; if it returns a dictionary, we append it.
            if isinstance(json_response, list):
                all_responses.extend(json_response)
            elif isinstance(json_response, dict):
                all_responses.append(json_response)
            else:
                print(f"  [Warning] API response for {file_name} was unexpected type ({type(json_response)}). Skipping.")
                continue

            success_count += 1
            
        except FileNotFoundError:
            print(f"  [Error] File not found: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"  [Error] API call failed for {file_name}. Status: {response.status_code if 'response' in locals() else 'N/A'}. Error: {e}")
        except json.JSONDecodeError:
            print(f"  [Error] Failed to decode JSON from API response for {file_name}.")
        except Exception as e:
            print(f"  [Error] An unexpected error occurred while processing {file_name}: {e}")

    print(f"\n--- Processing Complete ---")
    print(f"Successfully received {success_count} responses.")
    
    # 3. Create DataFrame and Export to Excel
    if all_responses:
        try:
            # Create a Pandas DataFrame from the list of dictionaries
            df = pd.DataFrame(all_responses)
            
            # Export to Excel
            df.to_excel(output_file, index=False)
            print(f"✅ Success! All data combined and exported to: {os.path.abspath(output_file)}")
        except Exception as e:
            print(f"❌ Error: Failed to create or export Excel file: {e}")
    else:
        print("No valid responses were collected. Excel file not created.")

# Execute the main function
process_json_folder_to_excel(INPUT_FOLDER, API_URL, OUTPUT_FILE)
