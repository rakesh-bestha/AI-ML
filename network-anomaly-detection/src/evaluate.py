"""
evaluate.py
-----------
Evaluates trained models on the test set.
Computes accuracy, precision, recall, F1-score, and ROC-AUC.
Prints a classification report and returns metrics dict.
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report, confusion_matrix
)


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray,
                   model_name: str = "Model", is_isolation_forest: bool = False):
    """
    Evaluate a trained model on the test set.

    Args:
        model: Trained sklearn model
        X_test: Test features
        y_test: True binary labels (0=normal, 1=attack)
        model_name: Display name for reporting
        is_isolation_forest: If True, remap -1/1 predictions to 1/0

    Returns:
        metrics (dict): accuracy, precision, recall, f1, roc_auc, y_pred
    """
    print(f"\n{'='*50}")
    print(f"  EVALUATION: {model_name}")
    print(f"{'='*50}")

    if is_isolation_forest:
        raw_preds = model.predict(X_test)
        # IsolationForest: 1=normal, -1=anomaly → remap to 0=normal, 1=attack
        y_pred = np.where(raw_preds == -1, 1, 0)
        # No probability output from IsolationForest; use decision function
        scores = -model.decision_function(X_test)  # higher = more anomalous
        try:
            roc_auc = roc_auc_score(y_test, scores)
        except Exception:
            roc_auc = None
    else:
        y_pred = model.predict(X_test)
        try:
            y_prob = model.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test, y_prob)
        except Exception:
            roc_auc = None

    acc       = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall    = recall_score(y_test, y_pred, zero_division=0)
    f1        = f1_score(y_test, y_pred, zero_division=0)
    cm        = confusion_matrix(y_test, y_pred)

    print(f"\nAccuracy  : {acc:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-Score  : {f1:.4f}")
    if roc_auc is not None:
        print(f"ROC-AUC   : {roc_auc:.4f}")
    print(f"\nConfusion Matrix:\n{cm}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=['Normal', 'Attack'])}")

    return {
        "model_name": model_name,
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "confusion_matrix": cm,
        "y_pred": y_pred
    }


def evaluate_all(models: dict, X_test: np.ndarray, y_test: np.ndarray):
    """
    Evaluate all models and return list of metric dicts.
    """
    results = []
    for name, model in models.items():
        is_iso = (name == "isolation_forest")
        metrics = evaluate_model(model, X_test, y_test,
                                 model_name=name.replace("_", " ").title(),
                                 is_isolation_forest=is_iso)
        metrics["model_key"] = name
        results.append(metrics)
    return results
