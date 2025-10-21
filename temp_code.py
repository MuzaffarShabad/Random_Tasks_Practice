import json
import os
import glob
from urllib.parse import unquote

# --- Configuration ---
INPUT_FOLDER = 'your_ndjson_folder' # Change this to your folder name
OUTPUT_FOLDER = 'extracted_json_bodies'
# ---------------------

def process_ndjson_files(input_dir, output_dir):
    """
    Reads all NDJSON files in the input directory, extracts the 'body' object
    from each line, and saves it as an individual JSON file in the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Use glob to find all files ending with .ndjson or .json in the input folder
    file_pattern = os.path.join(input_dir, '*.ndjson')
    ndjson_files = glob.glob(file_pattern)

    if not ndjson_files:
        print(f"No .ndjson files found in the directory: {input_dir}")
        return

    record_count = 0
    
    for input_filepath in ndjson_files:
        print(f"\nProcessing file: {os.path.basename(input_filepath)}")
        
        with open(input_filepath, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                try:
                    # 1. Parse the NDJSON line into a Python dictionary
                    record = json.loads(line)
                    
                    # 2. Extract the 'body' object
                    # We expect the 'body' key to contain the target structure.
                    # Your sample shows it as a list with one item, but the object
                    # you want to save is *inside* that list/value. We will
                    # assume the structure is: {"body": [ { ...the object you want... } ]}
                    
                    # Safely get the 'body' value, which is expected to be a list
                    body_list = record.get("body")
                    
                    if not body_list or not isinstance(body_list, list):
                        print(f"  [Warning] Line {line_number}: 'body' not found or not a list. Skipping.")
                        continue
                        
                    # The object you want is the first (and perhaps only) item in the list
                    body_object = body_list[0] 
                    
                    # 3. Create a unique filename for the output JSON
                    # We can use 'clientRequestId' if it exists, otherwise use a counter
                    client_id = body_object.get("clientRequestld", f"record_{record_count+1}")
                    output_filename = f"{client_id}.json"
                    output_filepath = os.path.join(output_dir, output_filename)
                    
                    # 4. Save the extracted body object to a new file
                    with open(output_filepath, 'w', encoding='utf-8') as out_f:
                        # Use json.dump for pretty-printing and readability
                        json.dump(body_object, out_f, indent=4)
                        
                    record_count += 1
                    
                except json.JSONDecodeError as e:
                    print(f"  [Error] Failed to decode JSON on line {line_number} in {os.path.basename(input_filepath)}: {e}")
                except Exception as e:
                    print(f"  [Error] An unexpected error occurred on line {line_number}: {e}")

    print(f"\n--- Processing Complete ---")
    print(f"Total objects extracted and saved: {record_count}")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

# Run the process
process_ndjson_files(INPUT_FOLDER, OUTPUT_FOLDER)
