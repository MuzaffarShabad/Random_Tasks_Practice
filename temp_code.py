import pandas as pd
import json
import ast # Used for safely evaluating string representations of dictionaries/lists

# --- 1. SAMPLE DATA SETUP (Replace this with your actual DataFrame loading) ---

# This simulates the value present in your 'statistics' column for one row
sample_statistics_value = {
    'CASH_SET_MIDDLE_OFFICE': {
        'entity_extractor_service_total_unique_rows': 'N/A', 
        'intent_service_intent_from_model': 'N/A',
        'intent_service_intent_from_regex': 'N/A', 
        'intent_service_regex_analysis': 'N/A'
    },
    'ASSET_SERVICING': {
        'entity_extractor_service_total_unique_rows': 0, 
        'intent_service_intent_from_model': "{'sentence': 'N/A', 'intent': ' Payment Incorrect/Missing', 'probability': 85.15, 'all_probabilities': {'Instruction Processing': 1.68, 'Liability Confirmation': 0.65, 'Payment': 85.15, 'Proxy': 1.42, 'notification': 11.09}, 'source': 'model'}", 
        'intent_service_intent_from_regex': "{'sentence': 'N/A', 'intent': '', 'probability': 0, 'source': 'regex'}", 
        'intent_service_regex_analysis': "{'Deadline Extension': []}"
    }
}

# Create a sample DataFrame (You will load your Excel file instead)
df = pd.DataFrame([{'statistics': sample_statistics_value}])

# --- 2. EXTRACTION FUNCTION ---

def extract_probabilities(row):
    """
    Safely extracts the 'all_probabilities' dictionary from the nested JSON string
    in the ASSET_SERVICING block.
    """
    try:
        # Access the 'ASSET_SERVICING' block
        asset_servicing = row['statistics']['ASSET_SERVICING']
        
        # Get the string containing the nested JSON data
        intent_model_str = asset_servicing['intent_service_intent_from_model']
        
        # Check for 'N/A' or empty string before parsing
        if intent_model_str == 'N/A':
            return pd.Series({})
            
        # The string uses single quotes, making it invalid JSON. 
        # Use ast.literal_eval for a safe conversion to a dictionary.
        intent_model_dict = ast.literal_eval(intent_model_str)
        
        # Access the probabilities dictionary
        probabilities = intent_model_dict.get('all_probabilities', {})
        
        # Clean up the keys: remove trailing quotes (e.g., 'Liability Confirmation' becomes 'Liability Confirmation')
        cleaned_probabilities = {k.strip("'"): v for k, v in probabilities.items()}
        
        # Return as a Pandas Series, where keys become column names
        return pd.Series(cleaned_probabilities)
        
    except (KeyError, ValueError, TypeError, SyntaxError) as e:
        # Handle cases where the structure is missing or the string is malformed
        # print(f"Error processing row: {e}") # Uncomment this for debugging
        return pd.Series({}) # Return an empty Series for rows that fail

# --- 3. APPLY EXTRACTION AND CLEANUP ---

# Load your actual Excel file here:
# df = pd.read_excel("your_results_file.xlsx")

# Apply the function to the 'statistics' column and concatenate the results
probability_df = df.apply(extract_probabilities, axis=1)

# Rename columns for clarity (e.g., replace spaces with underscores)
probability_df.columns = [col.replace(' ', '_').replace('/', '_') for col in probability_df.columns]

# Combine the new columns with the original DataFrame
df = pd.concat([df, probability_df], axis=1)

# --- 4. DISPLAY RESULT ---
print(df.head())

# --- 5. EXPORT FINAL RESULT ---
# df.to_excel("final_results_with_probabilities.xlsx", index=False)
