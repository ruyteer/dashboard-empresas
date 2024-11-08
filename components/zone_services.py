from functions.get_zone_services import get_zone_services
from data.church_list import church_list
import streamlit as st
import plotly.express as px

def zone_services(servicos_validos):

    
    contagem_servicos_df, contagem_servicos = get_zone_services(church_list, servicos_validos)

    st.title('Distribuição de Serviços por Região')

    def highlight_row_red(row):
          if row['Serviços'] < 1:
               return ['background-color: red'] * len(row)
          return [''] * len(row)



    df_services = contagem_servicos_df.style.apply(highlight_row_red, axis=1)
 
  
    st.dataframe(df_services, use_container_width=True, column_config={
        "Valor Total": st.column_config.NumberColumn(
            "Valor Total",
            format="R$ %d"
        ),
    })
   

    fig = px.pie(contagem_servicos_df, names='Região', values='Serviços',
                     
                 title='Quantidade de Serviços por Região', height=800)
    fig.update_traces(textinfo='label+value', textposition='inside')

    st.plotly_chart(fig, use_container_width=True)
 
    


    