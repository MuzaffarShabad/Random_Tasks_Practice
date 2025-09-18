import pandas as pd
import ast
import json

# Load Excel
file_path = "your_file.xlsx"
df = pd.read_excel(file_path)

def normalize_dict(d):
    """
    Normalize dictionary:
    - Strip spaces from keys/values
    - Lowercase keys
    - Convert values to string
    """
    return {k.strip().lower(): str(v).strip() for k, v in d.items()}

def compare_dict_lists(list1, list2):
    """Compare two lists of dicts, return common, only_in_list1, only_in_list2"""
    # Flatten outer [[]] if needed
    if isinstance(list1, list) and len(list1) == 1 and isinstance(list1[0], list):
        list1 = list1[0]
    if isinstance(list2, list) and len(list2) == 1 and isinstance(list2[0], list):
        list2 = list2[0]

    norm1 = [normalize_dict(d) for d in list1]
    norm2 = [normalize_dict(d) for d in list2]

    # Use sets of JSON strings for comparison
    set1 = {json.dumps(d, sort_keys=True) for d in norm1}
    set2 = {json.dumps(d, sort_keys=True) for d in norm2}

    common = set1 & set2
    only1 = set1 - set2
    only2 = set2 - set1

    return (
        [json.loads(x) for x in common],
        [json.loads(x) for x in only1],
        [json.loads(x) for x in only2],
    )

# Process row by row
common_list, only5_list, only10_list = [], [], []

for _, row in df.iterrows():
    try:
        # Parse safely
        list5 = ast.literal_eval(str(row["output_5"]))
        list10 = ast.literal_eval(str(row["output_10"]))

        common, only5, only10 = compare_dict_lists(list5, list10)
    except Exception as e:
        print(f"⚠️ Error parsing row: {e}")
        common, only5, only10 = [], [], []

    common_list.append(common)
    only5_list.append(only5)
    only10_list.append(only10)

# Add results
df["common_items"] = common_list
df["only_in_output_5"] = only5_list
df["only_in_output_10"] = only10_list

# Save
output_file = "comparison_results.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Comparison done. Results saved in {output_file}")
