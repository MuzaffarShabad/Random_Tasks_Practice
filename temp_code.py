import pandas as pd
from itertools import combinations
from collections import defaultdict
import re

def preprocess(text):
    # Lowercase, remove punctuation, and split into words
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()

def get_ngrams(words, n):
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

def cluster_by_ngram(texts, n):
    text_ngrams = [get_ngrams(preprocess(t), n) for t in texts]
    clusters = [-1] * len(texts)
    cluster_id = 0

    for i in range(len(texts)):
        if clusters[i] != -1:
            continue  # already assigned to a cluster
        clusters[i] = cluster_id
        for j in range(i+1, len(texts)):
            if clusters[j] == -1 and not text_ngrams[i].isdisjoint(text_ngrams[j]):
                clusters[j] = cluster_id
        cluster_id += 1

    return clusters

# ---------- Main Program ----------

def categorize_emails_by_similarity(file_path, text_column, n):
    df = pd.read_excel(file_path)
    texts = df[text_column].fillna("").tolist()
    df['category'] = cluster_by_ngram(texts, n)
    return df

# ---------- Example Usage ----------
file_path = "your_file.xlsx"        # Replace with actual file path
text_column = "text"                # Replace with actual column name
n = 7                               # Number of consecutive words to match

result_df = categorize_emails_by_similarity(file_path, text_column, n)
result_df.to_excel("categorized_emails.xlsx", index=False)
