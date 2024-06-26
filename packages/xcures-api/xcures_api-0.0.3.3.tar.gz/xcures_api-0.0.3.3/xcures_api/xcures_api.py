import os
import requests
import logging
import time
import json
from yaml_config_day.config_manager import ProjectConfigManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class XCuresAPI:
    def __init__(self, config_path=None):
        if config_path is None:
            xcures_env = os.getenv('XCURES_ENV', 'n/a')
            if xcures_env == 'n/a':
                raise ValueError("XCURES_ENV not set.")
        
        self.config = ProjectConfigManager("xcures", xcures_env).get_config()

        self.base_url = self.config['base_url']
        self.base_auth_url = self.config['base_auth_url']
        self.project_id = self.config['project_id']
        self.client_id = self.config['client_id']
        self.client_secret = self.config['client_secret']
        
        self.token = self.get_token()

    def get_token(self):
        url = f"{self.base_auth_url}/oauth/token"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": "patient-registry-public-api",
            "grant_type": "client_credentials"
        }
        
        logging.info(f"Requesting token from {url}")
        response = requests.post(url, json=data, headers=headers)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response content: {response.content}")
        
        response.raise_for_status()
        return response.json()["access_token"]

    def get_headers(self, content_type="application/json"):
        return {
            "Authorization": f"Bearer {self.token}",
            "ProjectId": self.project_id,
            "Content-Type": content_type
        }


    def subject(self):
        url = f"{self.base_url}/api/v1/patient-registry/subject"
        headers = self.get_headers() 
        x = {
            "Authorization": f"Bearer {self.token}",
            "ProjectId": self.project_id,
        }
        
        logging.info(f"Testing authentication with GET request to {url}")
        response = requests.get(url, headers=headers)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response content: {response.content}")
        
        response.raise_for_status()
        return response.json()


    def patient_query(self, query_data):
        url = f"{self.base_url}/api/v1/patient-registry/query"
        headers = self.get_headers()
        logging.info(f"Sending query to {url} with data {query_data}")
        
        response = requests.post(url,  json=query_data, headers=headers)
        response.raise_for_status()
        return response.json()

# Usage example:
if __name__ == "__main__":
    # Ensure the environment variable XCURES_ENV is set
    os.environ['XCURES_ENV'] = 'prod'
    
    xcures_api = XCuresAPI()

    logging.info(f"XCURES_ENV: {os.getenv('XCURES_ENV')}")
    logging.info(""f"Project ID: {xcures_api.project_id}")
    logging.info("Querying all subjects in the project...")

    # Querying subjects works
    xcures_api.subject()


    # Querying patients DOES NOT appear to work... however, it might be there is no data... check with their support
    # and/or maybe this concept is not appropriate for us ATM...?
    # query_data = {
    #    "pageNumber": 1,
    #    "pageSize": 50,
    #    "sortField": "created",
    #    "sortIsDescending": False,
    #}
    
    #try:
    #    result = xcures_api.patient_query(query_data)
    #    print(result)
    #except Exception as e:
    #    logging.error(f"Error querying patients: {e}")
