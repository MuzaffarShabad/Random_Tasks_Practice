import pandas as pd
import ast
import json

# Load Excel
file_path = "your_file.xlsx"
df = pd.read_excel(file_path)

def normalize_dict(d):
    """Normalize dictionary by sorting keys and stripping spaces"""
    return {k.strip().lower(): str(v).strip() for k, v in d.items()}

def compare_dict_lists(list1, list2):
    """Compare two lists of dicts, return common, only_in_list1, only_in_list2"""
    norm1 = [normalize_dict(d) for d in list1]
    norm2 = [normalize_dict(d) for d in list2]

    # Convert to sets of json strings for comparison (order-independent)
    set1 = {json.dumps(d, sort_keys=True) for d in norm1}
    set2 = {json.dumps(d, sort_keys=True) for d in norm2}

    common = set1 & set2
    only1 = set1 - set2
    only2 = set2 - set1

    # Convert back to list of dicts
    return (
        [json.loads(x) for x in common],
        [json.loads(x) for x in only1],
        [json.loads(x) for x in only2]
    )

# Process row by row
common_list, only5_list, only10_list = [], [], []

for _, row in df.iterrows():
    try:
        # Convert string repr of list of dicts to actual Python objects
        list5 = ast.literal_eval(str(row["output_5"]))
        list10 = ast.literal_eval(str(row["output_10"]))

        common, only5, only10 = compare_dict_lists(list5, list10)
    except Exception as e:
        common, only5, only10 = [], [], []
        print(f"Error parsing row: {e}")

    common_list.append(common)
    only5_list.append(only5)
    only10_list.append(only10)

# Add results to DataFrame
df["common_items"] = common_list
df["only_in_output_5"] = only5_list
df["only_in_output_10"] = only10_list

# Save to new Excel
output_file = "comparison_results.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Comparison done. Results saved in {output_file}")
