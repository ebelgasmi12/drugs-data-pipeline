
# GCP credentials
# Set JSON file credentials
# if you want to use of auth method
variable credentials {
  type        = string
  default     = "your-credentials-path"
  description = "GCP service account credentials."
}

# GCP Project ID
variable project {
  type        = string
  description = "GCP project."
}

# GKE Cluster name
variable gcs-tf-bucket {
  type        = string
  default     = "mehdib-airfow-tf-state"
  description = "GCS Bucket name (for storing Terraform state)."
}

# GKE Cluster name
variable gke-cluster-name {
  type        = string
  default     = "airflow-cluster"
  description = "GKE Cluster name."
}