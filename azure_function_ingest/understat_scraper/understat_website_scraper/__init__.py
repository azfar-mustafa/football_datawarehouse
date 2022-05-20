import logging, json, tempfile, os, pendulum
import requests
from bs4 import BeautifulSoup
import json

import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    current_date = pendulum.today('Asia/Kuala_Lumpur')
    current_date = current_date.format('DDMMYYYY')

    def extract_data(club):
        url = f"http://understat.com/team/{club}/2021"
        res = requests.get(url) # Use requests package to get the url content
        soup = BeautifulSoup(res.content, 'lxml') # Use lxml to parse HTML
        scripts = soup.find_all('script') # Select script tag only
        strings = scripts[3].string # To select player statistics data and turn into string
        # Set the index to slice the string
        ind_start = strings.index("('")+2
        ind_end = strings.index(")")
        json_data = strings[ind_start:ind_end]
        json_data = json_data.encode('utf8').decode('unicode_escape') # Convert data into proper dictionary
        json_data = json_data[:-1] # This step is to remove apostrophe at the end of the string
        data = json.loads(json_data) # Convert data into json format
        return data

    def create_container():
        container_name = 'staging'
        container = ContainerClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=azfarstorageaccountblob;AccountKey=+uK9057ZIKHs2DGaGYkFcLdgi3SoWDcdE+JvU9cCgjEbPZVQPxUjWzdwyM7Du+IMI2lE16ibUFHm+AStFOlhNQ==;EndpointSuffix=core.windows.net", container_name)
        # Check if container exists or not. If not, create one
        if container.exists():
            logging.info(f"Container {container_name} has been created")
        else:
            container.create_container()
            logging.info(f"Created {container_name}")


    def upload_file(json_data, club):
        club = club.replace(' ','')
        filename = f"{club}_{current_date}.json"
        local_filepath = tempfile.gettempdir() # Get the directory for temporary files
        filepath = os.path.join(local_filepath, filename)
        container_name = 'staging'
        credential = DefaultAzureCredential()
        account_url = "https://azfarstorageaccountblob.blob.core.windows.net/"

        #blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=azfarstorageaccountblob;AccountKey=+uK9057ZIKHs2DGaGYkFcLdgi3SoWDcdE+JvU9cCgjEbPZVQPxUjWzdwyM7Du+IMI2lE16ibUFHm+AStFOlhNQ==;EndpointSuffix=core.windows.net")

        client = BlobServiceClient(account_url=account_url, credential=credential)
        blob_client = client.get_blob_client(container=container_name, blob=filename)
        #blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename) # Create a blob client to intertact with Blob Service  

        # Store json object into a json file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        # Upload file into blob
        with open(filepath, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)


    try:
        team = "Manchester City"
        scraped_data = extract_data(team)
        upload_file(scraped_data, team)     
    except Exception as e:
        logging.info(e)
        return func.HttpResponse(
             "There is an error in the function.",
             status_code=200
        )
    return func.HttpResponse(f"File is uploaded {current_date}")