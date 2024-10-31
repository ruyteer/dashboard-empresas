import pandas as pd
import streamlit as st
import plotly.express as px  
import plotly.graph_objs as go
from functions.rename_columns import rename_columns
from functions.convert_columns import convert_columns
from functions.filter_valid_data import filter_valid_data

st.set_page_config(layout='wide')
st.title('Dashboard de Relatório de Empresas')




# Carregar o arquivo Excel
file_path = st.file_uploader("Carregue seu arquivo Excel", type=["xlsx", "xls"])

if file_path is not None:
    try:
        df = rename_columns(file_path)
        df_cleaned = convert_columns(df)
        
        st.title('Dashboard de Relatório de Empresas')

        servicos_invalidos, servicos_validos = filter_valid_data(df_cleaned)

        tableLeft, tableRight = st.columns(2)

        tableLeft.subheader('Serviços finalizados')
        tableLeft.write(servicos_validos[['Empresa', 'CNPJ', 'Região', 'Cenáculo','Status',  'Valor']])
        
        tableRight.subheader('Serviços não finalizados')
        tableRight.write(servicos_invalidos[['Empresa', 'CNPJ', 'Região','Status',  'Data Original', 'Valor']]app


        
        st.subheader('Valor Total por Empresa')

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
        
        st.plotly_chart(company_bar_chart)



        
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


  
       

        

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")
else:
    st.info("Por favor, carregue um arquivo Excel para visualizar os dados.")