from pprint import pprint
from flights import Flights
from airport_code import AirportCode
from model import Model
from push_notifications import PushNotifications
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Launch flight price analizer raccoon-flight."
    )
    # flight date when you want to have a flight
    parser.add_argument(
        "-sf", "--startfrom", default='20/05/2023', help="flight date from",
    )
    # flight date when you want to have a flight 
    parser.add_argument(
        "-st", "--startto", default='11/06/2023', help="flight date to",
    )
     # duration in the destination in nights min
    parser.add_argument(
        "-nl", "--nightslow", default=21, help="duration in the destination in nights min",
    )
    # duration in the destination in nights max
    parser.add_argument(
        "-nb", "--nightsbig", default=28, help="duration in the destination in nights max",
    )
    # max flight duration
    parser.add_argument(
        "-md", "--maxduration", default=15, help="max flight duration",
    )
    
    return parser

def main():
    print('Runnnin raccoon to find the best flight fit for you...\n\n')
    pn = PushNotifications()
    parser = init_argparse()
    args = parser.parse_args()
    fd = Flights()
    data = Model().read()
    for (_, row) in data.iterrows():
        fd = Flights()
        airport = AirportCode()
        res = airport.get_code(row.City)
        row['iataCode'] = res
        try:
            # data = asyncio.run(fd.get_prices(res, args.startfrom, args.startto, row.LowestPrice, row.HighestPrice))
            data = fd.get_round_prices(
                res, 
                args.startfrom, 
                args.startto, 
                row.LowestPrice, 
                row.HighestPrice, 
                args.nightslow, 
                args.nightsbig, 
                args.maxduration
            )
            pprint(data)
            if (len(data) > 0):
                pn.send_email('Best flight prices', data)
        except Exception as e:
            print(f"{row} error: {e}")

if __name__ == '__main__':
    main()