import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

st.title('Dados de Produção')
arquivo = st.file_uploader('Carregar arquivo')

arqnome = "Controles de Produção.csv"
base = pd.read_csv(arqnome)

if arquivo is not None:
    df = pd.read_csv(arquivo)
else:
    df = base

aba1, aba2 = st.tabs(['Início', 'Avançado'])

with aba1:
    st.header('O que você deseja?')
    img = Image.open("IANES2.png")
    img = img.resize((150, 150))
    st.image(img)
    opc = st.radio('Opções: ', options=(':mag: Ver todos os registros', ':heavy_plus_sign: Adicionar novo registro', ':x: Remover registro', ':pencil2: Editar registro', ':chart_with_upwards_trend: Ver dados em gráficos'),index= None)
    
    if opc == ':heavy_plus_sign: Adicionar novo registro':
        st.sidebar.subheader(':heavy_plus_sign: Novo registro')
        data = st.sidebar.date_input('Data')
        maq = st.sidebar.text_input('Máquina')
        turno = st.sidebar.selectbox('Turno', options=('Manhã', 'Tarde', 'Noite'), index=None)
        pp = st.sidebar.number_input('Peças Produzidas', min_value=0)
        pds = st.sidebar.number_input('Peças Defeituosas', min_value=0, max_value=pp)
        
        botao = st.sidebar.button('Salvar registro')
        if botao:
            novo = {'Data': [data],
                'Máquina': [maq],
                'Turno': [turno],
                'Peças Produzidas': [pp],
                'Peças Defeituosas': [pds]}
            novo_df = pd.DataFrame(novo)
            novo_df.to_csv(arqnome, mode='a', header=False, index=False)
            st.success('Registro salvo! :white_check_mark:')
            
            df_fim = pd.read_csv(arqnome)
            st.dataframe(df_fim)
    elif opc == ':mag: Ver todos os registros':
        st.header(':mag: Dados')
        df_fim = pd.read_csv(arqnome)
        st.dataframe(df_fim)
    elif opc == ':x: Remover registro':
        st.sidebar.subheader(':wastebasket: Remover Registro')
        df_fim = pd.read_csv(arqnome)
        maquinas = df_fim['Máquina'].unique()
        selmaq = st.sidebar.selectbox('Deseja remover o registro de qual máquina?', options=maquinas, index=None)
        
        botaormv = st.sidebar.button('Remover registro')
        if botaormv:
            dfrmv = df_fim[df_fim['Máquina'] != selmaq]
            dfrmv.to_csv(arqnome, index=False)
            st.success(f'Registro da máquina "{selmaq}" removido!')
            st.dataframe(dfrmv)
    elif opc == ':pencil2: Editar registro':
        st.sidebar.subheader(':pencil2: Editar Registro')
        df_fim = pd.read_csv(arqnome)
        maquinas = df_fim['Máquina'].unique()
        selmaq = st.sidebar.selectbox('Escolha uma máquina para editar', options=maquinas, index=None)
        linhamaq = df_fim[df_fim['Máquina'] == selmaq]
        st.dataframe(linhamaq)
        
        nvdata = st.sidebar.date_input(' Nova Data')
        nvturno = st.sidebar.selectbox('Novo turno', options=('Manhã', 'Tarde', 'Noite'), index=None)
        nvpp = st.sidebar.number_input('Nova produção', min_value=0)
        nvpds = st.sidebar.number_input('Novo n° de defeitos', min_value=0, max_value=nvpp)
        
        botaoedt = st.sidebar.button('Salvar alterações')
        if botaoedt:
            df_fim.loc[df_fim['Máquina'] == selmaq,'Data'] = nvdata
            df_fim.loc[df_fim['Máquina'] == selmaq,'Turno'] = nvturno
            df_fim.loc[df_fim['Máquina'] == selmaq,'Peças Produzidas'] = nvpp
            df_fim.loc[df_fim['Máquina'] == selmaq,'Peças Defeituosas'] = nvpds
            df_fim.to_csv(arqnome, index=False)
            st.success('Registro atualizdo!')
            st.dataframe(df_fim)
    elif opc == ':chart_with_upwards_trend: Ver dados em gráficos':
        st.sidebar.subheader(':chart_with_upwards_trend: Gráficos')
        df_fim = pd.read_csv(arqnome)
        peçboa = df_fim['Peças Produzidas']-df_fim['Peças Defeituosas']
        efic = (peçboa/df_fim['Peças Produzidas'])*100
        
        grafopcs = st.sidebar.radio('Gráficos: ',options=(':chart: Produção total por máquina', ':chart_with_downwards_trend: Defeitos por máquina', ':bar_chart: Eficiência (%) por Máquina'), index=None)
        if grafopcs == ':chart: Produção total por máquina':
            fig, ax = plt.subplots()
            ax.plot(df_fim['Máquina'], df_fim['Peças Produzidas'], color='green')
            ax.set_title('Produção Total por Máquiina')
            ax.set_xlabel('Máquina')
            ax.set_ylabel('Peças produzidas')
            ax.grid()
            st.sidebar.pyplot(fig)
        elif grafopcs == ':chart_with_downwards_trend: Defeitos por máquina':
            taxa_defeitos = (df_fim['Peças Defeituosas'] / df_fim['Peças Produzidas']) * 100
            fig1, ax1 = plt.subplots()
            ax1.bar(df_fim['Máquina'], taxa_defeitos, color='crimson')
            ax1.set_title('Taxa de Defeitos (%) por Máquina')
            ax1.set_xlabel('Máquina')
            ax1.set_ylabel('Taxa de Defeitos (%)')
            ax1.grid()
            st.sidebar.pyplot(fig1)
        elif grafopcs == ':bar_chart: Eficiência (%) por Máquina':
            fig2, ax2 = plt.subplots()
            ax2.plot(df_fim['Máquina'],efic, color='lightblue')
            ax2.set_title('Eficiência (%) por Máquina')
            ax2.set_xlabel('Máquina')
            ax2.set_ylabel('Eficiência (%)')
            ax2.grid()
            st.sidebar.pyplot(fig2)
        else:
            pass
        if efic.min()<90:
            st.error(':warning: A eficiência está inferior a 90%!')
        
        if df_fim['Peças Produzidas'].min()<80:
            st.error(':warning: A produção está inferior a 80 peças!')
