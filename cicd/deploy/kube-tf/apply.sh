
# Get script directory (allows to launch script from anywhere)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Terraform deploy commands
terraform init $SCRIPT_DIR
terraform get $SCRIPT_DIR
terraform apply -auto-approve -var="project=$PROJECT_ID" $SCRIPT_DIR