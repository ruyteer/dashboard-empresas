import json
import streamlit as st
import plotly.graph_objects as go

def load_church_data():
    """Load church data from JSON file."""
    with open("church_list.json", encoding="utf-8") as file:
        return json.load(file)

def church_services():
    # Carregar dados de igrejas
    data = load_church_data()

    # Inicializar listas para nomes de regiões e detalhes das igrejas
    region_names = []
    church_blocks = []

    # Iterar por cada região e extrair blocos
    for region in ["Asa Sul", "Taguatinga", "Solo Sagrado"]:
        for block in data[region]:
            region_name = block['Região']
            region_names.append(region_name)
            church_blocks.append(block)

    # Criar selectbox para escolher a região
    selected_region = st.selectbox("Select a region:", region_names)

    # Coletar igrejas da região selecionada
    selected_churches = [block['Igrejas'] for block in church_blocks if block['Região'] == selected_region]

    # Criar gráfico de pizza para mostrar o número de igrejas na região selecionada
    if selected_churches:
        church_counts = {church: len(services) for church, services in selected_churches[0].items()}
        
        # Criar figura de gráfico de pizza
        fig = go.Figure(
            go.Pie(
                labels=list(church_counts.keys()),
                values=list(church_counts.values()),
                hole=0.3
            )
        )
        fig.update_layout(title_text=f"Igrejas em {selected_region}")

        # Exibir o gráfico de pizza
        st.subheader("Churches Chart (Under Development)")
        st.plotly_chart(fig)
    else:
        st.write("No churches found for the selected region.")
