"""
preprocessor.py
---------------
Handles data cleaning, label encoding of categorical features,
and standard scaling of numeric features.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

CATEGORICAL_COLS = ["protocol_type", "service", "flag"]


class Preprocessor:
    def __init__(self):
        self.encoders = {col: LabelEncoder() for col in CATEGORICAL_COLS}
        self.scaler = StandardScaler()
        self._fitted = False

    def fit_transform(self, df: pd.DataFrame):
        """
        Fit encoders and scaler on training data, then transform.

        Args:
            df: Training DataFrame (includes 'label' column)

        Returns:
            X (np.ndarray): Scaled feature matrix
            y (np.ndarray): Binary label array
        """
        df = df.copy()

        print("[INFO] Encoding categorical features...")
        for col in CATEGORICAL_COLS:
            df[col] = self.encoders[col].fit_transform(df[col].astype(str))

        y = df["label"].values
        X_df = df.drop(columns=["label"])

        print("[INFO] Scaling features...")
        X = self.scaler.fit_transform(X_df)

        self._fitted = True
        self._feature_names = X_df.columns.tolist()

        print(f"[INFO] Preprocessing complete. X shape: {X.shape}, y shape: {y.shape}")
        return X, y

    def transform(self, df: pd.DataFrame):
        """
        Apply fitted encoders and scaler to new data (test set).

        Args:
            df: Test DataFrame

        Returns:
            X (np.ndarray): Scaled feature matrix
            y (np.ndarray): Binary label array
        """
        if not self._fitted:
            raise RuntimeError("Preprocessor must be fit before transforming test data.")

        df = df.copy()

        for col in CATEGORICAL_COLS:
            # Handle unseen labels gracefully
            known_classes = set(self.encoders[col].classes_)
            df[col] = df[col].apply(
                lambda x: x if x in known_classes else self.encoders[col].classes_[0]
            )
            df[col] = self.encoders[col].transform(df[col].astype(str))

        y = df["label"].values
        X_df = df.drop(columns=["label"])

        X = self.scaler.transform(X_df)
        return X, y

    @property
    def feature_names(self):
        return self._feature_names

    def save(self, path: str = "outputs/models/preprocessor.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)
        print(f"[INFO] Preprocessor saved to {path}")

    @staticmethod
    def load(path: str = "outputs/models/preprocessor.pkl"):
        return joblib.load(path)
