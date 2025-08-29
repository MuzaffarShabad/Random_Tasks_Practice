import pandas as pd

# Load Excel
df = pd.read_excel("your_file.xlsx")

# Example keywords per intent
intent_keywords = {
    "booking": ["book", "flight", "reserve"],
    "cancel": ["cancel", "terminate", "stop"],
    "refund": ["refund", "money back", "reimbursement"]
}

# Function to find matched keywords for a given intent
def find_keywords(text, intent):
    text_lower = text.lower()
    keywords = intent_keywords.get(intent, [intent])  # fallback = intent
    return [kw for kw in keywords if kw.lower() in text_lower]

# Main processing function
def process_row(row):
    text = row["text"]
    pred = row["pred"]

    # Check predicted intent
    matched = find_keywords(text, pred)
    if matched:
        return {"matched_keywords": matched, "has_keyword": True}

    # Otherwise check other intents
    suggested = {}
    idx = 1
    for intent, keywords in intent_keywords.items():
        if intent == pred:
            continue
        matches = [kw for kw in keywords if kw.lower() in text.lower()]
        if matches:
            suggested[f"suggested_intent_{idx}"] = intent
            suggested[f"suggested_keywords_{idx}"] = matches
            idx += 1

    # Base output
    result = {"matched_keywords": [], "has_keyword": False}
    result.update(suggested)
    return result

# Apply logic to DataFrame
extra = df.apply(process_row, axis=1, result_type="expand")
df = pd.concat([df, extra], axis=1)

# Save back
df.to_excel("output_with_multi_suggestions.xlsx", index=False)

print(df)
