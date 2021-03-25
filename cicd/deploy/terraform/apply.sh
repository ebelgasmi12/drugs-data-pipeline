
#!/bin/bash

# Get script directory (allows to launch script from anywhere)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# If the Branch is PROD
if [ $BRANCH_NAME = "prod" ]
then
    echo "********************************* APPLYING ************************************"
    echo "Execucting terraform command in folder: $SCRIPT_DIR"
    echo "*******************************************************************************"
    # Terraform deploy commands
    terraform init $SCRIPT_DIR
    terraform get $SCRIPT_DIR
    terraform apply -auto-approve -var="project=$PROJECT_ID" $SCRIPT_DIR
else
    echo "***************************** SKIPPING APPLYING *******************************"
    echo "Branch '$BRANCH_NAME' does not represent an oficial environment."
    echo "*******************************************************************************"
fi


