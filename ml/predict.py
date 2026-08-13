"""Score a transaction with the trained risk model."""

from pathlib import Path
from typing import Any

import joblib

from ml.features import FEATURE_NAMES

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "transaction_risk_model.joblib"


def load_model() -> dict[str, Any]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model missing. Run: python -m ml.train")
    return joblib.load(MODEL_PATH)


def score_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    missing = [name for name in FEATURE_NAMES if name not in transaction]
    if missing:
        raise ValueError(f"Missing required features: {', '.join(missing)}")

    values = [[float(transaction[name]) for name in FEATURE_NAMES]]
    probability = float(load_model()["model"].predict_proba(values)[0, 1])
    return {
        "risk_score": round(probability, 4),
        "risk_level": "high" if probability >= 0.65 else "low",
        "model_version": "1.0.0",
    }
