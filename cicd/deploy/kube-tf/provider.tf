# GCP Provider
# Uncomment credentials if you want
# to use JSON file authentication
provider "google" {
    project = "mehdib-airflow-project" 
    region = "europe-west1-b"
    # credentials = "${file("${var.credentials}")}"
}