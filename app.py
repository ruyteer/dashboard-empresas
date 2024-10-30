import pandas as pd
import streamlit as st
import plotly.express as px  
import plotly.graph_objs as go
st.set_page_config(layout='wide')
st.title('Dashboard de Relatório de Empresas')




# Carregar o arquivo Excel
file_path = st.file_uploader("Carregue seu arquivo Excel", type=["xlsx", "xls"])

if file_path is not None:
    try:

        df = pd.read_excel(file_path, sheet_name='Sheet1')
        # Renomear colunas e limpar dados
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

        # Converter colunas para os formatos corretos
        df_cleaned['Data Original'] = df_cleaned['Data'] 
        df_cleaned['Data'] = pd.to_datetime(df_cleaned['Data'], errors='coerce')  
        df_cleaned['Valor'] = df_cleaned['Valor'].str.replace('.', '', regex=False)  
        df_cleaned['Valor'] = df_cleaned['Valor'].str.replace(',', '.', regex=False)  
        df_cleaned['Valor'] = pd.to_numeric(df_cleaned['Valor'], errors='coerce')

        # Título do dashboard
        st.title('Dashboard de Relatório de Empresas')

        # Filtrar serviços com datas inválidas
        servicos_invalidos = df_cleaned[(df_cleaned['Status'] != 'Resolvido') & (df_cleaned['Status'] != 'Aguardando Solicitante')]

        # Filtrar serviços com datas válidas
        servicos_validos = df_cleaned[
    (df_cleaned['Status'] == 'Resolvido') | 
    (df_cleaned['Status'] == 'Aguardando Solicitante')
]


        # Mostrar a tabela filtrada apenas com valores específicos
        tab1, tab2 = st.columns(2)

        tab1.subheader('Serviços finalizados')
        tabela_servicos_validos = servicos_validos.drop(columns=['Avaliação do Serviço', 'Data Original', 'Número de Referência',  'Estado', 'Ação', 'Tipo de Serviço', 'Bloco', 'Nome Completo', 'Data de Criação'])
        tab1.write(tabela_servicos_validos)

        # Gráfico de barras: Valor total por empresa
        
        st.subheader('Valor Total por Empresa')

        # Agrupar os valores por CNPJ e somar os valores de serviços
        valor_total_empresa = servicos_validos.groupby('CNPJ').agg({
            'Valor': 'sum',
            'Empresa': 'first'  # Pega o primeiro nome da empresa encontrada
        }).reset_index()

        top_10_empresas = valor_total_empresa.sort_values(by='Valor', ascending=False).head(13)


        # Criar o gráfico de barras com Plotly
        fig_bar = px.bar(top_10_empresas, 
                        x='Empresa', 
                        y='Valor', 
                        title='Valor Total por Empresa', 
                        labels={'Empresa': 'Nome da Empresa', 'Valor': 'Valor Total'},
                        text_auto=True, )

        # Exibir o gráfico no Streamlit

        st.plotly_chart(fig_bar)
        
       # Nova seção: Quantidade de serviços prestados por empresa
     

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
        fig = px.pie(quantidade_servicos, names='Empresa', values='Quantidade de Serviços', title='Quantidade de Serviços Prestados por Empresa', height=600, )

        fig.update_traces(textinfo='label+value', textposition='inside')
       
        st.plotly_chart(fig)  # Exibir o gráfico de pizza no Streamlit


        # Gráfico de barras: Valor total por Cenáculo (substituindo por Região, já que não há Cenáculo)

      
        col1, col2 = st.columns(2)
        filtro_valor_maximo_local = st.slider("Escolha o valor máximo para cada região/cenáculo", min_value=0, max_value=100000, value=50000)
       

        col1.subheader('Valor total por Região')
        valor_total_regiao = servicos_validos.groupby('Região')['Valor'].sum().reset_index()
        valor_total_regiao['Cor'] = valor_total_regiao['Valor'].apply(lambda x: 'red' if x > filtro_valor_maximo_local else 'blue')
        # col1.bar_chart(valor_total_regiao.set_index('Região'))
        fig_regiao = px.bar(valor_total_regiao, x='Região', y='Valor', color='Cor', color_discrete_map={'red': 'red', 'blue': 'blue'})
        col1.plotly_chart(fig_regiao, use_container_width=True)

        col2.subheader('Valor total por Cenáculo')
        valor_total_cenaculo = servicos_validos.groupby('Cenáculo')['Valor'].sum().reset_index()
        valor_total_cenaculo['Cor'] = valor_total_cenaculo['Valor'].apply(lambda x: 'red' if x > filtro_valor_maximo_local else 'green')
        fig_cenaculo = px.bar(valor_total_cenaculo, x='Cenáculo', y='Valor', color='Cor', 
                      color_discrete_map={'red': 'red', 'green': 'green'})
        col2.plotly_chart(fig_cenaculo, use_container_width=True)


        # Seção para Serviços não finalizados
        tab2.subheader('Serviços não finalizados')
        # Aqui mantemos a coluna original da data
        tab2.write(servicos_invalidos[['Empresa', 'CNPJ', 'Região','Status',  'Data Original', 'Valor']])

        

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")
else:
    st.info("Por favor, carregue um arquivo Excel para visualizar os dados.")