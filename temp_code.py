import pandas as pd
from joblib import load

# 1. Load Excel file
df = pd.read_excel("input_data.xlsx")   # replace with your file
X_text = df['text']   # assuming the text column is named 'text'

# 2. Load TF-IDF vectorizer
vectorizer = load("TF-IDF-Vectorizer.joblib")

# 3. Transform text into numeric features
X_tfidf = vectorizer.transform(X_text)

# Show shape of the transformed data
print("TF-IDF shape:", X_tfidf.shape)

# Optionally convert to dense DataFrame (only if not too large)
tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=vectorizer.get_feature_names_out())
print(tfidf_df.head())
