variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "name of the project"
  type        = string
  default     = "Terraform-ml-project"
}
