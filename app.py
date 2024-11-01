import pandas as pd
import streamlit as st
import plotly.express as px  
import plotly.graph_objs as go
from functions.rename_columns import rename_columns
from functions.convert_columns import convert_columns
from functions.filter_valid_data import filter_valid_data

from components.company_amount import company_amount
from components.company_services import company_services
from components.zone_amount import zone_amount
from components.cenacle_amount import cenacle_amount
from components.church_pie import church_pie
from components.church_services import church_services

import json

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

        ########

        tableLeft, tableRight = st.columns(2)

        tableLeft.subheader('Serviços finalizados')
        tableLeft.write(servicos_validos[['Empresa', 'CNPJ', 'Região', 'Cenáculo','Status',  'Valor']])
        
        tableRight.subheader('Serviços não finalizados')
        tableRight.write(servicos_invalidos[['Empresa', 'CNPJ', 'Região','Status',  'Data Original', 'Valor']])

        ########
        
        st.subheader('Valor Total por Empresa')

        company_bar_chart = company_amount(servicos_validos)
        
        st.plotly_chart(company_bar_chart)
     
        ########
        st.subheader('Quantidade de Serviços Prestados por Empresa')
        valid_or_invalid = st.selectbox('Status do Serviço', options=['Finalizados/Em andamento', 'Reprovados'])

        company_services_fig = company_services((servicos_validos if valid_or_invalid == 'Finalizados/Em andamento' else servicos_invalidos))
        st.plotly_chart(company_services_fig)  


        ########

        st.subheader('Valor total por Região')

        zone_input = st.number_input("Escolha o valor máximo para cada região", min_value=0, max_value=100000, value=50000)
       
        zone_fig = zone_amount(servicos_validos, zone_input)

        st.plotly_chart(zone_fig, use_container_width=True)

        #####

        st.subheader('Valor total por Cenáculo')

        cenacle_input = st.number_input("Escolha o valor máximo para cada cenáculo", min_value=0, max_value=100000, value=60000)

        cenacle_fig = cenacle_amount(servicos_validos, cenacle_input)
        
        st.plotly_chart(cenacle_fig, use_container_width=True)


        church_pie()
        church_services()
       

        

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")
else:
    st.info("Por favor, carregue um arquivo Excel para visualizar os dados.")