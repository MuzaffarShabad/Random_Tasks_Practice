import pandas as pd
from collections import defaultdict
import re

def preprocess(text):
    """Lowercase, remove punctuation, and split text into words."""
    text = re.sub(r'[^\w\s]', '', str(text).lower())
    return text.split()

def get_exact_ngrams(words, n):
    """Generate all n-grams of exact consecutive words."""
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]

def build_exact_ngram_clusters(texts, n):
    """Cluster texts by exact shared n-grams."""
    ngram_to_texts = defaultdict(set)

    # Step 1: Map each exact n-gram to the indices of texts that contain it
    for idx, text in enumerate(texts):
        words = preprocess(text)
        ngrams = get_exact_ngrams(words, n)
        for ng in ngrams:
            ngram_to_texts[ng].add(idx)

    # Step 2: Cluster texts that share the same exact n-gram
    clusters = [-1] * len(texts)
    cluster_id = 0
    visited = set()

    for i in range(len(texts)):
        if i in visited:
            continue

        matched_group = set()
        words = preprocess(texts[i])
        ngrams = get_exact_ngrams(words, n)

        for ng in ngrams:
            matched_group.update(ngram_to_texts[ng])

        if len(matched_group) > 1:
            for idx in matched_group:
                clusters[idx] = cluster_id
                visited.add(idx)
            cluster_id += 1

    # Assign "no_match" to texts not in any cluster
    for i in range(len(clusters)):
        if clusters[i] == -1:
            clusters[i] = "no_match"

    return clusters

# ----------- MAIN USAGE ---------------

def process_excel(file_path, text_column_name, n):
    df = pd.read_excel(file_path)
    texts = df[text_column_name].fillna("").tolist()
    df['Category'] = build_exact_ngram_clusters(texts, n)
    return df

# ----------- Example Execution -----------

# Customize this path and column name as per your file
file_path = "your_excel_file.xlsx"       # e.g. "emails.xlsx"
text_column_name = "text"                # e.g. "email_text"
n = 7                                    # consecutive word count to match

df_result = process_excel(file_path, text_column_name, n)
df_result.to_excel("categorized_output.xlsx", index=False)
print(df_result[['text', 'Category']])
