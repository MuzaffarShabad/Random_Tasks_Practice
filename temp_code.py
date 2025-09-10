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












print("y_true shape:", len(y))
print("y_prob shape:", y_prob.shape)
print("clf.classes_:", clf.classes_)
print("Unique y_true:", set(y))








from sklearn.preprocessing import label_binarize

def CalculateMatrix(tfidf, y, clf):
    y_pred = clf.predict(tfidf)
    labels = clf.classes_

    report_dict = classification_report(
        y, y_pred, labels=labels, output_dict=True, zero_division=0
    )
    results_df = pd.DataFrame(report_dict).transpose()
    cm = confusion_matrix(y, y_pred, labels=labels)

    auc = None
    if hasattr(clf, "predict_proba"):
        y_prob = clf.predict_proba(tfidf)

        # Binarize y_true for multiclass AUC
        y_bin = label_binarize(y, classes=labels)

        if y_bin.shape[1] == y_prob.shape[1]:
            auc = roc_auc_score(y_bin, y_prob, multi_class='ovr')

    return results_df, cm, auc





















import pandas as pd
from joblib import load
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import label_binarize
import numpy as np

def CalculateMatrix(tfidf, y, clf):
    # Predictions
    y_pred = clf.predict(tfidf)
    labels = clf.classes_

    # Classification report
    report_dict = classification_report(
        y, y_pred, labels=labels, output_dict=True, zero_division=0
    )
    results_df = pd.DataFrame(report_dict).transpose()

    # Confusion matrix
    cm = confusion_matrix(y, y_pred, labels=labels)

    # AUC calculation (per-class safe handling)
    auc = {}
    if hasattr(clf, "predict_proba"):
        y_prob = clf.predict_proba(tfidf)

        # Store predictions with probabilities
        preds_df = pd.DataFrame(y_prob, columns=[f"proba_{c}" for c in labels])
        preds_df["true_label"] = y
        preds_df["predicted_label"] = y_pred

        # Compute per-class AUC
        y_bin = label_binarize(y, classes=labels)
        for i, cls in enumerate(labels):
            if len(np.unique(y_bin[:, i])) > 1:  # skip if only one class present
                auc[cls] = roc_auc_score(y_bin[:, i], y_prob[:, i])
            else:
                auc[cls] = np.nan
    else:
        preds_df = pd.DataFrame({"true_label": y, "predicted_label": y_pred})

    return results_df, cm, auc, preds_df












# Run evaluation
results_df, cm, auc, preds_df = CalculateMatrix(X_tfidf, y_true, clf)

print("Classification Report:\n", results_df)
print("\nConfusion Matrix:\n", cm)
print("\nPer-class AUC:", auc)

# Show sample predictions with probabilities
print("\nSample predictions with probabilities:\n", preds_df.head(10))

# Save to Excel
preds_df.to_excel("detailed_predictions.xlsx", index=False)

