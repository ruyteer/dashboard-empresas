import pandas as pd

def rename_columns(file_path):
    df = pd.read_excel(file_path, sheet_name='Sheet1')
        
    df_cleaned = df.rename(columns={
            'Empresas BB': 'Número de Referência',
            'Unnamed: 1': 'Data de Criação',
            'Unnamed: 2': 'Estado',
            'Unnamed: 3': 'Nome Completo',
            'Unnamed: 4': 'Bloco',
            'Unnamed: 5': 'Região',
            'Unnamed: 6': 'Cenáculo',
            'Unnamed: 7': 'Tipo de Serviço',
            'Unnamed: 8': 'Status',
            'Unnamed: 9': 'Ação',
            'Unnamed: 10': 'Empresa',
            'Unnamed: 11': 'CNPJ',
            'Unnamed: 12': 'Valor',
            'Unnamed: 13': 'Avaliação do Serviço',
            'Unnamed: 14': 'Data'
        }).drop(index=0)

    return df_cleaned 
