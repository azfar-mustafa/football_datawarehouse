#!/bin/bash

# Initialize variable
. ./.env

# Assign identity to the app
az webapp identity assign --resource-group $resourceGroup --name $appName --identities $resourceid