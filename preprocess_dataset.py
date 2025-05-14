import csv
import re
from datetime import datetime

# Mappatura dei codici dei borough ai nomi corrispondenti
BOROUGH_MAP = {
    "1": "Manhattan",
    "2": "Bronx",
    "3": "Brooklyn",
    "4": "Queens",
    "5": "Staten Island"
}

# Mappa per il codice completo della Building Class Category
BUILDING_CATEGORY_MAP = {
    "A": "ONE FAMILY DWELLINGS",
    "A0": "CAPE COD",
    "A1": "TWO STORIES - DETACHED SM OR MID",
    "A2": "ONE STORY - PERMANENT LIVING QUARTER",
    "A3": "LARGE SUBURBAN RESIDENCE",
    "A4": "CITY RESIDENCE ONE FAMILY",
    "A5": "ONE FAMILY ATTACHED OR SEMI-DETACHED",
    "A6": "SUMMER COTTAGE",
    "A7": "MANSION TYPE OR TOWN HOUSE",
    "A8": "BUNGALOW COLONY - COOPERATIVELY OWNED LAND",
    "A9": "MISCELLANEOUS ONE FAMILY",
    "B": "TWO FAMILY DWELLINGS",
    "B1": "TWO FAMILY BRICK",
    "B2": "TWO FAMILY FRAME",
    "B3": "TWO FAMILY CONVERTED FROM ONE FAMILY",
    "B9": "MISCELLANEOUS TWO FAMILY",
    "C": "WALK UP APARTMENTS",
    "C0": "THREE FAMILIES",
    "C1": "OVER SIX FAMILIES WITHOUT STORES",
    "C2": "FIVE TO SIX FAMILIES",
    "C3": "FOUR FAMILIES",
    "C4": "OLD LAW TENEMENT",
    "C5": "CONVERTED DWELLINGS OR ROOMING HOUSE",
    "C6": "WALK-UP COOPERATIVE",
    "C7": "WALK-UP APT. OVER SIX FAMILIES WITH STORES",
    "C8": "WALK-UP CO-OP; CONVERSION FROM LOFT/WAREHOUSE",
    "C9": "GARDEN APARTMENTS",
    "CB": "WALKUP APT LESS THAN 11 UNITS RESIDENTIAL",
    "CC": "WALKUP CO-OP APT LESS THAN 11 UNITS RESIDENTIAL",
    "CM": "MOBILE HOMES/TRAILER PARKS",
    "D": "ELEVATOR APARTMENTS",
    "D0": "ELEVATOR CO-OP; CONVERSION FROM LOFT/WAREHOUSE",
    "D1": "ELEVATOR APT; SEMI-FIREPROOF WITHOUT STORES",
    "D2": "ELEVATOR APT; ARTISTS IN RESIDENCE",
    "D3": "ELEVATOR APT; FIREPROOF WITHOUT STORES",
    "D4": "ELEVATOR COOPERATIVE",
    "D5": "ELEVATOR APT; CONVERTED",
    "D6": "ELEVATOR APT; FIREPROOF WITH STORES",
    "D7": "ELEVATOR APT; SEMI-FIREPROOF WITH STORES",
    "D8": "ELEVATOR APT; LUXURY TYPE",
    "D9": "ELEVATOR APT; MISCELLANEOUS",
    "DB": "ELEVATOR APT LESS THAN 11 UNITS RESIDENTIAL",
    "DC": "ELEVATOR CO-OP APT LESS THAN 11 UNITS RESIDENTIAL",
    "E": "WAREHOUSES",
    "E1": "GENERAL WAREHOUSE",
    "E2": "CONTRACTORS WAREHOUSE",
    "E7": "SELF-STORAGE WAREHOUSES",
    "E9": "MISCELLANEOUS WAREHOUSE",
    "F": "FACTORIES AND INDUSTRIAL BUILDINGS",
    "F1": "FACTORY; HEAVY MANUFACTURING - FIREPROOF",
    "F2": "FACTORY; SPECIAL CONSTRUCTION - FIREPROOF",
    "F4": "FACTORY; INDUSTRIAL SEMI-FIREPROOF",
    "F5": "FACTORY; LIGHT MANUFACTURING",
    "F8": "FACTORY; TANK FARM",
    "F9": "FACTORY; INDUSTRIAL-MISCELLANEOUS",
    "G": "GARAGES",
    "G0": "GARAGE; RESIDENTIAL TAX CLASS 1",
    "G1": "ALL PARKING GARAGES",
    "G2": "AUTO BODY/COLLISION OR AUTO REPAIR",
    "G3": "GAS STATION WITH RETAIL STORE",
    "G4": "GAS STATION WITH SERVICE/AUTO REPAIR",
    "G5": "GAS STATION ONLY WITH/WITHOUT SMALL KIOSK",
    "G6": "LICENSED PARKING LOT",
    "G7": "UNLICENSED PARKING LOT",
    "G8": "CAR SALES/RENTAL WITH SHOWROOM",
    "G9": "MISCELLANEOUS GARAGE",
    "GU": "CAR SALES OR RENTAL LOTS WITHOUT SHOWROOM",
    "GW": "CAR WASH OR LUBRITORIUM FACILITY",
    "H": "HOTELS",
    "HB": "BOUTIQUE: 10-100 ROOMS, W/LUXURY FACILITIES, THEMED, STYLISH, W/FULL SVC ACCOMMODATIONS",
    "HH": "HOSTELS- BED RENTALS IN DORMITORY-LIKE SETTINGS W/SHARED ROOMS & BATHROOMS",
    "HR": "SRO- 1 OR 2 PEOPLE HOUSED IN INDIVIDUAL ROOMS IN MULTIPLE DWELLING AFFORDABLE HOUSING",
    "HS": "EXTENDED STAY/SUITE: AMENITIES SIMILAR TO APT; TYPICALLY CHARGE WEEKLY RATES & LESS EXPENSIVE THAN FULL-SERVICE HOTEL",
    "H1": "LUXURY HOTEL",
    "H2": "FULL SERVICE HOTEL",
    "H3": "LIMITED SERVICE; MANY AFFILIATED WITH NATIONAL CHAIN",
    "H4": "MOTEL",
    "H5": "HOTEL; PRIVATE CLUB, LUXURY TYPE",
    "H6": "APARTMENT HOTEL",
    "H7": "APARTMENT HOTEL - COOPERATIVELY OWNED",
    "H8": "DORMITORY",
    "H9": "MISCELLANEOUS HOTEL",
    "I": "HOSPITALS AND HEALTH FACILITIES",
    "I1": "HOSPITAL, SANITARIUM, MENTAL INSTITUTION",
    "I2": "INFIRMARY",
    "I3": "DISPENSARY",
    "I4": "HOSPITAL; STAFF FACILITY",
    "I5": "HEALTH CENTER, CHILD CENTER, CLINIC",
    "I6": "NURSING HOME",
    "I7": "ADULT CARE FACILITY",
    "I9": "MISCELLANEOUS HOSPITAL, HEALTH CARE FACILITY",
    "J": "THEATRES",
    "J1": "THEATRE; ART TYPE LESS THAN 400 SEATS",
    "J2": "THEATRE; ART TYPE MORE THAN 400 SEATS",
    "J3": "MOTION PICTURE THEATRE WITH BALCONY",
    "J4": "LEGITIMATE THEATRE, SOLE USE",
    "J5": "THEATRE IN MIXED-USE BUILDING",
    "J6": "TELEVISION STUDIO",
    "J7": "OFF BROADWAY TYPE THEATRE",
    "J8": "MULTIPLEX PICTURE THEATRE",
    "J9": "MISCELLANEOUS THEATRE",
    "K": "STORE BUILDINGS",
    "K1": "ONE STORY RETAIL BUILDING",
    "K2": "MULTI-STORY RETAIL BUILDING (2 OR MORE)",
    "K3": "MULTI-STORY DEPARTMENT STORE",
    "K4": "PREDOMINANT RETAIL WITH OTHER USES",
    "K5": "STAND-ALONE FOOD ESTABLISHMENT",
    "K6": "SHOPPING CENTER WITH OR WITHOUT PARKING",
    "K7": "BANKING FACILITIES WITH OR WITHOUT PARKING",
    "K8": "BIG BOX RETAIL: NOT AFFIXED & STANDING ON OWN LOT W/PARKING, E.G. COSTCO & BJ'S",
    "K9": "MISCELLANEOUS STORE BUILDING",
    "L": "LOFTS",
    "L1": "LOFT; OVER 8 STORIES (MID MANH. TYPE)",
    "L2": "LOFT; FIREPROOF AND STORAGE TYPE WITHOUT STORES",
    "L3": "LOFT; SEMI-FIREPROOF",
    "L8": "LOFT; WITH RETAIL STORES OTHER THAN TYPE ONE",
    "L9": "MISCELLANEOUS LOFT",
    "M": "RELIGIOUS FACILITIES",
    "M1": "CHURCH, SYNAGOGUE, CHAPEL",
    "M2": "MISSION HOUSE (NON-RESIDENTIAL)",
    "M3": "PARSONAGE, RECTORY",
    "M4": "CONVENT",
    "M9": "MISCELLANEOUS RELIGIOUS FACILITY",
    "N": "ASYLUMS AND HOMES",
    "N1": "ASYLUM",
    "N2": "HOME FOR INDIGENT CHILDREN, AGED, HOMELESS",
    "N3": "ORPHANAGE",
    "N4": "DETENTION HOUSE FOR WAYWARD GIRLS",
    "N9": "MISCELLANEOUS ASYLUM, HOME",
    "O": "OFFICE BUILDINGS",
    "O1": "OFFICE ONLY - 1 STORY",
    "O2": "OFFICE ONLY 2 - 6 STORIES",
    "O3": "OFFICE ONLY 7 - 19 STORIES",
    "O4": "OFFICE ONLY WITH OR WITHOUT COMM - 20 STORIES OR MORE",
    "O5": "OFFICE WITH COMM - 1 TO 6 STORIES",
    "O6": "OFFICE WITH COMM 7 - 19 STORIES",
    "O7": "PROFESSIONAL BUILDINGS/STAND ALONE FUNERAL HOMES",
    "O8": "OFFICE WITH APARTMENTS ONLY (NO COMM)",
    "O9": "MISCELLANEOUS AND OLD STYLE BANK BLDGS.",
    "P": "INDOOR PUBLIC ASSEMBLY & CULT. FACILITIES",
    "P1": "CONCERT HALL",
    "P2": "LODGE ROOM",
    "P3": "YWCA, YMCA, YWHA, YMHA, PAL",
    "P4": "BEACH CLUB",
    "P5": "COMMUNITY CENTER",
    "P6": "AMUSEMENT PLACE, BATH HOUSE, BOAT HOUSE",
    "P7": "MUSEUM",
    "P8": "LIBRARY",
    "P9": "MISCELLANEOUS INDOOR PUBLIC ASSEMBLY",
    "Q": "OUTDOOR RECREATIONAL FACILITIES",
    "Q1": "PARKS/RECREATION FACILTY",
    "Q2": "PLAYGROUND",
    "Q3": "OUTDOOR POOL",
    "Q4": "BEACH",
    "Q5": "GOLF COURSE",
    "Q6": "STADIUM, RACE TRACK, BASEBALL FIELD",
    "Q7": "TENNIS COURT",
    "Q8": "MARINA, YACHT CLUB",
    "Q9": "MISCELLANEOUS OUTDOOR RECREATIONAL FACILITY",
    "R": "CONDOMINIUMS",
    "RA": "CULTURAL, MEDICAL, EDUCATIONAL, ETC.",
    "RB": "OFFICE SPACE",
    "RG": "INDOOR PARKING",
    "RH": "HOTEL/BOATEL",
    "RK": "RETAIL SPACE",
    "RP": "OUTDOOR PARKING",
    "RR": "CONDOMINIUM RENTALS",
    "RS": "NON-BUSINESS STORAGE SPACE",
    "RT": "TERRACES/GARDENS/CABANAS",
    "RW": "WAREHOUSE/FACTORY/INDUSTRIAL",
    "R0": "SPECIAL CONDOMINIUM BILLING LOT",
    "R1": "CONDO; RESIDENTIAL UNIT IN 2-10 UNIT BLDG.",
    "R2": "CONDO; RESIDENTIAL UNIT IN WALK-UP BLDG.",
    "R3": "CONDO; RESIDENTIAL UNIT IN 1-3 STORY BLDG.",
    "R4": "CONDO; RESIDENTIAL UNIT IN ELEVATOR BLDG.",
    "R5": "MISCELLANEOUS COMMERCIAL",
    "R6": "CONDO; RESID.UNIT OF 1-3 UNIT BLDG-ORIG CLASS 1",
    "R7": "CONDO; COMML.UNIT OF 1-3 UNIT BLDG-ORIG CLASS 1",
    "R8": "CONDO; COMML.UNIT OF 2-10 UNIT BLDG.",
    "R9": "CO-OP WITHIN A CONDOMINIUM",
    "S": "PRIMARILY RES. - MIXED USE",
    "S0": "PRIMARILY 1 FAMILY WITH 2 STORES OR OFFICES",
    "S1": "PRIMARILY 1 FAMILY WITH 1 STORE OR OFFICE",
    "S2": "PRIMARILY 2 FAMILY WITH 1 STORE OR OFFICE",
    "S3": "PRIMARILY 3 FAMILY WITH 1 STORE OR OFFICE",
    "S4": "PRIMARILY 4 FAMILY WITH 1 STORE OROFFICE",
    "S5": "PRIMARILY 5-6 FAMILY WITH 1 STORE OR OFFICE",
    "S9": "SINGLE OR MULTIPLE DWELLING WITH STORES OR OFFICES",
    "T": "TRANSPORTATION FACILITIES",
    "T1": "AIRPORT, AIRFIELD, TERMINAL",
    "T2": "PIER, DOCK, BULKHEAD",
    "T9": "MISCELLANEOUS TRANSPORTATION FACILITY",
    "U": "UTILITY BUREAU PROPERTIES",
    "U0": "UTILITY COMPANY LAND AND BUILDING",
    "U1": "BRIDGE, TUNNEL, HIGHWAY",
    "U2": "GAS OR ELECTRIC UTILITY",
    "U3": "CEILING RAILROAD",
    "U4": "TELEPHONE UTILITY",
    "U5": "COMMUNICATION FACILITY OTHER THAN TELEPHONE",
    "U6": "RAILROAD - PRIVATE OWNERSHIP",
    "U7": "TRANSPORTATION - PUBLIC OWNERSHIP",
    "U8": "REVOCABLE CONSENT",
    "U9": "MISCELLANEOUS UTILITY PROPERTY",
    "V": "VACANT LAND",
    "V0": "ZONED RESIDENTIAL; NOT MANHATTAN",
    "V1": "ZONED COMMERCIAL OR MANHATTAN RESIDENTIAL",
    "V2": "ZONED COMMERCIAL ADJACENT TO CLASS 1 DWELLING: NOT MANHATTAN",
    "V3": "ZONED PRIMARILY RESIDENTIAL; NOT MANHATTAN",
    "V4": "POLICE OR FIRE DEPARTMENT",
    "V5": "SCHOOL SITE OR YARD",
    "V6": "LIBRARY, HOSPITAL OR MUSEUM",
    "V7": "PORT AUTHORITY OF NEW YORK AND NEW JERSEY",
    "V8": "NEW YORK STATE OR US GOVERNMENT",
    "V9": "MISCELLANEOUS VACANT LAND",
    "W": "EDUCATIONAL FACILITIES",
    "W1": "PUBLIC ELEMENTARY, JUNIOR OR SENIOR HIGH",
    "W2": "PAROCHIAL SCHOOL, YESHIVA",
    "W3": "SCHOOL OR ACADEMY",
    "W4": "TRAINING SCHOOL",
    "W5": "CITY UNIVERSITY",
    "W6": "OTHER COLLEGE AND UNIVERSITY",
    "W7": "THEOLOGICAL SEMINARY",
    "W8": "OTHER PRIVATE SCHOOL",
    "W9": "MISCELLANEOUS EDUCATIONAL FACILITY",
    "Y": "GOVERNMENT/CITY DEPARTMENTS",
    "Y1": "FIRE DEPARTMENT",
    "Y2": "POLICE DEPARTMENT",
    "Y3": "PRISON, JAIL, HOUSE OF DETENTION",
    "Y4": "MILITARY AND NAVAL INSTALLATION",
    "Y5": "DEPARTMENT OF REAL ESTATE",
    "Y6": "DEPARTMENT OF SANITATION",
    "Y7": "DEPARTMENT OF PORTS AND TERMINALS",
    "Y8": "DEPARTMENT OF PUBLIC WORKS",
    "Y9": "DEPARTMENT OF ENVIRONMENTAL PROTECTION",
    "Z": "MISC. BUILDING CLASSIFICATIONS",
    "Z0": "TENNIS COURT, POOL, SHED, ETC.",
    "Z1": "COURT HOUSE",
    "Z2": "PUBLIC PARKING AREA",
    "Z3": "POST OFFICE",
    "Z4": "FOREIGN GOVERNMENT",
    "Z5": "UNITED NATIONS",
    "Z7": "EASEMENT",
    "Z8": "CEMETERY",
    "Z9": "OTHER MISCELLANEOUS"
}

