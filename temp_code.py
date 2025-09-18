import pandas as pd
import json
import re

file_path = r"C:\Users\shaba\OneDrive\Desktop\sample.xlsx"
df = pd.read_excel(file_path)

def clean_and_parse(cell_value):
    if pd.isna(cell_value):
        return []
    text = str(cell_value)

    # Fix quotes (turn all into double quotes)
    text = text.replace("'", '"')

    # Fix common errors like "}, {"
    text = re.sub(r'(\w)"(\s*:)', r'\1"\2', text)  

    # Remove trailing commas/spaces
    text = text.strip()

    # Ensure it looks like a list
    if not text.startswith("["):
        text = "[" + text
    if not text.endswith("]"):
        text = text + "]"

    try:
        return json.loads(text)
    except Exception as e:
        print("⚠️ Bad record:", e, "\n", text[:200])
        return []

def normalize_dict(d):
    return {k.strip().lower(): str(v).strip() for k, v in d.items()}

def compare_dict_lists(list1, list2):
    # Flatten if nested
    flat1 = []
    for x in list1:
        flat1.extend(x if isinstance(x, list) else [x])
    flat2 = []
    for x in list2:
        flat2.extend(x if isinstance(x, list) else [x])

    norm1 = [normalize_dict(d) for d in flat1 if isinstance(d, dict)]
    norm2 = [normalize_dict(d) for d in flat2 if isinstance(d, dict)]

    set1 = {json.dumps(d, sort_keys=True) for d in norm1}
    set2 = {json.dumps(d, sort_keys=True) for d in norm2}

    common = [json.loads(x) for x in set1 & set2]
    only1 = [json.loads(x) for x in set1 - set2]
    only2 = [json.loads(x) for x in set2 - set1]

    return common, only1, only2

common_list, only5_list, only10_list = [], [], []

for _, row in df.iterrows():
    list5 = clean_and_parse(row["output_5"])
    list10 = clean_and_parse(row["output_10"])

    common, only5, only10 = compare_dict_lists(list5, list10)

    common_list.append(common)
    only5_list.append(only5)
    only10_list.append(only10)

df["common_items"] = common_list
df["only_in_output_5"] = only5_list
df["only_in_output_10"] = only10_list

df.to_excel("comparison_results.xlsx", index=False)
print("✅ Done. Results saved to comparison_results.xlsx")
