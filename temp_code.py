import numpy as np
import pandas as pd

def psi_from_confusion_matrices(train_cm, test_cm, class_labels=None, epsilon=1e-6):
    """
    Compute PSI from confusion matrices of train and test sets, with class labels.

    Parameters:
        train_cm (ndarray): Confusion matrix for train (actual values by rows)
        test_cm (ndarray): Confusion matrix for test
        class_labels (list): Optional list of class names (e.g., ['A', 'B', 'C'])
        epsilon (float): Small value to prevent division/log errors

    Returns:
        psi_df (DataFrame): PSI per class with counts and ratios
        total_psi (float): Total aggregated PSI value
    """
    # Step 1: Get class-wise actual counts (sum of rows)
    train_counts = np.sum(train_cm, axis=1)
    test_counts = np.sum(test_cm, axis=1)

    # Step 2: Normalize to get distributions
    train_dist = train_counts / train_counts.sum()
    test_dist = test_counts / test_counts.sum()

    # Step 3: Create class labels if not provided
    num_classes = len(train_counts)
    if class_labels is None:
        class_labels = [f"Class {i}" for i in range(num_classes)]

    # Step 4: Calculate PSI
    psi_values = []
    for i, (e, a) in enumerate(zip(train_dist, test_dist)):
        e += epsilon
        a += epsilon
        psi = (e - a) * np.log(e / a)
        psi_values.append((
            class_labels[i],
            train_counts[i],
            test_counts[i],
            round(e, 6),
            round(a, 6),
            round(psi, 6)
        ))

    psi_df = pd.DataFrame(psi_values, columns=["Class", "Train Count", "Test Count", "Train Ratio", "Test Ratio", "PSI"]).set_index("Class")
    total_psi = psi_df["PSI"].sum()
    return psi_df, total_psi
