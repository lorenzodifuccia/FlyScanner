import time
import datetime
import requests

from providers import HEADER_DEFAULT


class Ryanair:
    NAME = "Ryanair"

    # Static
    BASE_URL = "https://www.ryanair.com"

    HOME_PATH = "/it/it"

    SEARCH_PATH = "/api/booking/v4/it-it/availability" \
                  "?ADT={adults}&CHD=0&Destination={destination_iata}&Disc=0&INF=0&Origin={departure_iata}&" \
                  "TEEN=0&promoCode=&IncludeConnectingFlights=false&DateOut={date}&" \
                  "FlexDaysOut=0&FlexDaysBeforeOut=0&RoundTrip=false&ToUs=AGREED"

    AUTOCOMPLETE_PATH = "/api/locate/v1/autocomplete/airports?phrase={0}&market=it-it"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = HEADER_DEFAULT.copy()

        # Debug
        # self.session.proxies = {"http": "http://127.0.0.1:8080", "https": "https://127.0.0.1:8080"}
        # self.session.verify = False

        self.__init_cookies()

    def __init_cookies(self):
        self.session.cookies.clear()

        resp_home = self.session.get(self.BASE_URL + self.HOME_PATH)
        if resp_home.status_code != 200:
            raise Exception("invalid response: %s" % resp_home)

        self.session.headers["Referer"] = self.BASE_URL + self.HOME_PATH

    # Location
    def prepare_location(self, location: dict):
        if "iata" not in location or not location["iata"]:
            return False

        for autocomplete in self.autocomplete(location["iata"]):
            if autocomplete["code"] == location["iata"]:
                autocomplete["iata"] = autocomplete["code"]
                return autocomplete

            return False

        return False

    # Search
    def search(self, num_adults: int, date: str, departure: dict, destination: dict):
        time.sleep(1)

        resp_search = self.session.get(self.BASE_URL + self.SEARCH_PATH.format(
            adults=num_adults,
            date=date,
            departure_iata=departure["iata"],
            destination_iata=destination["iata"]
        ))

        if resp_search.status_code == 404 and "No HTTP resource was found" in resp_search.text:
            print("[!] No flight info or IP Blocked")
            return {"date": date, "result": []}

        elif resp_search.status_code != 200:
            raise Exception("invalid response: %s" % resp_search)

        resp_data = resp_search.json()

        price_currency = resp_data.get("currency", "N/D")
        departure_location = resp_data["trips"][0]["originName"] + " - " + resp_data["trips"][0]["origin"]
        arrival_location = resp_data["trips"][0]["destinationName"] + " - " + resp_data["trips"][0]["destination"]

        search_data = resp_data["trips"][0]["dates"][0]["flights"]

        for flight in search_data:
            if flight["faresLeft"] == 0:
                continue

            price = flight["regularFare"]["fares"][0]["amount"]

            trip_stops = []
            trip_stops_duration = datetime.timedelta()
            last_arrival_time = None
            for segment in flight["segments"]:
                segment_departure_time = datetime.datetime.fromisoformat(segment["time"][0])

                if last_arrival_time:
                    trip_stops_duration += segment_departure_time - last_arrival_time

                last_arrival_time = datetime.datetime.fromisoformat(segment["time"][1])

                trip_stops.append({
                    "departure_location": segment["origin"],
                    "arrival_location": segment["destination"],
                    "departure_date": segment["time"][0],
                    "arrival_date": segment["time"][1],
                    "duration": segment["duration"]
                })

            flight["price"] = price
            flight["price_currency"] = price_currency
            flight["departure_date"] = flight["time"][0]
            flight["arrival_date"] = flight["time"][1]
            flight["departure_location"] = departure_location
            flight["arrival_location"] = arrival_location
            # flight["duration"]
            flight["carrier"] = flight["operatedBy"]
            flight["stops"] = len(trip_stops)
            flight["stops_duration"] = str(trip_stops_duration)
            flight["stops_detail"] = trip_stops
            flight["discounts"] = []

        return {"date": date, "result": sorted(
            filter(lambda x: x["faresLeft"] != 0, search_data),
            key=lambda i: i["price"]
        )}

    # Autocomplete
    @staticmethod
    def autocomplete(search_word: str):
        resp_autocomplete = requests.get(Ryanair.BASE_URL + Ryanair.AUTOCOMPLETE_PATH.format(search_word),
                                         headers=HEADER_DEFAULT.copy())
        if resp_autocomplete.status_code != 200:
            raise Exception("invalid response: %s" % resp_autocomplete)

        return resp_autocomplete.json()

    @staticmethod
    def print_autocomplete(suggestion, deep=1):
        print("  " * (deep - 1), "\u2022 🌆", "Name:", suggestion["name"], "-", "IATA:", suggestion["code"])
        print("  " * deep, "City:", suggestion["city"]["name"], "-", suggestion["city"]["code"],
              "(%s)" % suggestion["city"].get("macCode", "N/D"))
        print("  " * deep, "Country:", suggestion["country"]["name"], "-", suggestion["country"]["code"])
        print("  " * deep, "Location Names:", ", ".join(suggestion["aliases"]))

