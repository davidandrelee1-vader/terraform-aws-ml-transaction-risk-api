import pytest

from ml.predict import score_transaction
from ml.train import train_and_save


@pytest.fixture(scope="session", autouse=True)
def trained_model():
    train_and_save()


def test_high_risk_scores_above_low_risk():
    low = score_transaction(
        {
            "amount": 24.50,
            "account_age_days": 1800,
            "transactions_last_24h": 1,
            "distance_from_home_km": 2,
            "is_foreign_transaction": 0,
        }
    )
    high = score_transaction(
        {
            "amount": 4500,
            "account_age_days": 3,
            "transactions_last_24h": 15,
            "distance_from_home_km": 700,
            "is_foreign_transaction": 1,
        }
    )
    assert high["risk_score"] > low["risk_score"]
    assert high["risk_level"] == "high"
    assert low["risk_level"] == "low"


def test_missing_feature_is_rejected():
    with pytest.raises(ValueError, match="Missing required features"):
        score_transaction({"amount": 100})
