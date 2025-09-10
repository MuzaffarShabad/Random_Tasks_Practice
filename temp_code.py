import pandas as pd
from joblib import load
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

def CalculateMatrix(tfidf, y, clf, labels):
    """
    Calculate evaluation metrics for a trained classifier.

    Parameters:
    - tfidf : sparse matrix, features from TF-IDF
    - y : array-like, true labels
    - clf : trained classifier
    - labels : list of labels to include in the report

    Returns:
    - results_df : DataFrame containing classification report
    - cm : confusion matrix
    - auc : AUC score (if probabilities available)
    """

    # Predictions
    y_pred = clf.predict(tfidf)

    # Classification report
    report_dict = classification_report(
        y, y_pred, labels=labels, output_dict=True, zero_division=0
    )
    results_df = pd.DataFrame(report_dict).transpose()

    # Confusion matrix
    cm = confusion_matrix(y, y_pred, labels=labels)

    # AUC score (if predict_proba exists)
    auc = None
    if hasattr(clf, "predict_proba"):
        try:
            y_prob = clf.predict_proba(tfidf)
            auc = roc_auc_score(y, y_prob, multi_class='ovr')
        except Exception as e:
            print("AUC not calculated:", e)

    return results_df, cm, auc






# 1. Load data
df = pd.read_excel("input_data.xlsx")
X_text = df['text']
y_true = df['label']

# 2. Load TF-IDF vectorizer & transform
vectorizer = load("TF-IDF-Vectorizer.joblib")
X_tfidf = vectorizer.transform(X_text)

# 3. Load trained classifier
clf = load("model.joblib")   # random forest model

# 4. Define labels
labels = sorted(df['label'].unique())

# 5. Run evaluation
results_df, cm, auc = CalculateMatrix(X_tfidf, y_true, clf, labels)

print("Classification Report:\n", results_df)
print("\nConfusion Matrix:\n", cm)
print("\nAUC Score:", auc)

