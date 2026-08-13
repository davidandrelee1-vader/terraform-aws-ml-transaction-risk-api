# Terraform AWS ML Transaction Risk API

An end-to-end machine-learning portfolio project that trains a transaction-risk classifier and deploys it as a low-cost serverless API on AWS using Docker, FastAPI, Lambda, and Terraform.

## Architecture

```text
Client
  |
  v
AWS Lambda Function URL
  |
  v
AWS Lambda Web Adapter
  |
  v
FastAPI Prediction API
  |
  v
Scikit-learn Transaction Risk Model
```

Supporting services:

- Amazon ECR stores the container image.
- Amazon S3 stores the trained model artifact.
- AWS IAM provides least-privilege Lambda execution permissions.
- Amazon CloudWatch receives Lambda logs.
- AWS Budgets sends monthly cost alerts.
- Terraform provisions and manages all AWS resources.

## Project Highlights

- Generates synthetic transaction data with no customer information.
- Performs feature engineering and model training with scikit-learn.
- Handles severe class imbalance using balanced class weights.
- Serves predictions through FastAPI.
- Packages the application in a multi-stage distroless Docker image.
- Uses AWS Lambda Web Adapter for serverless FastAPI deployment.
- Achieved an Amazon ECR security scan with zero findings.
- Includes automated prediction tests.
- Deploys through reusable Terraform infrastructure.
- Configures a $5 monthly AWS Budget with email notifications.

## Model Features

The model evaluates:

- Transaction amount
- Account age in days
- Transactions during the last 24 hours
- Distance from the account holder's home
- Foreign transaction indicator

## Model Evaluation

Current balanced baseline:

| Metric | Result |
|---|---:|
| Accuracy | 71.2% |
| ROC AUC | 0.785 |
| Risk-class recall | 70.0% |
| Risk-class precision | 4.9% |
| Risk-class F1 | 9.2% |

The dataset is intentionally imbalanced. The classifier prioritizes detecting risky transactions, improving risk recall from 0% to 70%. Low precision shows that additional feature engineering, threshold tuning, and real-world validation would be required before production use.

## Technology Stack

- Python
- NumPy
- scikit-learn
- Joblib
- FastAPI
- Uvicorn
- Pytest
- Docker
- Google Distroless
- AWS Lambda Web Adapter
- AWS Lambda
- Amazon ECR
- Amazon S3
- AWS IAM
- AWS Budgets
- Terraform

## Project Structure

```text
.
├── ml/
│   ├── api.py
│   ├── features.py
│   ├── predict.py
│   └── train.py
├── tests/
│   └── test_predict.py
├── Dockerfile
├── budget.tf
├── ecr.tf
├── lambda.tf
├── main.tf
├── provider.tf
├── variable.tf
├── version.tf
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Run Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Train the model:

```powershell
python -m ml.train
```

Run tests:

```powershell
python -m pytest -q
```

Start the API:

```powershell
python -m uvicorn ml.api:app --reload
```

Open the interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## Run with Docker

Build the image:

```powershell
docker build -t transaction-risk-api .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 transaction-risk-api
```

Test its health:

```text
http://127.0.0.1:8000/health
```

## Deploy with Terraform

Set the budget-notification email locally:

```powershell
$env:TF_VAR_budget_email = "your-email@example.com"
```

Deploy:

```powershell
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Retrieve the API URL:

```powershell
terraform output -raw inference_api_url
```

## API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### Risk Prediction

```http
POST /predict
Content-Type: application/json
```

Example request:

```json
{
  "amount": 5000,
  "account_age_days": 10,
  "transactions_last_24h": 20,
  "distance_from_home_km": 1000,
  "is_foreign_transaction": 1
}
```

Example response:

```json
{
  "risk_score": 1.0,
  "risk_level": "high",
  "model_version": "1.0.0"
}
```

## Security and Cost Controls

- Distroless runtime image reduces the container attack surface.
- ECR scans container images when pushed.
- The deployed Lambda image completed its ECR scan with zero findings.
- Terraform state, model binaries, virtual environments, datasets, and credentials are excluded from Git.
- Lambda avoids always-running server costs.
- AWS Budget notifications are configured at 80% actual and 100% forecasted usage of a $5 monthly budget.

## Important Security Note

The Lambda Function URL uses public access for demonstration purposes. A production system should add authentication, request throttling, monitoring, input controls, and an API-management layer.

## Cleanup

To remove billable deployment resources:

```powershell
terraform destroy
```

Review the plan carefully before approving destruction.
