#!/bin/bash

# Initialize variable
. ./.env

# Assign identity to the app
az webapp identity assign --resource-group $resourceGroup --name $appName --identities $resourceid

az role assignment create --role "Storage Blob Data Reader" --assignee $principalid