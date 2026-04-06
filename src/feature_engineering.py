"""
feature_engineering.py
-----------------------
Feature selection using variance threshold and correlation analysis.
Optional PCA for dimensionality reduction.
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
import joblib
import os


class FeatureEngineer:
    def __init__(self, variance_threshold: float = 0.01, apply_pca: bool = False, pca_components: int = 20):
        self.variance_threshold = variance_threshold
        self.apply_pca = apply_pca
        self.pca_components = pca_components

        self.selector = VarianceThreshold(threshold=variance_threshold)
        self.pca = PCA(n_components=pca_components, random_state=42) if apply_pca else None
        self._fitted = False
        self.selected_indices = None

    def fit_transform(self, X: np.ndarray, feature_names: list = None):
        """
        Apply variance thresholding + optional PCA on training features.

        Returns:
            X_transformed (np.ndarray)
            selected_feature_names (list)
        """
        print(f"[INFO] Applying variance threshold ({self.variance_threshold})...")
        X_sel = self.selector.fit_transform(X)
        self.selected_indices = self.selector.get_support(indices=True)

        if feature_names:
            self.selected_feature_names = [feature_names[i] for i in self.selected_indices]
        else:
            self.selected_feature_names = [f"feature_{i}" for i in self.selected_indices]

        print(f"[INFO] Features after variance filter: {X_sel.shape[1]} / {X.shape[1]}")

        if self.apply_pca:
            print(f"[INFO] Applying PCA → {self.pca_components} components...")
            X_sel = self.pca.fit_transform(X_sel)
            explained = np.sum(self.pca.explained_variance_ratio_) * 100
            print(f"[INFO] PCA explained variance: {explained:.2f}%")

        self._fitted = True
        return X_sel, self.selected_feature_names

    def transform(self, X: np.ndarray):
        if not self._fitted:
            raise RuntimeError("FeatureEngineer must be fit before transforming.")
        X_sel = self.selector.transform(X)
        if self.apply_pca:
            X_sel = self.pca.transform(X_sel)
        return X_sel

    def save(self, path: str = "outputs/models/feature_engineer.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)
        print(f"[INFO] FeatureEngineer saved to {path}")

    @staticmethod
    def load(path: str = "outputs/models/feature_engineer.pkl"):
        return joblib.load(path)
