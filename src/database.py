"""
database.py
-----------
SQLite persistence layer for storing model predictions,
evaluation metrics, and feature importance scores.
Uses only the Python standard library (sqlite3).
"""

import sqlite3
import os
import json
from datetime import datetime

DB_PATH = "outputs/predictions.db"


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db(db_path: str = DB_PATH):
    """
    Create all required tables if they don't exist.
    Tables:
        - model_metrics   : Stores evaluation results per model per run
        - predictions     : Stores per-sample predictions
        - feature_importance : Top N feature importances (Random Forest)
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS model_metrics (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date    TEXT NOT NULL,
            model_name  TEXT NOT NULL,
            accuracy    REAL,
            precision   REAL,
            recall      REAL,
            f1_score    REAL,
            roc_auc     REAL
        );

        CREATE TABLE IF NOT EXISTS predictions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date    TEXT NOT NULL,
            model_name  TEXT NOT NULL,
            sample_idx  INTEGER,
            true_label  INTEGER,
            pred_label  INTEGER,
            is_correct  INTEGER
        );

        CREATE TABLE IF NOT EXISTS feature_importance (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date        TEXT NOT NULL,
            feature_name    TEXT NOT NULL,
            importance_score REAL,
            rank            INTEGER
        );
    """)

    conn.commit()
    conn.close()
    print(f"[DB] Database initialized at {db_path}")


def save_metrics(metrics_list: list, db_path: str = DB_PATH):
    """
    Persist model evaluation metrics to the model_metrics table.

    Args:
        metrics_list: List of dicts from evaluate.evaluate_all()
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for m in metrics_list:
        cur.execute("""
            INSERT INTO model_metrics (run_date, model_name, accuracy, precision, recall, f1_score, roc_auc)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            run_date,
            m.get("model_name", "Unknown"),
            m.get("accuracy"),
            m.get("precision"),
            m.get("recall"),
            m.get("f1"),
            m.get("roc_auc")
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Saved {len(metrics_list)} model metric records.")


def save_predictions(model_name: str, y_true, y_pred, db_path: str = DB_PATH):
    """
    Persist per-sample predictions (first 5000 records for efficiency).
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    limit = min(len(y_true), 5000)
    rows = [
        (run_date, model_name, int(i), int(y_true[i]), int(y_pred[i]), int(y_true[i] == y_pred[i]))
        for i in range(limit)
    ]

    cur.executemany("""
        INSERT INTO predictions (run_date, model_name, sample_idx, true_label, pred_label, is_correct)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()
    print(f"[DB] Saved {limit} prediction records for '{model_name}'.")


def save_feature_importance(feature_names: list, importance_scores, top_n: int = 20, db_path: str = DB_PATH):
    """
    Persist top N feature importances from Random Forest.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pairs = sorted(zip(feature_names, importance_scores), key=lambda x: x[1], reverse=True)[:top_n]

    rows = [
        (run_date, name, float(score), rank + 1)
        for rank, (name, score) in enumerate(pairs)
    ]

    cur.executemany("""
        INSERT INTO feature_importance (run_date, feature_name, importance_score, rank)
        VALUES (?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()
    print(f"[DB] Saved top {top_n} feature importances.")


def fetch_metrics_summary(db_path: str = DB_PATH):
    """
    Fetch latest run metrics for all models.
    Returns list of Row objects.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT model_name, accuracy, precision, recall, f1_score, roc_auc
        FROM model_metrics
        WHERE run_date = (SELECT MAX(run_date) FROM model_metrics)
        ORDER BY f1_score DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
