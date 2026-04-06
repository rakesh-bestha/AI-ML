"""
main.py
-------
Entry point for the Network Traffic Anomaly Detection pipeline.

Usage:
    python main.py

Runs the complete pipeline:
  1. Load NSL-KDD data
  2. Binarize labels (normal vs attack)
  3. Preprocess (encode + scale)
  4. Feature engineering (variance filter)
  5. Train all models
  6. Evaluate all models
  7. Save predictions and metrics to SQLite
  8. Generate all visualizations
"""

import sys
import os

# Add src/ to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_loader import load_data, binarize_labels
from preprocessor import Preprocessor
from feature_engineering import FeatureEngineer
from train import train_all
from evaluate import evaluate_all
from database import initialize_db, save_metrics, save_predictions, save_feature_importance
from visualize import (
    plot_label_distribution,
    plot_correlation_heatmap,
    plot_confusion_matrix,
    plot_roc_curves,
    plot_feature_importance,
    plot_model_comparison
)


def main():
    print("\n" + "="*60)
    print("   NETWORK TRAFFIC ANOMALY DETECTION — ML PIPELINE")
    print("="*60 + "\n")

    # ── Step 1: Load Data ──────────────────────────────────────
    df_train, df_test = load_data()

    # ── Step 2: Binarize Labels ───────────────────────────────
    df_train = binarize_labels(df_train)
    df_test  = binarize_labels(df_test)

    # ── Step 3: Preprocessing ─────────────────────────────────
    preprocessor = Preprocessor()
    X_train, y_train = preprocessor.fit_transform(df_train)
    X_test,  y_test  = preprocessor.transform(df_test)
    preprocessor.save()

    feature_names = preprocessor.feature_names

    # ── Step 4: Feature Engineering ───────────────────────────
    fe = FeatureEngineer(variance_threshold=0.01, apply_pca=False)
    X_train_fe, selected_features = fe.fit_transform(X_train, feature_names)
    X_test_fe = fe.transform(X_test)
    fe.save()

    # ── Step 5: Train Models ───────────────────────────────────
    models = train_all(X_train_fe, y_train)

    # ── Step 6: Evaluate Models ───────────────────────────────
    results = evaluate_all(models, X_test_fe, y_test)

    # ── Step 7: Persist to SQLite ─────────────────────────────
    initialize_db()
    save_metrics(results)

    for r in results:
        save_predictions(r["model_name"], y_test, r["y_pred"])

    # Save Random Forest feature importances
    rf_model = models.get("random_forest")
    if rf_model and hasattr(rf_model, "feature_importances_"):
        save_feature_importance(selected_features, rf_model.feature_importances_, top_n=20)

    # ── Step 8: Visualizations ────────────────────────────────
    print("\n[INFO] Generating visualizations...")

    plot_label_distribution(y_train, y_test)
    plot_correlation_heatmap(X_train_fe, selected_features, top_n=min(20, len(selected_features)))

    for r in results:
        if r.get("confusion_matrix") is not None:
            plot_confusion_matrix(r["confusion_matrix"], r["model_name"])

    plot_roc_curves(models, X_test_fe, y_test)

    if rf_model and hasattr(rf_model, "feature_importances_"):
        plot_feature_importance(rf_model, selected_features, top_n=20)

    plot_model_comparison(results)

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "="*60)
    print("   PIPELINE COMPLETE")
    print("="*60)
    print(f"\n{'Model':<30} {'Accuracy':>10} {'F1-Score':>10}")
    print("-" * 52)
    for r in sorted(results, key=lambda x: x["f1"], reverse=True):
        print(f"{r['model_name']:<30} {r['accuracy']:>10.4f} {r['f1']:>10.4f}")

    print(f"\n✅ Plots saved   → outputs/plots/")
    print(f"✅ Models saved  → outputs/models/")
    print(f"✅ Database      → outputs/predictions.db")
    print()


if __name__ == "__main__":
    main()
