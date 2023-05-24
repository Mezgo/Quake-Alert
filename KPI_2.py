import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
from datetime import timedelta
import seaborn as sns

def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
def show_kpi_2():
    #st.title("KPI 2")
    
    cargar_estilos()
    
    # Funciones
    df = pd.read_csv('chile_poblacion_es.csv')
    
    df_fh = df.copy()

    df_fh['fecha_local'] = pd.to_datetime(df_fh['fecha_local'])
    df_fh['hora_local'] = pd.to_datetime(df_fh['hora_local'])
    df_fh_filtrado = df_fh[(df_fh['magnitud'] > 4.5) & (df_fh['profundidad'] < 70)]
    df_fh_filtrado = df_fh_filtrado.sort_values(by=['fecha_local', 'hora_local'])
    df_fh_filtrado['dif_tiempo'] = df_fh_filtrado['fecha_local'].diff().fillna(pd.Timedelta(seconds=0)) + df_fh_filtrado['hora_local'].diff().fillna(pd.Timedelta(seconds=0))
    plt.figure(figsize=(10, 6))
    x = df_fh_filtrado['magnitud']
    y = df_fh_filtrado['dif_tiempo'].dt.days
    plt.scatter(x, y, color='#e11e30')
    plt.xlabel('Magnitud')
    plt.ylabel('Días desde el último sismo')
    plt.title('Relación entre Magnitud y Días desde el último sismo')
    plt.xlim(0, 8.5)
    plt.ylim(0, 20)
    #plt.show()


    '''
    SECCION LOGO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
            col1.image('logo.png')
    with col2: 
            st.empty()


    '''
    SECCION KPI
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        #st.markdown("<h1 style='font-size: 30px;'>KPI 1: </h1>", unsafe_allow_html=True)
        st.empty()
    with col2:
        st.empty()
    with col3:
        st.empty()
    
    '''
    SECCION CUERPO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown("<h1 style='font-size: 30px;'>KPI: Confirmacion o no de un mito</h1>", unsafe_allow_html=True)
        '''
        GRAFICO
        '''
        #st.subheader('Gráfico de barras')
        st.pyplot(plt.gcf())
    with col2:
        st.empty()
    with col3:
        #st.subheader('Estadísticas descriptivas')
        #st.write(stats)
        # Utilizar la clase CSS en el elemento
        #st.markdown('<div class="espacio_conclusion"></div>', unsafe_allow_html=True)
       st.write('<div class="cuerpo_titulo">Conclusion</div>', unsafe_allow_html=True)
        
       st.markdown(
            '<div class="texto_conclusion">El Mito no es cierto ya que en ocasiones han pasado pocos días desde un sismo de gran magnitud y ocurre otro de mayor  magnitud. Al parecer no hay relación entre el tiempo que pasa entre sismo y sismo. </div>', 
            unsafe_allow_html=True
            )
        
    
    '''
    SECCION FOOTER
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown('<div class="EMPTY_footer"></div>', unsafe_allow_html=True)
        col1.image('logo_footer.png')
    with col2:
        st.empty()