# Mappa per la macrocategoria (basata solo sulla prima lettera del codice)
MACRO_BUILDING_CATEGORY_MAP = {
    "A": "ONE FAMILY DWELLINGS",
    "B": "TWO FAMILY DWELLINGS",
    "C": "APARTMENT BUILDINGS (WALK UP/CONVERTED)",
    "D": "ELEVATOR APARTMENTS",
    "E": "WAREHOUSES",
    "F": "FACTORIES AND INDUSTRIAL BUILDINGS",
    "G": "GARAGES",
    "H": "HOTELS",
    "I": "HOSPITALS AND HEALTH FACILITIES",
    "J": "THEATRES",
    "K": "STORE BUILDINGS",
    "L": "LOFTS",
    "M": "RELIGIOUS FACILITIES",
    "N": "ASYLUMS AND HOMES",
    "O": "OFFICE BUILDINGS",
    "P": "INDOOR PUBLIC ASSEMBLY & CULTURAL FACILITIES",
    "Q": "OUTDOOR RECREATIONAL FACILITIES",
    "R": "CONDOMINIUMS",
    "S": "PRIMARILY RESIDENTIAL - MIXED USE",
    "T": "TRANSPORTATION FACILITIES",
    "U": "UTILITY BUREAU PROPERTIES",
    "V": "VACANT LAND",
    "W": "EDUCATIONAL FACILITIES",
    "Y": "GOVERNMENT/CITY DEPARTMENTS",
    "Z": "MISC. BUILDING CLASSIFICATIONS"
}

