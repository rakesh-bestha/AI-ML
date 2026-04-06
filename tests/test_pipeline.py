"""
test_pipeline.py
----------------
Unit tests for the anomaly detection pipeline components.
Run with: python -m pytest tests/ -v
"""

import sys
import os
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from preprocessor import Preprocessor
from feature_engineering import FeatureEngineer
from database import initialize_db, save_metrics, get_connection


# ── Fixtures ──────────────────────────────────────────────────

@pytest.fixture
def sample_df():
    """Generate a tiny synthetic DataFrame matching NSL-KDD structure."""
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "duration":        np.random.randint(0, 1000, n),
        "protocol_type":   np.random.choice(["tcp", "udp", "icmp"], n),
        "service":         np.random.choice(["http", "ftp", "smtp", "ssh"], n),
        "flag":            np.random.choice(["SF", "S0", "REJ"], n),
        "src_bytes":       np.random.randint(0, 100000, n),
        "dst_bytes":       np.random.randint(0, 100000, n),
        "land":            np.zeros(n, dtype=int),
        "wrong_fragment":  np.zeros(n, dtype=int),
        "urgent":          np.zeros(n, dtype=int),
        "hot":             np.random.randint(0, 10, n),
        "num_failed_logins": np.zeros(n, dtype=int),
        "logged_in":       np.random.randint(0, 2, n),
        "num_compromised": np.zeros(n, dtype=int),
        "root_shell":      np.zeros(n, dtype=int),
        "su_attempted":    np.zeros(n, dtype=int),
        "num_root":        np.zeros(n, dtype=int),
        "num_file_creations": np.zeros(n, dtype=int),
        "num_shells":      np.zeros(n, dtype=int),
        "num_access_files": np.zeros(n, dtype=int),
        "num_outbound_cmds": np.zeros(n, dtype=int),
        "is_host_login":   np.zeros(n, dtype=int),
        "is_guest_login":  np.zeros(n, dtype=int),
        "count":           np.random.randint(1, 512, n),
        "srv_count":       np.random.randint(1, 512, n),
        "serror_rate":     np.random.uniform(0, 1, n),
        "srv_serror_rate": np.random.uniform(0, 1, n),
        "rerror_rate":     np.random.uniform(0, 1, n),
        "srv_rerror_rate": np.random.uniform(0, 1, n),
        "same_srv_rate":   np.random.uniform(0, 1, n),
        "diff_srv_rate":   np.random.uniform(0, 1, n),
        "srv_diff_host_rate": np.random.uniform(0, 1, n),
        "dst_host_count":  np.random.randint(1, 255, n),
        "dst_host_srv_count": np.random.randint(1, 255, n),
        "dst_host_same_srv_rate": np.random.uniform(0, 1, n),
        "dst_host_diff_srv_rate": np.random.uniform(0, 1, n),
        "dst_host_same_src_port_rate": np.random.uniform(0, 1, n),
        "dst_host_srv_diff_host_rate": np.random.uniform(0, 1, n),
        "dst_host_serror_rate": np.random.uniform(0, 1, n),
        "dst_host_srv_serror_rate": np.random.uniform(0, 1, n),
        "dst_host_rerror_rate": np.random.uniform(0, 1, n),
        "dst_host_srv_rerror_rate": np.random.uniform(0, 1, n),
        "label":           np.random.randint(0, 2, n),
    })
    return df


# ── Preprocessor Tests ────────────────────────────────────────

class TestPreprocessor:
    def test_fit_transform_shape(self, sample_df):
        pre = Preprocessor()
        X, y = pre.fit_transform(sample_df)
        assert X.shape[0] == len(sample_df)
        assert X.shape[1] == len(sample_df.columns) - 1  # minus label
        assert len(y) == len(sample_df)

    def test_transform_unseen_labels(self, sample_df):
        pre = Preprocessor()
        X_train, y_train = pre.fit_transform(sample_df)

        # Test data with an unseen protocol_type
        test_df = sample_df.copy()
        test_df["protocol_type"] = "unknown_protocol"
        X_test, y_test = pre.transform(test_df)
        assert X_test.shape == X_train.shape

    def test_labels_are_binary(self, sample_df):
        pre = Preprocessor()
        _, y = pre.fit_transform(sample_df)
        assert set(np.unique(y)).issubset({0, 1})


# ── Feature Engineering Tests ─────────────────────────────────

class TestFeatureEngineer:
    def test_fit_transform_reduces_features(self, sample_df):
        pre = Preprocessor()
        X, _ = pre.fit_transform(sample_df)
        fe = FeatureEngineer(variance_threshold=0.01)
        X_fe, names = fe.fit_transform(X, pre.feature_names)
        assert X_fe.shape[0] == X.shape[0]
        assert X_fe.shape[1] <= X.shape[1]

    def test_transform_matches_fit(self, sample_df):
        pre = Preprocessor()
        X, _ = pre.fit_transform(sample_df)
        fe = FeatureEngineer(variance_threshold=0.0)
        X_fe, _ = fe.fit_transform(X)
        X_transformed = fe.transform(X)
        assert X_transformed.shape == X_fe.shape


# ── Database Tests ────────────────────────────────────────────

class TestDatabase:
    TMP_DB = "outputs/test_predictions.db"

    def test_initialize_creates_tables(self):
        initialize_db(self.TMP_DB)
        conn = get_connection(self.TMP_DB)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cur.fetchall()}
        conn.close()
        assert "model_metrics" in tables
        assert "predictions" in tables
        assert "feature_importance" in tables

    def test_save_metrics(self):
        initialize_db(self.TMP_DB)
        metrics = [{
            "model_name": "Test Model",
            "accuracy": 0.95,
            "precision": 0.94,
            "recall": 0.96,
            "f1": 0.95,
            "roc_auc": 0.97
        }]
        save_metrics(metrics, self.TMP_DB)
        conn = get_connection(self.TMP_DB)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM model_metrics WHERE model_name='Test Model'")
        count = cur.fetchone()[0]
        conn.close()
        assert count >= 1
