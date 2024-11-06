from functions.get_zone_services import get_zone_services
from data.church_list import church_list
import streamlit as st
import plotly.express as px

def zone_services(servicos_validos):

    
    contagem_servicos_df = get_zone_services(church_list, servicos_validos)
    print(contagem_servicos_df)
    st.dataframe(contagem_servicos_df)

    fig = px.pie(contagem_servicos_df, names='Região', values='Serviços',
                     
                 title='Distribuição de Serviços por Região', height=800,)
    fig.update_traces(textinfo='label+value', textposition='inside')
    st.plotly_chart(fig, use_container_width=True)
    