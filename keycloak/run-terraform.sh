#!/bin/sh

export TF_VAR_user_password
TF_VAR_user_password=$(uuidgen)

terraform init
terraform apply -auto-approve
