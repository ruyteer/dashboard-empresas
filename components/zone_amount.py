import plotly.express as px  

def zone_amount(servicos_validos, filtro_valor_maximo_regiao):
    valor_total_regiao = servicos_validos.groupby('Região')['Valor'].sum().reset_index()
    valor_total_regiao['Cor'] = valor_total_regiao['Valor'].apply(lambda x: 'red' if x > filtro_valor_maximo_regiao else 'blue')
       
    fig_regiao = px.bar(valor_total_regiao, x='Região', y='Valor', color='Cor', color_discrete_map={'red': 'red', 'blue': 'blue'}, text_auto=True, )

    return fig_regiao