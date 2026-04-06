"""
data_loader.py
--------------
Loads and validates the NSL-KDD dataset from the data/ directory.
"""

import pandas as pd
import os

# 41 feature names from the NSL-KDD dataset
COLUMN_NAMES = [
    "duration", "protocol_type", "service", "flag", "src_bytes",
    "dst_bytes", "land", "wrong_fragment", "urgent", "hot",
    "num_failed_logins", "logged_in", "num_compromised", "root_shell",
    "su_attempted", "num_root", "num_file_creations", "num_shells",
    "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
    "label", "difficulty_level"
]


def load_data(train_path: str = "data/KDDTrain+.txt",
              test_path: str = "data/KDDTest+.txt"):
    """
    Load train and test datasets from the NSL-KDD text files.

    Returns:
        df_train (pd.DataFrame): Training data
        df_test  (pd.DataFrame): Test data
    """
    print("[INFO] Loading dataset...")

    if not os.path.exists(train_path) or not os.path.exists(test_path):
        raise FileNotFoundError(
            "Dataset not found. Please download NSL-KDD and place "
            "KDDTrain+.txt and KDDTest+.txt inside the data/ folder.\n"
            "Download: https://www.unb.ca/cic/datasets/nsl.html"
        )

    df_train = pd.read_csv(train_path, header=None, names=COLUMN_NAMES)
    df_test  = pd.read_csv(test_path,  header=None, names=COLUMN_NAMES)

    # Drop difficulty_level (not a feature)
    df_train.drop(columns=["difficulty_level"], inplace=True)
    df_test.drop(columns=["difficulty_level"], inplace=True)

    print(f"[INFO] Train shape: {df_train.shape}")
    print(f"[INFO] Test  shape: {df_test.shape}")
    print(f"[INFO] Label distribution (train):\n{df_train['label'].value_counts().head(10)}\n")

    return df_train, df_test


def binarize_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert multi-class attack labels to binary:
        0 = normal
        1 = attack (any intrusion type)
    """
    df = df.copy()
    df["label"] = df["label"].apply(lambda x: 0 if x.strip() == "normal" else 1)
    return df
