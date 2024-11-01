import plotly.express as px  

def company_services(servicos_validos):
    # Contar a quantidade de serviços por CNPJ
        quantidade_servicos = servicos_validos['CNPJ'].value_counts().reset_index()
        quantidade_servicos.columns = ['CNPJ', 'Quantidade de Serviços']

        # Unir com o DataFrame original para pegar os nomes das empresas
        quantidade_servicos = quantidade_servicos.merge(servicos_validos[['CNPJ', 'Empresa']], on='CNPJ', how='left')

        # Remover duplicatas para garantir que temos apenas um nome de empresa por CNPJ
        quantidade_servicos = quantidade_servicos.drop_duplicates(subset=['CNPJ'])

        # Selecionar apenas as colunas necessárias
        quantidade_servicos = quantidade_servicos[['Empresa', 'Quantidade de Serviços', 'CNPJ']]

      

        # Gráfico de pizza
        fig = px.pie(quantidade_servicos, names='Empresa', values='Quantidade de Serviços', height=600, )

        fig.update_traces(textinfo='label+value', textposition='inside')

        return fig