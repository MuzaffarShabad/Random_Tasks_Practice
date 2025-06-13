import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'text': [
        'Apple is a fruit', 'Apple is a fruit',
        'Banana is yellow', 'Banana is yellow',
        'Orange is sweet', 'Grapes are green'
    ],
    'actual_pred': [
        'Fruit', 'Company',    # <-- Same text, different categories
        'Fruit', 'Fruit',
        'Fruit', 'Fruit'
    ]
})

# Step 1: Group by text and check how many unique categories exist for each text
duplicates_with_diff_labels = df.groupby('text')['actual_pred'].nunique()

# Step 2: Filter where more than one unique label exists
conflicting_entries = duplicates_with_diff_labels[duplicates_with_diff_labels > 1]

# Step 3: Optional - show full rows from original DataFrame
result_df = df[df['text'].isin(conflicting_entries.index)]

print(result_df)
