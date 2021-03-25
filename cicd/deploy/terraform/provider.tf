# GCP Provider
# Uncomment credentials if you want
# to use JSON file authentication
provider "google" {
    project = "mehdib-airflow-project" 
    region = "europe-west1-b"
    # credentials = "${file("${var.credentials}")}"
}

# google_client_config and kubernetes provider must be explicitly specified like the following.
data "google_client_config" "default" {}

provider "kubernetes" {
  load_config_file       = false
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}