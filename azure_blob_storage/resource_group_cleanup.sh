#!/bin/bash

# Delete resource group

. ./.env

az group delete --name $resourceGroup --yes -y

echo "Resource group $resourceGroup is deleted"