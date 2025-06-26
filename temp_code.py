import pandas as pd

def expand_ast_value(data, out_df=True, return_first_only=False):
    if len(data) == 0:
        return pd.DataFrame() if out_df else {}

    # Step 1: Remove empty string entries from each list
    cleaned_data = {
        k: [val for val in v if val != ''] for k, v in data.items()
    }

    # Step 2: Check if all lists are now empty
    if all(len(v) == 0 for v in cleaned_data.values()):
        return pd.DataFrame() if out_df else {}

    # Step 3: Find max length of remaining lists
    max_length = max(len(v) for v in cleaned_data.values())

    # Step 4: Expand each list
    expanded_data = {
        k: v + [v[-1]] * (max_length - len(v)) if v else [None] * max_length
        for k, v in cleaned_data.items()
    }

    # Step 5: If return_first_only is True, return only first element per key
    if return_first_only:
        first_only_data = {k: v[0] for k, v in expanded_data.items() if v}
        return first_only_data

    # Step 6: Return DataFrame or expanded dict
    return pd.DataFrame(expanded_data) if out_df else expanded_data
