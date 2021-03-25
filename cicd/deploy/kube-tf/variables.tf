
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
variable gke_cluster_name {
  type        = string
  default     = "airflow-cluster"
  description = "GKE Cluster name."
}