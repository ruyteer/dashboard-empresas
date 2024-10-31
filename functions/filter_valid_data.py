def filter_valid_data(df_cleaned):
    servicos_invalidos = df_cleaned[(df_cleaned['Status'] != 'Resolvido') & (df_cleaned['Status'] != 'Aguardando Solicitante')]

       
    servicos_validos = df_cleaned[
    (df_cleaned['Status'] == 'Resolvido') | 
    (df_cleaned['Status'] == 'Aguardando Solicitante')]

    return servicos_invalidos, servicos_validos