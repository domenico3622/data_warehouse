import pandas as pd

def crea_csv_filtrato(input_csv_path, output_csv_path):
    # Leggi il CSV originale
    df = pd.read_csv(input_csv_path)

    # Seleziona solo le colonne desiderate
    colonne_richieste = [
        'Borough', 
        'Neighborhoods', 
        'NYC_Poverty_Rate', 
        'Median_Income', 
        'Perc_White', 
        'Perc_Black'
    ]
    df_filtrato = df[colonne_richieste]

    # Estrai solo il primo nome dal campo "Neighborhoods" (prima della virgola), se è una stringa
    df_filtrato['Neighborhoods'] = df_filtrato['Neighborhoods'].apply(
        lambda x: x.split(',')[0].strip() if isinstance(x, str) else x
    )

    # Rimuovi righe duplicate basandoti sulla colonna 'Neighborhoods' mantenendo solo la prima occorrenza
    df_unico = df_filtrato.drop_duplicates(subset='Neighborhoods', keep='first')

    # Salva il nuovo CSV
    df_unico.to_csv(output_csv_path, index=False)

    print(f"CSV salvato in: {output_csv_path}")

crea_csv_filtrato("NeighborhoodFinancialHealthIndicators-2018_2021-Dataset.csv", "NeighborhoodIndex.csv")
