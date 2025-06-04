from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
import pandas as pd

# Step 1: Generate default report
report_dict = classification_report(
    y_true, y_pred,
    labels=your_label_list,
    target_names=your_label_list,
    output_dict=True
)

# Step 2: Manually calculate micro avg
micro_precision = precision_score(y_true, y_pred, average='micro')
micro_recall = recall_score(y_true, y_pred, average='micro')
micro_f1 = f1_score(y_true, y_pred, average='micro')
micro_support = len(y_true)

# Add micro avg to the report dictionary
report_dict["micro avg"] = {
    "precision": micro_precision,
    "recall": micro_recall,
    "f1-score": micro_f1,
    "support": micro_support
}

# Step 3: Convert to DataFrame and export
report_df = pd.DataFrame(report_dict).transpose().round(3)
report_df.to_excel("classification_report_with_micro_avg.xlsx")

print("Classification report with micro avg exported successfully.")