def clean_value(value: str) -> str:
    """Rimuove gli spazi iniziali e finali da un valore."""
    return value.strip()

def clean_date(date_str: str) -> str:
    """
    Converte la data da 'YYYY-MM-DD HH:MM:SS' a 'DD/MM/YYYY'.
    Se la conversione fallisce, restituisce la stringa originale.
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def clean_address(address: str) -> str:
    """
    Rimuove gli spazi multipli all'interno di un indirizzo,
    lasciando un solo spazio tra le parole.
    """
    return re.sub(r'\s+', ' ', address).strip()

def is_valid_price(price: str) -> bool:
    """
    Controlla se la colonna 'SALE PRICE' contiene un valore numerico valido
    e se è maggiore o uguale a 5.000.
    """
    price = clean_value(price)
    if not price.isdigit():
        return False
    return int(price) >= 5000

def is_valid_total_units(units: str) -> bool:
    """
    Verifica se il valore della colonna 'TOTAL UNITS' è diverso da zero.
    Se il valore è numerico, restituisce False se è zero, True altrimenti.
    Per valori non numerici restituisce True.
    """
    units = clean_value(units)
    if units.isdigit():
        return int(units) != 0
    return True

def is_valid_land_square_feet(value: str) -> bool:
    """
    Verifica se il valore della colonna 'LAND SQUARE FEET' è numerico, non vuoto,
    non contiene simboli come "-" ed è maggiore di 1.
    """
    value = clean_value(value)
    if value == "" or value == "-":
        return False
    # Rimuove eventuali virgole e controlla se è numerico
    value_numeric = value.replace(",", "")
    try:
        num = float(value_numeric)
        return num > 1
    except ValueError:
        return False

def map_borough(borough: str) -> str:
    """
    Converte il valore numerico della colonna 'BOROUGH' nel nome corrispondente.
    Se il valore non è un numero tra 1 e 5, lo lascia invariato.
    """
    borough = clean_value(borough)
    return BOROUGH_MAP.get(borough, borough)

def get_building_category_description(code: str) -> str:
    """
    Restituisce la descrizione corrispondente al codice completo della categoria dell'edificio.
    Se il codice non viene trovato, restituisce una stringa vuota.
    """
    code = clean_value(code)
    return BUILDING_CATEGORY_MAP.get(code, "")

def get_building_macro_category_description(code: str) -> str:
    """
    Restituisce la descrizione della macrocategoria basata sulla prima lettera del codice.
    Se il codice è vuoto o non viene trovato, restituisce una stringa vuota.
    """
    code = clean_value(code)
    if not code:
        return ""
    macro = code[0]
    return MACRO_BUILDING_CATEGORY_MAP.get(macro, "")

''' SENZA SCALA LOGARITMICA 
def get_land_square_category(value: str) -> str:
    """
    Converte un valore numerico di 'LAND SQUARE FEET' in una stringa di categoria,
    con intervalli di 1000 in 1000 fino a 22999 (es. '0-999', '1000-1999', ...).
    Valori oltre 22999 verranno categorizzati come '23000+'.
    """
    try:
        num = int(value.replace(",", ""))
        if num > 22999:
            return "23000+"
        lower_bound = (num // 1000) * 1000
        upper_bound = lower_bound + 999
        return f"{lower_bound}-{upper_bound}"
    except ValueError:
        return "Invalid"
'''

import math
def get_land_square_category(value: str) -> str:
    """
    Converte un valore numerico di 'LAND SQUARE FEET' in una categoria su scala logaritmica base 2.
    Esempi:
      1–1           → '1-1'
      2–3           → '2-3'
      4–7           → '4-7'
      8–15          → '8-15'
      ...
      >=2,147,483,648 → '2,147,483,648+'
    """
    try:
        num = int(value.replace(",", ""))
        if num < 1:
            return "0"
        elif num >= 2 ** 31:
            return f"{2 ** 31:,}+"
        else:
            lower_exp = int(math.floor(math.log(num, 2)))
            lower = 2 ** lower_exp
            upper = (2 ** (lower_exp + 1)) - 1
            return f"{lower:,}-{upper:,}"
    except ValueError:
        return "Invalid"


def remove_columns(row: dict, columns_to_remove: list) -> dict:
    """Elimina dal dizionario della riga le colonne specificate."""
    return {key: value for key, value in row.items() if key not in columns_to_remove}

def process_row(row: dict) -> dict:
    """
    Elabora un dizionario di riga:
      - Pulisce i valori rimuovendo spazi inutili
      - Converte 'SALE DATE' in formato 'YYYY-MM-DD'
      - Corregge gli spazi negli indirizzi
      - Converte i codici 'BOROUGH' nei nomi corrispondenti
      - Aggiunge la colonna 'BUILDING CATERY DESCRIPTION' basata sul codice completo
      - Aggiunge la colonna 'BUILDING MACRO CATEGORY DESCRIPTION' basata sulla prima lettera del codice
    """
    new_row = {}
    for key, value in row.items():
        cleaned = clean_value(value) if value is not None else ''
        if key.upper() == "SALE DATE" and cleaned:
            cleaned = clean_date(cleaned)
        elif key.upper() == "ADDRESS" and cleaned:
            cleaned = clean_address(cleaned)
        elif key.upper() == "BOROUGH" and cleaned:
            cleaned = map_borough(cleaned)
        new_row[key] = cleaned

    building_code = row.get("BUILDING CLASS AT TIME OF SALE", "")
    new_row["BUILDING CLASS CATEGORY"] = get_building_category_description(building_code)
    new_row["BUILDING MACRO CLASS CATEGORY"] = get_building_macro_category_description(building_code)
    land_value = row.get("LAND SQUARE FEET", "")
    new_row["LAND SQUARE CATEGORY"] = get_land_square_category(land_value)
    return new_row

def process_csv(input_file: str, output_file: str, columns_to_remove: list) -> None:
    """
    Legge il file CSV in input, pulisce i dati e:
      - Rimuove le righe con 'SALE PRICE' non valido o inferiore a 5.000.
      - Rimuove le righe con 'TOTAL UNITS' uguale a zero.
      - Rimuove le righe in cui 'LAND SQUARE FEET' non è un numero > 1 o contiene simboli come "-".
      - Elimina le colonne specificate.
      Infine, scrive il risultato in un nuovo file CSV.
    """
    with open(input_file, 'r', encoding='utf-8', newline='') as infile:
        reader = csv.DictReader(infile)
        # Prepara i fieldnames eliminando quelli da rimuovere e aggiungendo le nuove colonne se non già presenti
        fieldnames = [col for col in reader.fieldnames if col not in columns_to_remove]
        if "BUILDING CLASS CATEGORY" not in fieldnames:
            fieldnames.append("BUILDING CLASS CATEGORY")
        if "BUILDING MACRO CLASS CATEGORY" not in fieldnames:
            fieldnames.append("BUILDING MACRO CLASS CATEGORY")
        if "LAND SQUARE CATEGORY" not in fieldnames:
            fieldnames.append("LAND SQUARE CATEGORY")

        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Salta le righe con SALE PRICE non valido o inferiore a 5.000
                if not is_valid_price(row.get("SALE PRICE", "")):
                    continue
                # Salta le righe con TOTAL UNITS uguale a zero
                if not is_valid_total_units(row.get("TOTAL UNITS", "")):
                    continue
                # Salta le righe in cui LAND SQUARE FEET non è valido (numerico > 1, non vuoto e senza simboli come "-")
                if not is_valid_land_square_feet(row.get("LAND SQUARE FEET", "")):
                    continue

                cleaned_row = process_row(row)
                cleaned_row = remove_columns(cleaned_row, columns_to_remove)
                writer.writerow(cleaned_row)

def main():
    input_file = r"D:\PerDesktop\corsi\Magistrale\2anno-2sem\data warehouse\sales_nyc.csv"
    output_file = r"D:\PerDesktop\corsi\Magistrale\2anno-2sem\data warehouse\output.csv"

    # Aggiorna l'elenco delle colonne da rimuovere se non vuoi rimuovere 'BUILDING CLASS CATEGORY'
    columns_to_remove = ["TAX CLASS AT TIME OF SALE","BUILDING CLASS AT PRESENT", "TAX CLASS AT PRESENT", "EASE-MENT", "ID", "APARTMENT NUMBER", "GROSS SQUARE FEET"]
    process_csv(input_file, output_file, columns_to_remove)
    print(f"Elaborazione completata. Nuovo file salvato come '{output_file}'.")

if __name__ == '__main__':
    main()
