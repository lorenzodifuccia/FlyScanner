import datetime
import requests

from providers import HEADER_DEFAULT


class eDreams:
    NAME = "eDreams"

    # Static
    BASE_URL = "https://www.edreams.com"

    VISITOR_PATH = "/travel/service/frontendapi/getVisitInformation"

    GRAPHQL_PATH = "/frontend-api/service/graphql"
    GRAPHQL_BODY = {
        "query": "query searchQuery($searchRequest: SearchRequest!) {\n  search(searchRequest: $searchRequest) {\n"
                 "    searchId\n    searchCode {\n      code\n      message\n    }\n    defaultFeeType {\n      name\n"
                 "      id\n    }\n    itineraries {\n      ...ItineraryBackendFragment\n    }\n    externalSelection {"
                 "\n      id\n      segmentKeys\n    }\n    trackingInfo {\n      returningUserDeviceId\n    }\n  }\n}"
                 "\n\nfragment ItineraryBackendFragment on Itinerary {\n  id\n  isFareUpgradeAvailable\n  key\n  "
                 "hotelXSellingEnabled\n  campaignConfig {\n    primeDayConfig {\n      isPrimeDayFare\n      "
                 "primeDayFareType\n    }\n    airlineCampaignConfig {\n      hasAirlineCampaign\n    }\n  }\n  "
                 "carbonFootprint {\n    isEco\n    ecoPercentageThanAverage\n    totalCo2Kilos\n    totalCo2eKilos\n  "
                 "}\n  meRating\n  fees {\n    price {\n      amount\n      currency\n    }\n    type {\n      "
                 "...FeeTypeInfo\n    }\n  }\n  ticketsLeft\n  legs {\n    segmentKeys\n    segments {\n      "
                 "...SegmentInfo\n    }\n  }\n  transportTypes\n  perks {\n    primeDiscount {\n      amount\n      "
                 "currency\n    }\n    extraPrimeCoupon {\n      amount\n      currency\n    }\n    "
                 "primeDiscountPerPassenger {\n      amount\n      currency\n    }\n    extraPrimeCouponPerPassenger {"
                 "\n      amount\n      currency\n    }\n  }\n}\n\nfragment SegmentInfo on Segment {\n  id\n  carrier {"
                 "\n    id\n    name\n  }\n  sections {\n    ...SectionInfo\n  }\n  baggageCondition\n  transportTypes"
                 "\n}\n\nfragment SectionInfo on Section {\n  id\n  departureDate\n  arrivalDate\n  departure {\n    "
                 "...SectionLocation\n  }\n  destination {\n    ...SectionLocation\n  }\n  carrier {\n    "
                 "...CarrierInfo\n  }\n  operatingCarrier {\n    ...CarrierInfo\n  }\n  technicalStops {\n    "
                 "...TechnicalStopInfo\n  }\n  cabinClass\n  flightCode\n  departureTerminal\n  arrivalTerminal\n  "
                 "vehicleModel\n  transportType\n  insuranceOffer {\n    url\n    id\n    policy\n  }\n}\n\n"
                 "fragment SectionLocation on Location {\n  id\n  iata\n  cityIata\n  cityName\n  name\n  countryName\n"
                 "  locationType\n}\n\nfragment CarrierInfo on Carrier {\n  id\n  name\n}\n\n"
                 "fragment TechnicalStopInfo on TechnicalStop {\n  location {\n    id\n    iata\n    cityName\n    "
                 "name\n    countryName\n  }\n  arrivalDate\n  departureDate\n}\n\n"
                 "fragment FeeTypeInfo on FeeType {\n  id\n  name\n  paymentMethod\n}\n"}

    FLEXIBLE_PATH = "/travel/service/flow/flexibledates/prices"

    AUTOCOMPLETE_PATH = "/frontend-home/service/geo/autocomplete;searchWord={};departureOrArrival=ARRIVAL;" \
                        "addSearchByCountry=true;addSearchByRegion=true;nearestLocations=true;product=FLIGHT"

    # Graphic
    IMG_URL = "https://www.edreams.it/images/onefront/bluestone/ED/OpenGraph.png"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = HEADER_DEFAULT.copy()

        # Debug
        # self.session.proxies = {"http": "http://127.0.0.1:8080", "https": "https://127.0.0.1:8080"}
        # self.session.verify = False

        self.__init_cookies()

    def __init_cookies(self):
        self.session.cookies.clear()

        resp_home = self.session.get(self.BASE_URL)
        if resp_home.status_code != 200:
            raise Exception("invalid response: %s" % resp_home)

        self.session.headers["Referer"] = self.BASE_URL
        resp_visitor = self.session.get(self.BASE_URL + self.VISITOR_PATH)
        if resp_visitor.status_code != 200:
            raise Exception("invalid response: %s" % resp_visitor)

    # Locations
    def prepare_location(self, location: dict):
        if "iata" not in location or not location["iata"]:
            return False

        if "geoNodeId" not in location or not location["geoNodeId"]:
            for autocomplete in self.autocomplete(location["iata"]):
                if autocomplete["iata"] == location["iata"]:
                    return autocomplete

            return False

        return location

    @staticmethod
    def parse_location(location):
        return " - ".join(location[x] for x in ["name", "cityName", "countryName", "locationType", "iata"]
                          if x in location)

    # Search
    # noinspection PyTypeChecker
    def search(self, num_adults: int, date: str, departure: dict, destination: dict):
        graphql_body = self.GRAPHQL_BODY.copy()
        graphql_body["variables"] = {
            "searchRequest": {
                "buyPath": 71, "tripType": "ONE_WAY",
                "itinerary": {
                    "numAdults": num_adults, "numChildren": 0, "numInfants": 0,
                    "cabinClass": "TOURIST", "resident": False, "mainAirportsOnly": False, "externalSelection": None,
                    "segments": [{
                        "date": date, "departure": {"iata": departure["iata"], "geoNodeId": departure["geoNodeId"]},
                        "destination": {"iata": destination["iata"], "geoNodeId": destination["geoNodeId"]}
                    }]
                }
            }
        }

        self.session.headers["X-Visit"] = self.session.cookies["viI"]
        self.session.headers["X-Of1jsessionid"] = self.session.cookies["OF1JSESSIONID"]
        self.session.headers["Referer"] = self.BASE_URL + "/travel/"
        resp_search = self.session.post(self.BASE_URL + self.GRAPHQL_PATH, json=graphql_body)
        if resp_search.status_code != 200:
            raise Exception("invalid response: %s" % resp_search)

        search_data = resp_search.json()["data"]["search"]["itineraries"]

        if not len(search_data):
            return {"date": date, "result": []}

        for itinerary in search_data:
            price = None
            price_currency = None
            discounts = []

            for fee in itinerary["fees"]:
                if fee["type"]["id"] == "MEMBER_PRICE_POLICY_UNDISCOUNTED":
                    price = fee["price"]["amount"]
                    price_currency = fee["price"]["currency"]

                else:
                    discounts.append({"price": fee["price"]["amount"],
                                      "price_currency": fee["price"]["currency"],
                                      "reason": fee["type"]["id"]})

            trip_departure = None
            trip_arrival = None
            trip_departure_date = None
            trip_arrival_date = None
            trip_stops = []
            trip_stops_duration = datetime.timedelta()
            for sections in itinerary["legs"][0]["segments"][0]["sections"]:
                if not trip_departure:
                    trip_departure = self.parse_location(sections["departure"])

                section_departure_date = datetime.datetime.fromisoformat(
                    sections["departureDate"].replace('Z', '+00:00')
                )
                if not trip_departure_date:
                    trip_departure_date = section_departure_date

                if trip_arrival_date:
                    trip_stops_duration += section_departure_date - trip_arrival_date

                trip_arrival = self.parse_location(sections["destination"])
                trip_arrival_date = datetime.datetime.fromisoformat(sections["arrivalDate"].replace('Z', '+00:00'))
                trip_stops.append({
                    "departure_location": self.parse_location(sections["departure"]),
                    "arrival_location": self.parse_location(sections["destination"]),
                    "departure_date": sections["departureDate"],
                    "arrival_date": sections["arrivalDate"],
                    "duration": str(trip_arrival_date - section_departure_date)
                })

            itinerary["price"] = price
            itinerary["price_currency"] = price_currency
            itinerary["departure_date"] = trip_departure_date.isoformat()
            itinerary["arrival_date"] = trip_arrival_date.isoformat()
            itinerary["departure_location"] = trip_departure
            itinerary["arrival_location"] = trip_arrival
            itinerary["duration"] = str(trip_arrival_date - trip_departure_date)
            itinerary["carrier"] = itinerary["legs"][0]["segments"][0]["carrier"]["name"]
            itinerary["stops"] = len(trip_stops)
            itinerary["stops_duration"] = str(trip_stops_duration)
            itinerary["stops_detail"] = trip_stops
            itinerary["discounts"] = discounts

        return {"date": date, "result": sorted(search_data, key=lambda i: i["price"])}

    def flexible_date(self, destination_geo: int, origin_geo: int, departure_date: str):
        self.session.headers["Referer"] = self.BASE_URL
        resp_flexible = self.session.post(self.BASE_URL + self.FLEXIBLE_PATH,
                                          json={
                                              "destinationGeoNode": destination_geo, "originGeoNode": origin_geo,
                                              "departureDate": departure_date,
                                              "interfaceClient": "ONE_FRONT_SMARTPHONE",
                                              "tripType": "ONE_WAY", "site": "GB", "numberOfFutureDaysDep": "60"
                                          })

        if resp_flexible.status_code != 200:
            raise Exception("invalid response: %s" % resp_flexible)

        return resp_flexible.json()

    # Autocomplete
    @staticmethod
    def autocomplete(search_word: str):
        local_headers = HEADER_DEFAULT.copy()
        local_headers["Referer"] = eDreams.BASE_URL

        resp_autocomplete = requests.get(eDreams.BASE_URL + eDreams.AUTOCOMPLETE_PATH.format(search_word),
                                         headers=local_headers)
        if resp_autocomplete.status_code != 200:
            raise Exception("invalid response: %s" % resp_autocomplete)

        return resp_autocomplete.json()

    @staticmethod
    def print_autocomplete(suggestion, deep=1):
        icons = {
            "CITY": "🌆",
            "AIRPORT": "✈️",
            "COUNTRY": "🌎",
            "NEAREST": "📍",
            "IATA_CODE": "🌐",
        }

        print("  " * (deep - 1), "\u2022", suggestion["type"], icons[suggestion["type"]])
        print("  " * deep, "Name:", suggestion["name"])
        print("  " * deep, "Geo:", suggestion["geoNodeId"], "(%s)" % suggestion["geoNodeType"],
              "- IATA:", suggestion["iata"])
        print("  " * deep, "City:", suggestion["city"])
        print("  " * deep, "Country:", suggestion["country"], "(%s)" % suggestion["countryCode"])
        print("  " * deep, "Location Names:", ", ".join(suggestion["locationNames"]))

        if suggestion["relatedLocations"]:
            print("  " * deep, "Related Locations:")
            for related in suggestion["relatedLocations"]:
                eDreams.print_autocomplete(related, deep + 1)
