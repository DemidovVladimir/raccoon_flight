from pprint import pprint
from flights import Flights
from airport_code import AirportCode
from model import Model
from push_notifications import PushNotifications
import datetime
import asyncio
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Launch flight price analizer raccoon-flight."
    )
    # flight date when you want to have a flight in hours
    parser.add_argument(
        "-s", "--start", default=10, help="flight date when you want to have a flight in hours",
    )
    # duration of the vacation or time been in the location in hours as well
    parser.add_argument(
        "-d", "--duration", default=100, help="duration of the vacation or time been in the location in hours as well",
    )
    return parser

if __name__ == '__main__':
    pn = PushNotifications()
    parser = init_argparse()
    args = parser.parse_args()
    fd = Flights()
    data = Model().read()
    for (index, row) in data.iterrows():
        fd = Flights()
        airport = AirportCode()
        res = airport.get_code(row.City)
        row['iataCode'] = res
        dateFrom = datetime.datetime.now() + datetime.timedelta(hours=args.start)
        dateTo = dateFrom + datetime.timedelta(hours=168)
        returnFrom = dateTo + datetime.timedelta(hours=args.duration)
        returnTo = returnFrom + datetime.timedelta(hours=48)
        try:
            # data = asyncio.run(fd.get_prices(res, dateFrom, dateTo, row.get('lowestPrice'), row.get('highestPrice')))
            data = asyncio.run(fd.get_round_prices(res, dateFrom, dateTo, row.LowestPrice, row.HighestPrice, returnFrom, returnTo))
            pprint(data)
            pn.send_email('new flight prices', data)
        except Exception as e:
            print(f"{row} error: {e}")
