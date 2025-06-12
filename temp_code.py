import pandas as pd
import numpy as np
from collections import Counter

def calculate_psi_from_counts(train_labels, test_labels):
    # Count class frequencies
    train_counts = Counter(train_labels)
    test_counts = Counter(test_labels)

    # Get all classes
    all_classes = sorted(set(train_counts) | set(test_counts))

    # Initialize results
    result = []

    total_train = sum(train_counts.values())
    total_test = sum(test_counts.values())

    for cls in all_classes:
        train_count = train_counts.get(cls, 0)
        test_count = test_counts.get(cls, 0)

        train_ratio = train_count / total_train if total_train else 0
        test_ratio = test_count / total_test if total_test else 0

        # Avoid log(0)
        psi = (test_ratio - train_ratio) * np.log((test_ratio + 1e-8) / (train_ratio + 1e-8)) if train_ratio > 0 and test_ratio > 0 else 0

        result.append({
            "class": cls,
            "train count": train_count,
            "test count": test_count,
            "train ratio": round(train_ratio, 4),
            "test ratio": round(test_ratio, 4),
            "psi": round(psi, 6)
        })

    df = pd.DataFrame(result)
    total_psi = df['psi'].sum()
    df.loc['Total'] = ['Total', '', '', '', '', round(total_psi, 6)]

    return df
