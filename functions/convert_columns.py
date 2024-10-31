# Converter colunas para os formatos corretos
import pandas as pd

def convert_columns(df_cleaned): 
    df_cleaned['Data Original'] = df_cleaned['Data'] 
    df_cleaned['Data'] = pd.to_datetime(df_cleaned['Data'], errors='coerce')  
    df_cleaned['Valor'] = df_cleaned['Valor'].str.replace('.', '', regex=False)  
    df_cleaned['Valor'] = df_cleaned['Valor'].str.replace(',', '.', regex=False)  
    df_cleaned['Valor'] = pd.to_numeric(df_cleaned['Valor'], errors='coerce')

    return df_cleaned