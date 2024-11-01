import plotly.express as px  

def company_amount(servicos_validos):
    company_amount = servicos_validos.groupby('CNPJ').agg({
            'Valor': 'sum',
            'Empresa': 'first' 
        }).reset_index()

    sorted_companies = company_amount.sort_values(by='Valor', ascending=False).head(13)

    company_bar_chart = px.bar(sorted_companies, 
                        x='Empresa', 
                        y='Valor', 
                        title='Valor Total por Empresa', 
                        labels={'Empresa': 'Nome da Empresa', 'Valor': 'Valor Total'},
                        text_auto=True,
                        color='Valor',
                      )
    return company_bar_chart