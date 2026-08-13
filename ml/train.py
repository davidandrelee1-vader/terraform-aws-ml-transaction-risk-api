"""Train a reproducible transaction-risk classifier on synthetic data."""

from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml.features import FEATURE_NAMES

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "model" / "transaction_risk_model.joblib"
RANDOM_SEED = 42


def generate_training_data(rows: int = 12_000) -> tuple[np.ndarray, np.ndarray]:
    """Generate synthetic transactions containing no customer information."""
    rng = np.random.default_rng(RANDOM_SEED)
    amount = np.clip(rng.lognormal(4.2, 1.1, rows), 1, 10_000)
    account_age = rng.integers(1, 3_650, rows)
    recent_transactions = np.clip(rng.poisson(3, rows), 0, 30)
    distance = np.clip(rng.exponential(35, rows), 0, 1_000)
    foreign = rng.binomial(1, 0.12, rows)
    features = np.column_stack(
        [amount, account_age, recent_transactions, distance, foreign]
    )

    signal = (
        0.0010 * amount
        - 0.0012 * account_age
        + 0.22 * recent_transactions
        + 0.009 * distance
        + 1.6 * foreign
        - 4.2
        + rng.normal(0, 0.8, rows)
    )
    labels = rng.binomial(1, 1 / (1 + np.exp(-signal)))
    return features, labels


def train_and_save() -> dict[str, float]:
    features, labels = generate_training_data()
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=labels,
    )
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1_000, class_weight="balanced", random_state=RANDOM_SEED)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    probabilities = pipeline.predict_proba(x_test)[:, 1]

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": pipeline, "features": FEATURE_NAMES, "version": "1.0.0"},
        MODEL_PATH,
    )
    print(classification_report(y_test, predictions, digits=3))
    metrics = {"roc_auc": float(roc_auc_score(y_test, probabilities))}
    print(f"ROC AUC: {metrics['roc_auc']:.3f}")
    print(f"Saved model: {MODEL_PATH}")
    return metrics


if __name__ == "__main__":
    train_and_save()
