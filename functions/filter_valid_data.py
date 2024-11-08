def filter_valid_data(df_cleaned):
    servicos_invalidos = df_cleaned[(df_cleaned['Status'] == 'Reprovado')]

       
    servicos_validos = df_cleaned[
    (df_cleaned['Status'] != 'Reprovado')
   ]

    return servicos_invalidos, servicos_validos