with aba2:
    df_fim = pd.read_csv(arqnome)
    tdatas = (df_fim['Data'].unique())
    st.header(':date: Procurar registro em um Intervalo de Datas')
    seldata1 = st.selectbox('Do dia:', options=tdatas, index=None)
    seldata2 = st.selectbox('Ao dia:', options=tdatas, index=None)
    if seldata1 and seldata2 and seldata1 <= seldata2:
        intervalo = df_fim[(df_fim['Data'] >= seldata1) & (df_fim['Data'] <= seldata2)]
        st.subheader(f'Registros de {seldata1} até {seldata2}:')
        st.dataframe(intervalo)
    else:
        st.warning('Intervalo inválido!')
       
    maquinas = df_fim['Máquina'].unique()
    st.header(':computer: Procurar registros de uma Máquina específica')
    selmaq = st.selectbox('Escolha uma Máquina', options=maquinas, index=None)
    linhamaq = df_fim[df_fim['Máquina'] == selmaq]
    st.dataframe(linhamaq)
    
    turnos = df_fim['Turno'].unique()
    st.header(':sunny: Procurar registros de um Turno específico')
    selturno = st.selectbox('Escolha uma Turno', options=turnos, index=None)
    linhaturno = df_fim[df_fim['Turno'] == selturno]
    st.dataframe(linhaturno)
    
    st.header(':package: Média de produção por Máquina')
    for i in maquinas:
        mediaprod = df_fim.loc[df_fim['Máquina'] == i, 'Peças Produzidas'].mean()
        st.write(f'Média de produção da {i}: {np.round(mediaprod, 2)}')
