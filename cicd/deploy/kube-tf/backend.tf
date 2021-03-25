# Use GCS as Terraform Backend
# to store state
terraform {
  backend "gcs" {
    bucket      = var.gcs-tf-bucket
  }
}