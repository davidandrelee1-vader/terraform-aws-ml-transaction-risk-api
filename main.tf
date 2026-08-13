#S3 BUCKET CREATION

resource "aws_s3_bucket" "main_object" {
  bucket = "terraform-ml-model-dav44"

  tags = {
    Name        = "terraform-ML"
    enviornment = "dev"
  }

}

resource "aws_s3_object" "model" {
  bucket      = aws_s3_bucket.main_object.id
  key         = "model/transaction_risk_model.joblib"
  source      = "${path.module}/model/transaction_risk_model.joblib"
  source_hash = filemd5("${path.module}/model/transaction_risk_model.joblib")
}
