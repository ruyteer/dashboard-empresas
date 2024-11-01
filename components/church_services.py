
import json
import streamlit as st
import plotly.graph_objects as go


def church_services():
   # Carregar dados do JSON
    with open("/workspaces/dashboard-empresas/church_list.json", encoding="utf-8") as f:
        data = json.load(f)

    # Obter os nomes das regiões disponíveis
    region_names = []
    reginos = []

    for bloco in data['Asa Sul']:
        bloco_nome = bloco['Região']
        region_names.append(bloco_nome)
        reginos.append(bloco)
    for bloco in data['Taguatinga']:
        bloco_nome = bloco['Região']
        region_names.append(bloco_nome)
        reginos.append(bloco)
    for bloco in data['Solo Sagrado']:
        bloco_nome = bloco['Região']
        region_names.append(bloco_nome)
        reginos.append(bloco)

    # Criar um selectbox para escolher a região
    selected_region = st.selectbox("Selecione uma região:", region_names)

    # Coletar igrejas da região selecionada
    churches = []
    for lista in reginos:
        
    
        if lista['Região'] == selected_region:
         churches = lista['Igrejas']

    # Criar gráfico de barras para as igrejas da região selecionada
    if churches:  # Verifica se há igrejas para a região selecionada
        fig = go.Figure(go.Bar(
            x=churches,
            y=[1] * len(churches),  # Valor constante para criar a barra
            marker_color='#1d00db'  # Cor das barras
        ))

        # Atualizar layout do gráfico
        fig.update_layout(
            title=f"Igrejas na Região: {selected_region}",
            xaxis_title="Igrejas",
            yaxis_title="Quantidade",
            yaxis=dict(showticklabels=False),  # Esconder os rótulos do eixo y
            height=400
        )

        # Exibir o gráfico
        st.subheader("Gráfico de Igrejas (Em desenvolvimento)")
        st.write(fig)
    else:
        st.write("Nenhuma igreja encontrada para a região selecionada.")



