import os

input_folder = "ndjson_files"   # folder containing NDJSON files
output_file = "merged_output.ndjson"

with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):  # or ".ndjson"
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as infile:
                for line in infile:
                    line = line.strip()
                    if line:  # avoid blank lines
                        outfile.write(line + "\n")

print(f"✅ All NDJSON files merged into {output_file}")
