#!/bin/bash

# Deploy azure function

. ./.env

( cd understat_scraper && func azure functionapp publish $appName )

echo "$appName is published"