import pandas as pd

# Step 1: Original (incomplete) dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Marks': [85, 92],            # Shorter
    'Roll': [11, 12, 13, 14]      # Longer
}

# Step 2: Normalize lengths by padding with None
max_len = max(len(v) for v in data.values())

for key in data:
    current_len = len(data[key])
    if current_len < max_len:
        data[key] += [None] * (max_len - current_len)

# Step 3: Convert to DataFrame
df = pd.DataFrame(data)

# Step 4: Add a new column (optional)
df['Grade'] = df['Marks'].apply(lambda x: 'A' if x is not None and x >= 90 else 'B' if x is not None and x >= 80 else 'C' if x is not None else None)

# Step 5: Convert back to dictionary
result_dict = df.to_dict(orient='list')

print(df)
print(result_dict)
