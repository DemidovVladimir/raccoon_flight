import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(".env")

class AirportCode:
    envs = os.environ.copy()
    headers = {
        'accept': 'application/json',
        'apikey': ''
    }

    def __init__(self):
        self.headers['apikey'] = self.envs['TEQUILA_API_KEY']

    def get_code(self, code: str) -> str:
        with requests.Session() as session:
            with session.get(f'https://api.tequila.kiwi.com/locations/query?term={code}&locale=en-US&location_types=airport&limit=10&active_only=true', headers=self.headers) as response:
                return json.loads(response.content)['locations'][0]['code']
