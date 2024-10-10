import pandas as pd
import streamlit as st
import plotly.express as px  # Importando a biblioteca Plotly

# Carregar os dados limpos
file_path = 'relatorio_atualizado.xlsx'  # Certifique-se de que o arquivo esteja no mesmo diretório
df = pd.read_excel(file_path, sheet_name='Planilha1')

# Renomear colunas e limpar dados
df_cleaned = df.rename(columns={
    'RELAÇÃO DE SERVIÇO - PROCESSO SIMPLIFICADO (de Janeiro a Outubro 2024)': 'Empresa',
    'Unnamed: 1': 'CNPJ',
    'Unnamed: 2': 'Cenáculo',
    'Unnamed: 3': 'Data',
    'Unnamed: 4': 'Valor',
    'Unnamed: 5': 'Valor Total'
}).drop(index=0).dropna(how='all')

# Converter colunas para os formatos corretos, mantendo a data original
df_cleaned['Data Original'] = df_cleaned['Data']  # Armazena a data original
df_cleaned['Data'] = pd.to_datetime(df_cleaned['Data'], errors='coerce')  # Converte para datetime, com erro coercivo
df_cleaned['Valor'] = pd.to_numeric(df_cleaned['Valor'], errors='coerce')
df_cleaned['Valor Total'] = pd.to_numeric(df_cleaned['Valor Total'], errors='coerce')

# Título do dashboard
st.title('Dashboard de Relatório de Empresas')

# Filtrar serviços com datas inválidas
servicos_invalidos = df_cleaned[df_cleaned['Data'].isna()]

# Filtrar serviços com datas válidas
servicos_validos = df_cleaned[df_cleaned['Data'].notna()]

# Filtro por data
st.sidebar.header('Filtrar por data')
start_date = st.sidebar.date_input('Data inicial', servicos_validos['Data'].min())
end_date = st.sidebar.date_input('Data final', servicos_validos['Data'].max())

# Aplicar filtro de data
mask = (servicos_validos['Data'] >= pd.to_datetime(start_date)) & (servicos_validos['Data'] <= pd.to_datetime(end_date))
df_filtered = servicos_validos[mask]

# Mostrar a tabela filtrada sem o "Valor Total"
st.subheader('Dados das Empresas')
df_filtered_no_total = df_filtered.drop(columns=['Valor Total', 'Data Original'])
st.write(df_filtered_no_total)

# Gráfico de barras: Valor total por empresa
st.subheader('Valor total por Empresa')
valor_total_empresa = df_filtered.groupby('Empresa')['Valor Total'].sum().reset_index()
st.bar_chart(valor_total_empresa.set_index('Empresa'))

# Nova seção: Quantidade de serviços prestados por empresa
st.subheader('Quantidade de Serviços Prestados por Empresa')
quantidade_servicos = df_filtered['Empresa'].value_counts().reset_index()
quantidade_servicos.columns = ['Empresa', 'Quantidade de Serviços']

# Gráfico de pizza
fig = px.pie(quantidade_servicos, names='Empresa', values='Quantidade de Serviços', title='Quantidade de Serviços Prestados por Empresa')
st.plotly_chart(fig)  # Exibir o gráfico de pizza no Streamlit

# Gráfico de barras: Valor total por Cenáculo
st.subheader('Valor total por Cenáculo')
valor_total_cenaculo = df_filtered.groupby('Cenáculo')['Valor Total'].sum().reset_index()
st.bar_chart(valor_total_cenaculo.set_index('Cenáculo'))

# Seção para Dados com Datas Inválidas
st.subheader('Dados com Datas Inválidas')
# Aqui mantemos a coluna original da data
st.write(servicos_invalidos[['Empresa', 'CNPJ', 'Cenáculo', 'Data Original', 'Valor']])
