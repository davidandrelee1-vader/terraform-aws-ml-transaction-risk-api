from fastapi import FastAPI
from pydantic import BaseModel

from ml.predict import score_transaction

app = FastAPI(title="Transaction Risk API")


class Transaction(BaseModel):
    amount: float
    account_age_days: float
    transactions_last_24h: float
    distance_from_home_km: float
    is_foreign_transaction: float


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(transaction: Transaction):
    return score_transaction(transaction.model_dump())
