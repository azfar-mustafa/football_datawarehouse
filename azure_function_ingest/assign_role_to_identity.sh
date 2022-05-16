#!/bin/bash

# Initialize variable
. ./.env

# Assign storage blob data reader to user identity
az role assignment create --role "Storage Blob Data Reader" --assignee $principalid