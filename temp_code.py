import pandas as pd

# Load Excel
df = pd.read_excel("your_file.xlsx")

# Example: Keywords per intent (you can pass this, partial allowed)
intent_keywords = {
    "booking": ["book", "flight", "reserve"],
    "cancel": ["cancel", "terminate", "stop"]
}

# Function to find matched keywords
def find_keywords(text, intent):
    text_lower = text.lower()
    # Use intent-specific keywords, else fallback to [intent]
    keywords = intent_keywords.get(intent, [intent])
    matches = [kw for kw in keywords if kw.lower() in text_lower]
    return matches

# Add columns
df["matched_keywords"] = df.apply(lambda row: find_keywords(row["text"], row["pred"]), axis=1)
df["has_keyword"] = df["matched_keywords"].apply(lambda x: len(x) > 0)

# Save updated file
df.to_excel("output_with_keywords.xlsx", index=False)

print(df.head())
