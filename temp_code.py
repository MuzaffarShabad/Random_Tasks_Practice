import os
import json
from datetime import datetime, timedelta

# Replace with actual START_DATE and END_DATE values
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 1, 5)  # Example

# Placeholder function for fetch_inquiries
def fetch_inquiries(start, end, client, grp_ids_set):
    # Simulate API data
    return [{"_id": 123, "data": "sample"}]

# Dummy client and group IDs
client = None
grp_ids_set = None

# Final list to store all inquiries
all_inquiries = []

while START_DATE < END_DATE:
    print(f"Querying for {START_DATE.day}/{START_DATE.month}/{START_DATE.year}")

    # Fetch data for one day
    inquiries = fetch_inquiries(START_DATE, START_DATE + timedelta(days=1), client, grp_ids_set)

    # Append all fetched inquiries to master list
    all_inquiries.extend(inquiries)

    # Move to next day
    START_DATE += timedelta(days=1)

# Define output filename
output_filename = "all_inquiries.json"
output_path = os.path.join(".", output_filename)

# Write all inquiries to one single JSON file
with open(output_path, "w") as f:
    json.dump(all_inquiries, f, indent=4)

print(f"\n✅ All inquiries written to {output_path}")
