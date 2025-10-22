import pandas as pd
import ast
import numpy as np

# --- Configuration ---
INPUT_EXCEL_FILE = "response.xlsx"  # Change this to the name of your Excel file
OUTPUT_EXCEL_FILE = "output_with_max_intent_and_probabilities.xlsx"
STATISTICS_COLUMN_NAME = "statistics" 

# --- Extraction Function ---

def extract_probabilities_and_max_intent(stats_data):
    """
    Safely extracts the 'all_probabilities' dictionary, and calculates 
    the intent with the max probability and its value.
    Returns a Series containing all probabilities, max intent, and max probability.
    """
    
    # Initialize default return values for the max intent/probability
    results = {'max_intent': 'N/A', 'max_probability': 0.0}
    
    if pd.isna(stats_data):
        return pd.Series(results)
    
    try:
        # 1. Access the 'ASSET_SERVICING' block
        asset_servicing = stats_data.get('ASSET_SERVICING')
        
        if not asset_servicing:
            return pd.Series(results)
            
        # 2. Get the string containing the nested data
        intent_model_str = asset_servicing.get('intent_service_intent_from_model')
        
        if not intent_model_str or intent_model_str == 'N/A':
            return pd.Series(results)
            
        # 3. Safely convert the string to a Python dictionary
        intent_model_dict = ast.literal_eval(intent_model_str)
        
        # 4. Access the target probabilities dictionary
        probabilities = intent_model_dict.get('all_probabilities', {})
        
        # 5. Extract MAX INTENT AND PROBABILITY
        if probabilities:
            # Find the key (intent) with the maximum value (probability)
            max_intent = max(probabilities, key=probabilities.get)
            max_probability = probabilities[max_intent]
            
            # Store the max intent/probability in the results dictionary
            results['max_intent'] = max_intent.strip("'").strip()
            results['max_probability'] = max_probability
        
        # 6. Extract all individual probabilities
        cleaned_probabilities = {k.strip("'").strip(): v for k, v in probabilities.items()}
        
        # Merge all individual probabilities into the results dictionary
        results.update(cleaned_probabilities)
        
        # Return as a Pandas Series
        return pd.Series(results)
        
    except (KeyError, ValueError, TypeError, SyntaxError) as e:
        # print(f"Error processing row: {e}") # Uncomment for debugging
        return pd.Series(results) 

# --- Main Processing Logic ---

# 1. Load the Excel file
try:
    df = pd.read_excel(INPUT_EXCEL_FILE)
    print(f"Successfully loaded {INPUT_EXCEL_FILE} with {len(df)} rows.")
except FileNotFoundError:
    print(f"❌ Error: Input file '{INPUT_EXCEL_FILE}' not found.")
    exit()

# 2. Convert 'statistics' column from string to dictionary if necessary
if STATISTICS_COLUMN_NAME in df.columns and df[STATISTICS_COLUMN_NAME].dtype == object and isinstance(df[STATISTICS_COLUMN_NAME].iloc[0], str):
    print("Converting 'statistics' column from string to dictionary...")
    df[STATISTICS_COLUMN_NAME] = df[STATISTICS_COLUMN_NAME].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else np.nan)


# 3. Apply the extraction function row-by-row
# The result is a new DataFrame containing all extracted data, including max intent/prob.
extracted_df = df.apply(lambda row: extract_probabilities_and_max_intent(row[STATISTICS_COLUMN_NAME]), axis=1)

# 4. Clean up column names for the new DataFrame
extracted_df.columns = [col.replace(' ', '_').replace('/', '_') for col in extracted_df.columns]

# 5. Combine the new columns with the original DataFrame
# Drop 'max_intent' and 'max_probability' from the new DataFrame if they were already added 
# by the prior step, just to ensure clean concatenation.
df = pd.concat([df, extracted_df], axis=1)

# 6. Export the final DataFrame back to a new Excel file
df.to_excel(OUTPUT_EXCEL_FILE, index=False)
print(f"\n✅ Success! Max intent/probability and all columns added and exported to: {OUTPUT_EXCEL_FILE}")
