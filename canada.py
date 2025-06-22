# canada.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@st.cache_data
def carregar_dados():
    """Carrega os dados de imigração do Canadá a partir de um arquivo CSV hospedado no GitHub. 
    Retorna um DataFrame contendo os dados."""
    # URL do arquivo CSV no GitHub

    url = 'https://raw.githubusercontent.com/alura-cursos/bibliotecas_visualizacao/refs/heads/main/Dados/imigrantes_canada.csv'
    dados = pd.read_csv(url)
    paises = dados['País'].unique().tolist()
    continentes = dados['Continente'].unique().tolist()
    regioes = dados['Região'].unique().tolist()
    anos = list(range(1980, 2014))  # Anos de 1980 a 2013
    # Convertendo os anos para string para facilitar a manipulação
    dados = dados.rename(columns={str(ano): ano for ano in range(1980, 2014)})
    dados.set_index('País', inplace=True)
    return dados, paises, continentes, regioes, anos

dados, paises, continentes, regioes, anos = carregar_dados()

st.set_page_config(
    page_title="Exploção de dados de imigração do Canadá",
    page_icon=":shark:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        
        'Get Help': 'https://docs.streamlit.io/',
    }
)

st.title("Imigração para o Canadá")

st.sidebar.header("Filtros")

btn_reset = st.sidebar.button("Resetar Dados")
btn_gerar = st.sidebar.button("Gráfico Interativo")
btn_plot = st.sidebar.button("Gráfico MatPlotlib")
btn_barras = st.sidebar.button("Gráfico de barras (Top10)")

col1,col2,col3 = st.columns(3)
with col1:
    continente = col1.multiselect("Selecione um continente", options=continentes, default=continentes, key='continente') #onchange=generate, default=continentes)
with col2:
    #st.sidebar.write("Selecione uma região para filtrar os países disponíveis.")
    regioes = dados[dados['Continente'].isin(continente)]['Região'].unique().tolist()
    regiao = col2.multiselect("Selecione uma região", regioes, default=regioes, key='regiao')
with col3:
    paises = dados[dados['Região'].isin(regiao)].index.unique().tolist()
    pais = col3.multiselect("Selecione o(s) país(es)", paises, default=paises, key = 'pais') #onchange=generate, default=paises)

ano_inicio = int(min(anos))
ano_fim = int(max(anos))
periodo = st.slider("Selecione o período:", min_value=ano_inicio, max_value=ano_fim, value=(ano_inicio,ano_fim), step=1, key='ano')
periodo_anos = list(range(min(periodo), max(periodo)))
pais_selected = list(pais)
st.write("---")

if btn_gerar:
    #if len(regiao) == 1:
    #    st.write(f"Região selecionada: {regiao}")
    #else:
    #    st.write(f"Regiões selecionada: {regiao}")
    #st.write(f"Países selecionados: {pais_selected  }")
    dados_filtrados = dados.loc[pais_selected, periodo_anos]
    dados_filtrados = dados_filtrados.T

    st.line_chart(dados_filtrados,
                  x_label='',
                  y_label='Número de Imigrantes',
                  )
    #st.dataframe(dados_filtrados)
elif btn_plot:
    dados_filtrados = dados.loc[pais_selected, periodo_anos]
    dados_filtrados = dados_filtrados.T
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot( dados_filtrados.index, dados_filtrados.values)#, marker='o', linestyle='-')
    ax.xaxis.set_major_locator(plt.MultipleLocator(5))
    ax.set_xlabel('')
    ax.set_ylabel('Número de Imigrantes')
    ax.set_title('Imigração para o Canadá\n1980 a 2013')
    st.pyplot(fig)
elif btn_barras:
    #cores = ['royalblue', 'orange', 'forestgreen', 'orchid', 'purple', 'brown', 'slateblue', 'gray', 'olive', 'navy']#, 'teal', 'tomato']
    dados_filtrados = dados.loc[pais_selected, periodo_anos]
    top10 = dados_filtrados.sum(axis=1).to_frame(name='Total')  # Somando os imigrantes por país no período selecionado  
    top10 = top10.sort_values(by='Total', ascending=False).reset_index().head(10)  # pegando os 10 maiores
    ds_top10 = top10.copy() # Cópia para exibição do DataFrame
    ds_top10.set_index('País', inplace=True) 
    # Concatenando o índice com o valor para exibição do gráfico na ordem correta
    top10['País'] = [f'{idx}-{val}' for idx, val in zip(top10.index, top10['País'])]
    st.bar_chart(top10, x='País', y='Total',
                 color='País',
                 y_label='',              
                 x_label='Número de Imigrantes',
                 horizontal=True
                 )
    st.dataframe(ds_top10)
  
else:
    st.info("Selecione o(s) Continente(s), Região(ões), País(es), período e clique no gráfico desejado para visualizar o resultado.")

st.write("---")

if btn_reset:
    dados, paises, continentes, regioes, anos = carregar_dados()
    st.session_state.clear()  # Limpa o estado da sessão
    st.rerun()

    btn_plot, btn_gerar = False

     
 
st.write("---")

