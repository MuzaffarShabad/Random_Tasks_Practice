import pandas as pd

# Read Excel file
df = pd.read_excel("your_file.xlsx")

# Ensure text column is string
df["text"] = df["text"].astype(str)

# Compute text length
df["text_length"] = df["text"].apply(len)

# Overall statistics
mean_length = df["text_length"].mean()
max_length = df["text_length"].max()
std_length = df["text_length"].std()

print("Mean text length:", mean_length)
print("Max text length:", max_length)
print("Std Dev of text length:", std_length)

# Value counts of inquiry_id
inquiry_counts = df["inquiry_id"].value_counts()

print("\nInquiry ID Value Counts:")
print(inquiry_counts)

# If you also want per-inquiry_id stats
group_stats = df.groupby("inquiry_id")["text_length"].agg(
    ["count", "mean", "max", "std"]
).reset_index()

print("\nPer Inquiry ID Stats:")
print(group_stats)
