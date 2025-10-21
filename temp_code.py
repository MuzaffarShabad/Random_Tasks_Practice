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
    Reads all .json files in NDJSON format, extracts the first object 
    inside the 'body' list, and saves it as a new file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Search for all files with the .json extension in the input folder
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
                # Skip any empty lines
                if not line.strip():
                    continue
                    
                try:
                    # 1. Parse the NDJSON line (one complete JSON object)
                    record = json.loads(line)
                    
                    # 2. Extract the target object from the 'body' list
                    body_list = record.get("body")
                    
                    # Ensure 'body' exists, is a list, and isn't empty
                    if not body_list or not isinstance(body_list, list) or not body_list:
                        print(f"  [Warning] Line {line_number}: 'body' not found, empty, or not a list. Skipping.")
                        continue
                        
                    # The object you want to save is the FIRST item in the list
                    body_object = body_list[0] 
                    
                    # 3. Create a unique filename
                    # We use 'clientRequestld' for a stable, unique name
                    client_id = body_object.get("clientRequestld", f"record_{record_count+1}")
                    output_filename = f"{client_id}.json"
                    output_filepath = os.path.join(output_dir, output_filename)
                    
                    # 4. Save the extracted object to the new file
                    with open(output_filepath, 'w', encoding='utf-8') as out_f:
                        # Use indent=4 for a clean, readable JSON format
                        json.dump(body_object, out_f, indent=4)
                        
                    record_count += 1
                    
                except json.JSONDecodeError as e:
                    print(f"  [Error] Failed to decode JSON on line {line_number} in {os.path.basename(input_filepath)}. Check for malformed JSON structure: {e}")
                except Exception as e:
                    print(f"  [Error] An unexpected error occurred on line {line_number}: {e}")

    print(f"\n--- Processing Complete 🚀 ---")
    print(f"Total objects extracted and saved: {record_count}")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

# Run the process
extract_and_save_bodies(INPUT_FOLDER, OUTPUT_FOLDER)
