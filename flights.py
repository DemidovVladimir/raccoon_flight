import requests
import json
from pprint import pprint
import aiohttp
import asyncio
import os
from dotenv import load_dotenv
load_dotenv(".env")

class Flights:
    envs = os.environ.copy()
    url = ""
    headers = {
        'accept': 'application/json',
        'apikey': ''
    }

    def __init__(self):
        self.headers['apikey'] = self.envs.get('TEQUILA_API_KEY')
        self.url = f"{self.envs.get('TEQUILA_API')}/search?fly_from=BER&technical_stops=0&sort=price"

    async def get_prices(self, fly_to, dateFrom, dateTo, price_from, price_to) -> dict:
        date_from = f"{dateFrom.strftime('%d')}/{dateFrom.strftime('%m')}/{dateFrom.strftime('%Y')}"
        date_to = f"{dateTo.strftime('%d')}/{dateTo.strftime('%m')}/{dateTo.strftime('%Y')}"
        self.url = f"{self.url}&fly_to={fly_to}&dateFrom={date_from}&dateTo={date_to}&price_from={price_from}&price_to={price_to}"
        try: 
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    data = await response.json()
                    data = [{x: y for x, y in n.items() if x in ['cityTo', 'conversion', 'countryTo', 'has_airport_change', 'price', 'local_departure', 'local_arrival']} for n in data.get('data') if (n.get('pnr_count') < 2) and (n.get('availability').get('seats') is not None) and int(n.get('availability').get('seats', 0)) > 3]
                    return data
        except Exception as e:
            print(e)
            return {}

    async def get_round_prices(self, fly_to, dateFrom, dateTo, price_from, price_to, returnFrom, returnTo) -> dict:
        date_from = f"{dateFrom.strftime('%d')}/{dateFrom.strftime('%m')}/{dateFrom.strftime('%Y')}"
        date_to = f"{dateTo.strftime('%d')}/{dateTo.strftime('%m')}/{dateTo.strftime('%Y')}"
        return_from = f"{returnFrom.strftime('%d')}/{returnFrom.strftime('%m')}/{returnFrom.strftime('%Y')}"
        return_to = f"{returnTo.strftime('%d')}/{returnTo.strftime('%m')}/{returnTo.strftime('%Y')}"
        self.url = f"{self.url}&fly_to={fly_to}&dateFrom={date_from}&dateTo={date_to}&price_from={price_from}&price_to={price_to}&return_from={return_from}&return_to={return_to}"
        try: 
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    data = await response.json()
                    data = [{x: y for x, y in n.items() if x in ['cityTo', 'conversion', 'countryTo', 'has_airport_change', 'price', 'local_departure', 'local_arrival']} for n in data.get('data') if (n.get('pnr_count') < 2) and (n.get('availability').get('seats') is not None) and int(n.get('availability').get('seats', 0)) > 3]
                    return data
        except Exception as e:
            print(e)
            return {}