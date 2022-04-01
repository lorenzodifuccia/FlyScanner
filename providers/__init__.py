# Defaults
HEADER_DEFAULT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.82 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://www.google.com/"
}

FLIGHT_DEFAULT = [
    "price",
    "price_currency",
    "departure_date",
    "arrival_date",
    "departure_location",
    "arrival_location",
    "duration",
    "carrier",
    "stops",
    "stops_duration",
    "stops_detail",
    "discounts"
]


# Import classes for __all__
from .eDreams import eDreams
from .ryanair import Ryanair

PROVIDERS = {
    eDreams.NAME: eDreams,
    Ryanair.NAME: Ryanair
}

__all__ = ["PROVIDERS", "HEADER_DEFAULT"]
