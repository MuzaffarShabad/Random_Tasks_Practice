import json
import os
import glob

# --- Configuration ---
# IMPORTANT: Change 'your_data_folder' to the actual name of your folder
INPUT_FOLDER = 'your_data_folder' 
OUTPUT_FOLDER = 'extracted_json_bodies'

# --- NEW: Key-Value Pair and its EXACT STRUCTURE and DESTINATION ---
NEW_KEY = "LOB"
NEW_VALUE = ["as"] # Note: The value is now a list
TARGET_NESTED_KEY_1 = "header"
TARGET_NESTED_KEY_2 = "metadata"
# -------------------------------------------------------------------

def extract_and_save_bodies_with_lob_in_metadata(input_dir, output_dir, key, value, target_key_1, target_key_2):
    """
    Reads all .json files in NDJSON format, extracts the object 
    under the 'body' key, and adds the specified key-value pair into the nested 'metadata' object.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

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
                    
                    if not body_object or not isinstance(body_object, dict):
                        print(f"  [Warning] Line {line_number}: 'body' not found or not an object. Skipping.")
                        continue
                    
                    # 3. TRAVERSE TO THE TARGET LOCATION (header -> metadata)
                    
                    # Level 1: Get the 'header'
                    header_object = body_object.get(target_key_1)
                    if not header_object or not isinstance(header_object, dict):
                         print(f"  [Warning] Line {line_number}: Target key '{target_key_1}' not found or not an object. Skipping key addition.")
                         continue
                            
                    # Level 2: Get the 'metadata'
                    metadata_object = header_object.get(target_key_2)
                    if not metadata_object or not isinstance(metadata_object, dict):
                         print(f"  [Warning] Line {line_number}: Target key '{target_key_2}' not found or not an object inside '{target_key_1}'. Skipping key addition.")
                         continue

                    # 4. INSERT THE NEW KEY-VALUE PAIR INTO 'metadata'
                    metadata_object[key] = value
                    
                    # 5. Create a unique filename using 'clientRequestId'
                    client_id = body_object.get("clientRequestId", f"record_{record_count+1}")
                    
                    # Clean the client ID for a safe filename
                    safe_client_id = client_id.replace(':', '_').replace('.', '_').replace(' ', '_')
                    output_filename = f"{safe_client_id}.json"
                    output_filepath = os.path.join(output_dir, output_filename)
                    
                    # 6. Save the modified object to the new file
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
extract_and_save_bodies_with_lob_in_metadata(
    INPUT_FOLDER, OUTPUT_FOLDER, NEW_KEY, NEW_VALUE, TARGET_NESTED_KEY_1, TARGET_NESTED_KEY_2
)
