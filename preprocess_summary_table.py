import pandas as pd
from datetime import datetime

def analyze_real_estate_dataset(csv_path):
    df = pd.read_csv(csv_path, dtype=str)

    total_rows = len(df)
    results = {}

    # Convert columns to appropriate dtypes where possible
    cols_to_int = ['SALE PRICE', 'TOTAL UNITS', 'COMMERCIAL UNITS', 'RESIDENTIAL UNITS', 'LAND SQUARE FEET', 'YEAR BUILT']
    for col in cols_to_int:
        df[col] = pd.to_numeric(df[col].str.replace('-', '').str.strip(), errors='coerce')

    # === VALIDITY CHECKS ===
    valid_counts = {}

    # 1. SALE DATE validity
    def is_valid_date(val):
        try:
            d = datetime.strptime(val.strip(), "%Y-%m-%d %H:%M:%S")
            # Controlla che anno, mese e giorno siano in range accettabili
            if d.year > 2025 or d.month < 1 or d.month > 12 or d.day < 1 or d.day > 31:
                return False
            return True
        except:
            return False

    valid_counts['SALE DATE'] = df['SALE DATE'].apply(is_valid_date).sum()

    # 2. Numeric columns
    for col in ['SALE PRICE', 'LAND SQUARE FEET', 'YEAR BUILT']:
        if col == 'SALE PRICE':
            valid = df[col].notnull() & (df[col] > 5000)
        elif col == 'LAND SQUARE FEET':
            valid = df[col].notnull() & (df[col] >= 5)
        elif col == 'YEAR BUILT':
            valid = df[col].notnull() & (df[col] <= 2025) & (df[col] > 200)
        valid_counts[col] = valid.sum()

    # 3. TOTAL UNITS: not null and > 0
    tu = df['TOTAL UNITS']
    valid_tu = tu.notnull() & (tu > 0)
    valid_counts['TOTAL UNITS'] = valid_tu.sum()

    # 4. COMMERCIAL and RESIDENTIAL UNITS validity
    cu = df['COMMERCIAL UNITS']
    ru = df['RESIDENTIAL UNITS']

    valid_cu = cu.notnull() & ((cu > 0) | ((cu == 0) & (ru > 0)))
    valid_ru = ru.notnull() & ((ru > 0) | ((ru == 0) & (cu > 0)))

    valid_counts['COMMERCIAL UNITS'] = valid_cu.sum()
    valid_counts['RESIDENTIAL UNITS'] = valid_ru.sum()

    # Percentuale validità
    results['validity'] = {col: round((valid_counts[col] / total_rows) * 100, 2) for col in valid_counts}

    # === CONSISTENCY CHECK ===
    df['unit_sum'] = df['RESIDENTIAL UNITS'] + df['COMMERCIAL UNITS']
    consistent_units = (df['TOTAL UNITS'] == df['unit_sum']).sum()
    results['consistency'] = round((consistent_units / total_rows) * 100, 2)

    # === UNIQUENESS CHECK ===
    df['BOROUGH_BLOCK_LOT'] = df['BOROUGH'].astype(str) + '_' + df['BLOCK'].astype(str) + '_' + df['LOT'].astype(str)
    unique_combinations = df['BOROUGH_BLOCK_LOT'].nunique()
    results['uniqueness'] = round((unique_combinations / total_rows) * 100, 2)

    # Stampa dei risultati
    print("=== VALIDITY & COMPLETENESS (%) ===")
    for col, val in results['validity'].items():
        print(f"{col}: {val}%")

    print("\n=== CONSISTENCY ===")
    print(f"TOTAL UNITS = RESIDENTIAL + COMMERCIAL: {results['consistency']}%")

    print("\n=== UNIQUENESS ===")
    print(f"Unique (BOROUGH+BLOCK+LOT): {results['uniqueness']}%")

    return results

# Esempio di utilizzo:
file_path = r"D:\PerDesktop\corsi\Magistrale\2anno-2sem\data warehouse\progetto\sales_nyc.csv"  # Sostituisci con il percorso corretto del file CSV
results = analyze_real_estate_dataset(file_path)

