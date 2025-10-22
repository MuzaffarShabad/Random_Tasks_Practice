import pandas as pd
import ast # Used for safely evaluating string representations of dictionaries
import numpy as np # Used for handling NaN values if necessary

# --- Configuration ---
INPUT_EXCEL_FILE = "response.xlsx"  # Change this to the name of your Excel file
OUTPUT_EXCEL_FILE = "output_with_probabilities.xlsx"
STATISTICS_COLUMN_NAME = "statistics" # The exact name of the column containing the complex data

# --- Extraction Function ---

def extract_probabilities(stats_data):
    """
    Safely extracts the 'all_probabilities' dictionary from the nested string 
    within the 'ASSET_SERVICING' block of the statistics column.
    """
    
    # 1. Check if the top-level data is valid (i.e., not NaN/missing)
    if pd.isna(stats_data):
        return pd.Series({})
    
    try:
        # 2. Access the 'ASSET_SERVICING' block
        asset_servicing = stats_data.get('ASSET_SERVICING')
        
        if not asset_servicing:
            return pd.Series({})
            
        # 3. Get the string containing the nested data
        intent_model_str = asset_servicing.get('intent_service_intent_from_model')
        
        # Check for 'N/A' or missing string
        if not intent_model_str or intent_model_str == 'N/A':
            return pd.Series({})
            
        # 4. Safely convert the string (with single quotes) to a Python dictionary
        # ast.literal_eval is safer than eval() and handles Python literals.
        intent_model_dict = ast.literal_eval(intent_model_str)
        
        # 5. Access the target probabilities dictionary
        probabilities = intent_model_dict.get('all_probabilities', {})
        
        # 6. Clean up the keys and return as a Pandas Series
        # We strip any accidental quotes/spaces from the keys (though not strictly necessary 
        # for your sample, it's good practice for messy data).
        cleaned_probabilities = {k.strip("'").strip(): v for k, v in probabilities.items()}
        
        # Return as a Pandas Series; keys become column names
        return pd.Series(cleaned_probabilities)
        
    except (KeyError, ValueError, TypeError, SyntaxError) as e:
        # Handle cases where the JSON structure is unexpected or the string parsing fails
        # print(f"Error processing row: {e}") # Uncomment this for debugging
        return pd.Series({}) # Return an empty Series for failed rows

# --- Main Processing Logic ---

# 1. Load the Excel file
try:
    df = pd.read_excel(INPUT_EXCEL_FILE)
    print(f"Successfully loaded {INPUT_EXCEL_FILE} with {len(df)} rows.")
except FileNotFoundError:
    print(f"❌ Error: Input file '{INPUT_EXCEL_FILE}' not found.")
    exit()

# 2. Ensure the 'statistics' column is properly formatted (as dictionaries)
# If the 'statistics' column was saved to Excel as a string, you must convert it first:
if df[STATISTICS_COLUMN_NAME].dtype == object and isinstance(df[STATISTICS_COLUMN_NAME].iloc[0], str):
    print("Converting 'statistics' column from string to dictionary...")
    # Use ast.literal_eval to convert the column strings into actual dictionaries
    df[STATISTICS_COLUMN_NAME] = df[STATISTICS_COLUMN_NAME].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else np.nan)


# 3. Apply the extraction function row-by-row
# The result is a new DataFrame containing only the extracted probability columns.
probability_df = df.apply(lambda row: extract_probabilities(row[STATISTICS_COLUMN_NAME]), axis=1)

# 4. Clean up column names for the new DataFrame
# Replace spaces and slashes for clean column headers
probability_df.columns = [col.replace(' ', '_').replace('/', '_') for col in probability_df.columns]

# 5. Combine the new probability columns with the original DataFrame
df = pd.concat([df, probability_df], axis=1)

# 6. Export the final DataFrame back to a new Excel file
df.to_excel(OUTPUT_EXCEL_FILE, index=False)
print(f"\n✅ Success! New columns added and exported to: {OUTPUT_EXCEL_FILE}")
