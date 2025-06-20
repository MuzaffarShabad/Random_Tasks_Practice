import pandas as pd
from collections import defaultdict
import re

def preprocess(text):
    """Lowercase, remove punctuation, and split text into words."""
    text = re.sub(r'[^\w\s]', '', str(text).lower())
    return text.split()

def get_exact_ngrams(words, n):
    """Generate all exact consecutive n-word sequences."""
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]

def build_exact_ngram_clusters(texts, n):
    ngram_to_texts = defaultdict(set)
    ngram_to_id = {}
    idx_to_ngram = ["no_match"] * len(texts)

    # Map each exact n-gram to text indices
    for idx, text in enumerate(texts):
        words = preprocess(text)
        ngrams = get_exact_ngrams(words, n)
        for ng in ngrams:
            ngram_to_texts[ng].add(idx)

    # Cluster assignment
    clusters = [-1] * len(texts)
    cluster_id = 0
    visited = set()

    for i in range(len(texts)):
        if i in visited:
            continue

        matched_group = set()
        words = preprocess(texts[i])
        ngrams = get_exact_ngrams(words, n)

        match_found = False
        for ng in ngrams:
            group = ngram_to_texts[ng]
            if len(group) > 1:
                matched_group = group
                matched_ngram = ng
                match_found = True
                break  # use the first valid match

        if match_found:
            for idx in matched_group:
                if clusters[idx] == -1:  # assign only if unassigned
                    clusters[idx] = cluster_id
                    idx_to_ngram[idx] = matched_ngram
                    visited.add(idx)
            cluster_id += 1

    return clusters, idx_to_ngram

# ----------- MAIN USAGE ---------------

def process_excel(file_path, text_column_name, n):
    df = pd.read_excel(file_path)
    texts = df[text_column_name].fillna("").tolist()
    categories, matched_ngrams = build_exact_ngram_clusters(texts, n)
    df['Category'] = categories
    df['Matched_Ngram'] = matched_ngrams
    return df

# ----------- Example Execution -----------

# Customize these
file_path = "your_excel_file.xlsx"      # e.g. "emails.xlsx"
text_column_name = "text"               # e.g. "email_text"
n = 7                                   # Number of consecutive words

df_result = process_excel(file_path, text_column_name, n)
df_result.to_excel("categorized_output_with_ngram.xlsx", index=False)
print(df_result[['text', 'Category', 'Matched_Ngram']])
