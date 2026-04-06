"""
train.py
--------
Trains three models on preprocessed network traffic data:
  1. Random Forest Classifier (primary)
  2. Logistic Regression
  3. Isolation Forest (unsupervised anomaly detection)

Each model is saved to outputs/models/ for later evaluation.
"""

import numpy as np
import joblib
import os
import time

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression


MODELS_DIR = "outputs/models"
os.makedirs(MODELS_DIR, exist_ok=True)


def train_random_forest(X_train: np.ndarray, y_train: np.ndarray):
    """Train a Random Forest classifier."""
    print("\n[TRAIN] Training Random Forest...")
    t0 = time.time()

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        n_jobs=-1,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    elapsed = time.time() - t0
    print(f"[TRAIN] Random Forest trained in {elapsed:.2f}s")

    path = os.path.join(MODELS_DIR, "random_forest.pkl")
    joblib.dump(model, path)
    print(f"[TRAIN] Model saved → {path}")
    return model


def train_logistic_regression(X_train: np.ndarray, y_train: np.ndarray):
    """Train a Logistic Regression classifier."""
    print("\n[TRAIN] Training Logistic Regression...")
    t0 = time.time()

    model = LogisticRegression(
        max_iter=1000,
        solver="lbfgs",
        class_weight="balanced",
        random_state=42
    )
    model.fit(X_train, y_train)

    elapsed = time.time() - t0
    print(f"[TRAIN] Logistic Regression trained in {elapsed:.2f}s")

    path = os.path.join(MODELS_DIR, "logistic_regression.pkl")
    joblib.dump(model, path)
    print(f"[TRAIN] Model saved → {path}")
    return model


def train_isolation_forest(X_train: np.ndarray):
    """
    Train an Isolation Forest for unsupervised anomaly detection.
    IsolationForest predicts: 1 = normal, -1 = anomaly.
    We remap to: 0 = normal, 1 = anomaly for consistency.
    """
    print("\n[TRAIN] Training Isolation Forest (unsupervised)...")
    t0 = time.time()

    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,  # ~20% anomaly assumption
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train)

    elapsed = time.time() - t0
    print(f"[TRAIN] Isolation Forest trained in {elapsed:.2f}s")

    path = os.path.join(MODELS_DIR, "isolation_forest.pkl")
    joblib.dump(model, path)
    print(f"[TRAIN] Model saved → {path}")
    return model


def train_all(X_train: np.ndarray, y_train: np.ndarray):
    """
    Train all three models and return them in a dict.
    """
    print("\n" + "="*50)
    print("   MODEL TRAINING PIPELINE")
    print("="*50)

    rf = train_random_forest(X_train, y_train)
    lr = train_logistic_regression(X_train, y_train)
    iso = train_isolation_forest(X_train)

    print("\n[INFO] All models trained and saved successfully.\n")
    return {"random_forest": rf, "logistic_regression": lr, "isolation_forest": iso}
