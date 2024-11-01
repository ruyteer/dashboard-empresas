import plotly.express as px  

def cenacle_amount(servicos_validos, filtro_valor_maximo_cenaculo):
    valor_total_cenaculo = servicos_validos.groupby('Cenáculo')['Valor'].sum().reset_index()
    valor_total_cenaculo['Cor'] = valor_total_cenaculo['Valor'].apply(lambda x: 'red' if x > filtro_valor_maximo_cenaculo else 'green')
    fig_cenaculo = px.bar(valor_total_cenaculo, x='Cenáculo', y='Valor', color='Cor', text_auto=True, 
                      color_discrete_map={'red': 'red', 'green': 'green'})
    
    return fig_cenaculo