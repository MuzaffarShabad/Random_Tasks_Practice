import pandas as pd

# Load Excel
df = pd.read_excel("your_file.xlsx")

# Example: keywords per intent
intent_keywords = {
    "booking": ["book", "flight", "reserve"],
    "cancel": ["cancel", "terminate", "stop"],
    "refund": ["refund", "money back", "reimbursement"]
}

# Function to find matched keywords for a given intent
def find_keywords(text, intent):
    text_lower = text.lower()
    keywords = intent_keywords.get(intent, [intent])  # fallback = intent itself
    return [kw for kw in keywords if kw.lower() in text_lower]

# Main logic
def process_row(row):
    text = row["text"]
    pred = row["pred"]
    
    # Keywords for predicted intent
    matched = find_keywords(text, pred)
    
    if matched:  # Found keywords for predicted intent
        return pd.Series({
            "matched_keywords": matched,
            "has_keyword": True,
            "suggested_intent": None,
            "suggested_keywords": []
        })
    else:  # No keywords found for predicted intent → check other intents
        for intent, keywords in intent_keywords.items():
            if intent == pred:  # skip current pred
                continue
            matches = [kw for kw in keywords if kw.lower() in text.lower()]
            if matches:
                return pd.Series({
                    "matched_keywords": [],
                    "has_keyword": False,
                    "suggested_intent": intent,
                    "suggested_keywords": matches
                })
        # No matches anywhere
        return pd.Series({
            "matched_keywords": [],
            "has_keyword": False,
            "suggested_intent": None,
            "suggested_keywords": []
        })

# Apply logic
df = df.join(df.apply(process_row, axis=1))

# Save back
df.to_excel("output_with_suggestions.xlsx", index=False)

print(df)
