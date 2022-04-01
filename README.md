# FlyScanner
Find the best rate for your next flight consulting different providers!

> **Note:** I'm not responsible for the use of this program, this is only for personal and educational purpose. Before any usage please read provider's Terms of Service.  


## Current providers:
- eDreams ([T&C](https://www.edreams.com/terms-and-conditions/))
- Ryanair ([T&U](https://www.ryanair.com/hr/en/corporate/terms-of-use))


## Usage
- Autocomplete (find the IATA of the location)
```bash
~$ python3 flyscanner.py --autocomplete Rome

    ________      _____                                 
   / ____/ /_  __/ ___/_________ _____  ____  ___  _____
  / /_  / / / / /\__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / __/ / / /_/ /___/ / /__/ /_/ / / / / / / /  __/ /    
/_/   /_/\__, //____/\___/\__,_/_/ /_/_/ /_/\___/_/     
        /____/                                          

 • CITY 🌆
   Name: Rome
   Geo: 9795 (CITY) - IATA: ROM
   City: Rome
   Country: Italy (IT)
   Location Names: Rome, Roma
   Related Locations:
   • AIRPORT ✈️
     Name: Fiumicino
     Geo: 607 (AIRPORT) - IATA: FCO
     City: Rome
     Country: Italy (IT)
     Location Names: Fiumicino
   • AIRPORT ✈️
     Name: Ciampino
     Geo: 365 (AIRPORT) - IATA: CIA
     City: Rome
     Country: Italy (IT)
     Location Names: Ciampino

  ...
```

- Seach (default provider, no stop date)
```bash
~$ python3 flyscanner.py --search --departure ROM --destination LON --date 2022-04-01

    ________      _____                                 
   / ____/ /_  __/ ___/_________ _____  ____  ___  _____
  / /_  / / / / /\__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / __/ / / /_/ /___/ / /__/ /_/ / / / / / / /  __/ /    
/_/   /_/\__, //____/\___/\__,_/_/ /_/_/ /_/\___/_/     
        /____/                                          

Provider: eDreams
Searching for 2022-04-01 ...
  • ✈️  FOUND: 75.08 EUR - Vueling - 🕓 2:50:00 ✈️
  Departure: 2022-04-01T21:20:00+02:00
  From: Fiumicino - Rome - Italy - AIRPORT - FCO
  Arrival: 2022-04-01T23:10:00+01:00
  To: Gatwick - London - United Kingdom - AIRPORT - LGW
  Available Discounts:
   Discount: 53.99 EUR MEMBER_PRICE_POLICY_DISCOUNTED

...

# Use Ctrl-C to stop the search
```

- Seach (with stop date)
```bash
~$ python3 flyscanner.py --search --departure ROM --destination LON --date 2022-04-01 --to-date 2022-04-02      

    ________      _____                                 
   / ____/ /_  __/ ___/_________ _____  ____  ___  _____
  / /_  / / / / /\__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / __/ / / /_/ /___/ / /__/ /_/ / / / / / / /  __/ /    
/_/   /_/\__, //____/\___/\__,_/_/ /_/_/ /_/\___/_/     
        /____/                                          

Provider: eDreams
Searching for 2022-04-01 ...
  • ✈️  FOUND: 75.08 EUR - Vueling - 🕓 2:50:00 ✈️ 
  Departure: 2022-04-01T21:20:00+02:00
  From: Fiumicino - Rome - Italy - AIRPORT - FCO
  Arrival: 2022-04-01T23:10:00+01:00
  To: Gatwick - London - United Kingdom - AIRPORT - LGW
  Available Discounts:
   Discount: 53.99 EUR MEMBER_PRICE_POLICY_DISCOUNTED

Searching for 2022-04-02 ...
  • ✈️  FOUND: 40.77 EUR - Ryanair - 🕓 2:35:00 ✈️ 
  Departure: 2022-04-02T06:50:00+02:00
  From: Ciampino - Rome - Italy - AIRPORT - CIA
  Arrival: 2022-04-02T08:25:00+01:00
  To: Stansted - London - United Kingdom - AIRPORT - STN
  Available Discounts:
   Discount: 25.99 EUR MEMBER_PRICE_POLICY_DISCOUNTED

Bye!
```

## Other options
- `--passengers`
- `--all`: Show all fly options for the day, not only the cheepest
- `--list`: Reduce verbosity to only first line
- `--save`: Save the search output on a Excel spreadsheet

## Save option
- `--save` will save to `~/Desktop/FlyScannerTrips.xlsx`
- or you can specify the path: `--save /path/to/file.xlsx`
