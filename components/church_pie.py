import json
import streamlit as st
import plotly.graph_objects as go

def church_pie():
    # Carregar dados do JSON
    with open("church_list.json", encoding="utf-8") as f:
        data = json.load(f)

    # Preparar dados para o gráfico
    labels = []
    parents = []
    values = []

    # Adicionar blocos principais e seus dados
    for bloco in data['Informações dos Blocos']:
        labels.append(bloco['Nome'])
        parents.append("")
        values.append(bloco['Igrejas'])
        
        # Adicionar nós filhos (Sede de Bloco, Sedes Regionais, Núcleos)
        labels.extend([f"{bloco['Nome']} - Sede de Bloco", f"{bloco['Nome']} - Sedes Regionais", f"{bloco['Nome']} - Núcleos"])
        parents.extend([bloco['Nome']] * 3)
        values.extend([bloco['Sede de Bloco'], bloco['Sedes Regionais'], bloco['Núcleos']])

    # Definir cores personalizadas (verde, azul e amarelo)
    colors = ['#039e00', '#1d00db', '#ffff00']  # Verde, Azul, Amarelo

    # Criar gráfico sunburst
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(colors=colors * (len(labels) // len(colors) + 1), line=dict(color='white', width=1))
    ))

    # Atualizar layout do gráfico
    fig.update_layout(title="Quantidade de Igrejas por Bloco", margin=dict(t=0, l=0, r=0, b=0))

    # Criar colunas para o gráfico e as informações
    col1, col2 = st.columns([2, 1])  # 2/3 para o gráfico e 1/3 para as informações

    # Exibir gráfico na primeira coluna
    with col1:
        st.subheader("Gráfico de Igrejas por Bloco")
        st.write(fig)

    # Exibir informações na segunda coluna com tamanho de fonte menor
    with col2:
        st.subheader("Informações dos Blocos")
        
        for bloco in data['Informações dos Blocos']:
            st.markdown(f"<div style='font-size: 12px;'><strong>{bloco['Nome']}</strong><br>"
                        f"Sede de Bloco: {bloco['Sede de Bloco']}<br>"
                        f"Sedes Regionais: {bloco['Sedes Regionais']}<br>"
                        f"Igrejas: {bloco['Igrejas']}<br>"
                        f"Núcleos: {bloco['Núcleos']}<br>"
                        f"Responsável: {bloco['Responsável']}</div>", unsafe_allow_html=True)
            st.markdown("---")  # Linha de separação entre blocos


