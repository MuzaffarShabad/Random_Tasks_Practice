import pandas as pd
from itertools import combinations
from collections import defaultdict
import re

def preprocess(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()

def get_exact_ngrams(words, n):
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

def build_clusters(texts, n):
    ngram_to_indices = defaultdict(set)

    for idx, text in enumerate(texts):
        words = preprocess(text)
        ngrams = get_exact_ngrams(words, n)
        for ng in ngrams:
            ngram_to_indices[ng].add(idx)

    # Build clusters from shared n-grams
    clusters = [-1] * len(texts)
    cluster_id = 0

    visited = set()
    for idx in range(len(texts)):
        if idx in visited:
            continue
        queue = {idx}
        current_cluster = set()
        while queue:
            current = queue.pop()
            if current in visited:
                continue
            visited.add(current)
            current_cluster.add(current)
            words = preprocess(texts[current])
            ngrams = get_exact_ngrams(words, n)
            for ng in ngrams:
                queue.update(ngram_to_indices[ng])

        for i in current_cluster:
            clusters[i] = cluster_id
        cluster_id += 1

    return clusters

# ---------- Main Program ----------
def categorize_exact_n_gram(file_path, text_column, n):
    df = pd.read_excel(file_path)
    texts = df[text_column].fillna("").tolist()
    df['category'] = build_clusters(texts, n)
    return df

# ---------- Example Usage ----------
file_path = "your_file.xlsx"         # Your Excel file
text_column = "text"                 # Column name
n = 7                                # Exact number of consecutive words

result_df = categorize_exact_n_gram(file_path, text_column, n)
result_df.to_excel("categorized_emails_exact_ngram.xlsx", index=False)
