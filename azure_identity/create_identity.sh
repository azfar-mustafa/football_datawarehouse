#!/bin/bash

# Inititalize variable
. ./.env

# To create user managed identity
az identity create --name $identity --resource-group $resourceGroup --location "$location"

echo "User identity $identity is created"