from sklearn.metrics import roc_auc_score, log_loss
import numpy as np

# Example classes
class_labels = ['amount', 'quantity', 'date', 'other']

# Assume these are your gold examples and predicted TableEntities
y_true = []      # actual labels
y_pred = []      # predicted labels (entity_type)
y_prob = []      # list of class probability distributions

for example, table_ent in zip(examples, entities):
    y_true.append(example.label)  # actual
    y_pred.append(table_ent.entity_type)  # predicted
    probs = [table_ent.label_probs.get(cls, 0.0) for cls in class_labels]
    y_prob.append(probs)

# Convert to numpy arrays
y_true = np.array(y_true)
y_prob = np.array(y_prob)

# Binarize true labels for ROC AUC
from sklearn.preprocessing import label_binarize
y_true_bin = label_binarize(y_true, classes=class_labels)

# 🔹 Log Loss
logloss = log_loss(y_true, y_prob, labels=class_labels)

# 🔹 AUC Score (macro-average for multiclass)
auc_score = roc_auc_score(y_true_bin, y_prob, average='macro', multi_class='ovr')

print("Log Loss:", logloss)
print("AUC Score:", auc_score)
