
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Relatório - Empresas")

data = {
    'ano': [2018, 2019, 2020, 2021, 2022],
    'vendas': [100, 150, 230, 350, 563]
}

df = pd.DataFrame(data)

st.dataframe(df)