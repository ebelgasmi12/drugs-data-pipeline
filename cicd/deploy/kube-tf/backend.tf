# Use GCS as Terraform Backend
# to store state
terraform {
  backend "gcs" {
    bucket      = "mehdib-airfow-tf-state"
  }
}