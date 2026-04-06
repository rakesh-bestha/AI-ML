"""
visualize.py
------------
Generates and saves all visualizations:
  - Label distribution (bar chart)
  - Correlation heatmap
  - Confusion matrices
  - ROC curves (all models)
  - Feature importance (Random Forest)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving files
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay, roc_curve, auc

PLOTS_DIR = "outputs/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# Style
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#f9f9f9",
    "axes.grid": True,
    "grid.alpha": 0.4,
    "font.family": "DejaVu Sans",
})


def plot_label_distribution(y_train, y_test):
    """Bar chart showing class balance in train and test sets."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, y, title in zip(axes, [y_train, y_test], ["Train Set", "Test Set"]):
        unique, counts = np.unique(y, return_counts=True)
        bars = ax.bar(["Normal (0)", "Attack (1)"], counts, color=["#2196F3", "#F44336"], edgecolor="white")
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                    f"{count:,}", ha="center", va="bottom", fontweight="bold")
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_ylabel("Count")
        ax.set_ylim(0, max(counts) * 1.15)
    fig.suptitle("Label Distribution — Normal vs Attack", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "label_distribution.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[PLOT] Saved → {path}")


def plot_correlation_heatmap(X, feature_names, top_n=20):
    """Heatmap of top N feature correlations."""
    import pandas as pd
    df = pd.DataFrame(X[:, :top_n], columns=feature_names[:top_n])
    corr = df.corr()

    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(corr, annot=False, cmap="coolwarm", center=0,
                linewidths=0.3, ax=ax, square=True, cbar_kws={"shrink": 0.8})
    ax.set_title(f"Feature Correlation Heatmap (Top {top_n} Features)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "correlation_heatmap.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[PLOT] Saved → {path}")


def plot_confusion_matrix(cm, model_name: str):
    """Single confusion matrix plot for a given model."""
    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Normal", "Attack"])
    disp.plot(ax=ax, colorbar=True, cmap="Blues")
    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fname = model_name.lower().replace(" ", "_")
    path = os.path.join(PLOTS_DIR, f"confusion_matrix_{fname}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[PLOT] Saved → {path}")


def plot_roc_curves(models: dict, X_test, y_test):
    """Overlay ROC curves for all classifiers that support predict_proba."""
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#1565C0", "#D32F2F", "#2E7D32", "#F57F17"]

    for (name, model), color in zip(models.items(), colors):
        if name == "isolation_forest":
            scores = -model.decision_function(X_test)
        else:
            try:
                scores = model.predict_proba(X_test)[:, 1]
            except AttributeError:
                continue

        fpr, tpr, _ = roc_curve(y_test, scores)
        roc_auc = auc(fpr, tpr)
        label = f"{name.replace('_', ' ').title()} (AUC = {roc_auc:.3f})"
        ax.plot(fpr, tpr, color=color, lw=2, label=label)

    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random Classifier")
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title("ROC Curves — All Models", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=10)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])
    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "roc_curves.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[PLOT] Saved → {path}")


def plot_feature_importance(model, feature_names: list, top_n: int = 20):
    """Horizontal bar chart of top N feature importances (Random Forest)."""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    top_features = [feature_names[i] for i in indices]
    top_scores = importances[indices]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(range(top_n), top_scores[::-1], color="#1A56A0", edgecolor="white")
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(top_features[::-1], fontsize=10)
    ax.set_xlabel("Importance Score", fontsize=12)
    ax.set_title(f"Top {top_n} Feature Importances — Random Forest", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "feature_importance.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[PLOT] Saved → {path}")


def plot_model_comparison(results: list):
    """Bar chart comparing F1-scores across all models."""
    names = [r["model_name"] for r in results]
    f1s = [r["f1"] for r in results]
    accs = [r["accuracy"] for r in results]

    x = np.arange(len(names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width/2, accs, width, label="Accuracy", color="#42A5F5", edgecolor="white")
    ax.bar(x + width/2, f1s, width, label="F1-Score", color="#EF5350", edgecolor="white")

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Model Comparison — Accuracy & F1-Score", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)

    for i, (a, f) in enumerate(zip(accs, f1s)):
        ax.text(i - width/2, a + 0.01, f"{a:.3f}", ha="center", fontsize=9, fontweight="bold")
        ax.text(i + width/2, f + 0.01, f"{f:.3f}", ha="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(PLOTS_DIR, "model_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[PLOT] Saved → {path}")
