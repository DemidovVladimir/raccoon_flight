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

    async def get_prices(self, fly_to, date_from, date_to, price_from, price_to) -> dict:
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

    async def get_round_prices(self, fly_to, date_from, date_to, price_from, price_to, nights_in_dst_from, nights_in_dst_to, max_fly_duration) -> dict:
        self.url = f"{self.url}&fly_to={fly_to}&dateFrom={date_from}&dateTo={date_to}&price_from={price_from}&price_to={price_to}&nights_in_dst_from={nights_in_dst_from}&nights_in_dst_to={nights_in_dst_to}&max_fly_duration={max_fly_duration}"
        try: 
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    data = await response.json()
                    # you can filter data here...
                    # data = [{x: y for x, y in n.items() if x in ['cityTo', 'conversion', 'countryTo', 'has_airport_change', 'price', 'local_departure', 'local_arrival']} for n in data.get('data') if (n.get('pnr_count') < 2) and (n.get('availability').get('seats') is not None) and int(n.get('availability').get('seats', 0)) > 3]
                    return data
        except Exception as e:
            print(e)
            return {}