from bs4 import BeautifulSoup
import pandas as pd
from fuzzywuzzy import process
from Levenshtein import distance as levenshtein_distance

def extract_tables_from_bs(soup, keys, max_dist=2):
    tables = soup.find_all('table')
    all_data = {}

    for table in tables:
        rows = table.find_all('tr')
        if not rows:
            continue

        # Extract text from each cell
        raw_rows = [
            [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            for row in rows
        ]

        # Remove empty rows
        raw_rows = [row for row in raw_rows if any(cell.strip() for cell in row)]

        if not raw_rows:
            continue

        # Case 1: Transposed with colon separator (3 columns like Name | : | Vijay)
        if all(len(row) == 3 and row[1] == ':' for row in raw_rows):
            raw_rows = [[row[0], row[2]] for row in raw_rows]

        # Case 2: Fully transposed table (2 columns like Name | Vijay)
        if all(len(row) == 2 for row in raw_rows):
            row_dict = {row[0].strip(): row[1].strip() for row in raw_rows}
            all_data.update({k: [v] for k, v in row_dict.items() if v})  # keep 1-row format
            continue

        # Case 3: Standard row-wise table
        first_row = raw_rows[0]
        data_rows = raw_rows[1:]

        # Fuzzy match headers with keys
        lower_keys = [key.lower() for key in keys]
        matched_headers = []
        for header in first_row:
            best_match, score = process.extractOne(header.lower(), lower_keys)
            if levenshtein_distance(best_match, header.lower()) <= max_dist:
                original_key = keys[lower_keys.index(best_match)]
                matched_headers.append(original_key)
            else:
                matched_headers.append(None)

        # Initialize storage
        table_data = {key: [] for key in matched_headers if key}

        for row in data_rows:
            if len(row) != len(matched_headers):
                continue  # Skip rows that don't match column count
            for idx, cell in enumerate(row):
                col = matched_headers[idx]
                if col:
                    table_data[col].append(cell)

        # Merge with all_data
        for k, v in table_data.items():
            if k in all_data:
                all_data[k].extend(v)
            else:
                all_data[k] = v

    # Remove empty columns
    all_data = {k: v for k, v in all_data.items() if v}
    return all_data
