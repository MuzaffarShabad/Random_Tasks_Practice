import json
import os
import glob

# --- Configuration ---
# IMPORTANT: Change 'your_data_folder' to the actual name of your folder
INPUT_FOLDER = 'your_data_folder' 
OUTPUT_FOLDER = 'extracted_json_bodies'
# ---------------------

def extract_and_save_bodies(input_dir, output_dir):
    """
    Reads all .json files in NDJSON format, extracts the object 
    under the 'body' key, and saves it as a new file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Search for all files with the .json extension
    file_pattern = os.path.join(input_dir, '*.json')
    input_files = glob.glob(file_pattern)

    if not input_files:
        print(f"❌ Error: No .json files found in the directory: {input_dir}")
        return

    record_count = 0
    
    for input_filepath in input_files:
        print(f"\nProcessing file: {os.path.basename(input_filepath)}")
        
        with open(input_filepath, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                if not line.strip():
                    continue
                    
                try:
                    # 1. Parse the NDJSON line
                    record = json.loads(line)
                    
                    # 2. Extract the target object from the 'body' key
                    body_object = record.get("body")
                    
                    # Check if 'body' exists and is a dictionary (JSON object)
                    if not body_object or not isinstance(body_object, dict):
                        # Use diagnostic to help identify potential key issues if needed
                        all_keys = list(record.keys())
                        print(f"  [Warning] Line {line_number}: 'body' not found or not an object.")
                        print(f"  [Diagnostic] Found keys: {all_keys}")
                        print(f"  Skipping record.")
                        continue
                        
                    # 3. Create a unique filename using 'clientRequestId'
                    client_id = body_object.get("clientRequestId", f"record_{record_count+1}")
                    
                    # Clean the client ID to ensure it's a valid filename (e.g., replace spaces/colons)
                    safe_client_id = client_id.replace(':', '_').replace('.', '_').replace(' ', '_')
                    output_filename = f"{safe_client_id}.json"
                    output_filepath = os.path.join(output_dir, output_filename)
                    
                    # 4. Save the extracted object to the new file
                    with open(output_filepath, 'w', encoding='utf-8') as out_f:
                        json.dump(body_object, out_f, indent=4)
                        
                    record_count += 1
                    
                except json.JSONDecodeError as e:
                    print(f"  [Error] Failed to decode JSON on line {line_number} in {os.path.basename(input_filepath)}: {e}")
                except Exception as e:
                    print(f"  [Error] An unexpected error occurred on line {line_number}: {e}")

    print(f"\n--- Processing Complete 🚀 ---")
    print(f"Total objects extracted and saved: {record_count}")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

# Run the process
extract_and_save_bodies(INPUT_FOLDER, OUTPUT_FOLDER)
