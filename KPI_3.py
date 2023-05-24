import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import datetime
from datetime import datetime

'''
def show_kpi_3():
    st.title("KPI 3")
    st.write("Antes de llamar a KPI_3.show_kpi_3()")
    st.write("Iniciando la función show_kpi_3()")
'''
 
def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


df = pd.read_csv('chile_poblacion_es.csv')

df['fecha_local'] = pd.to_datetime(df['fecha_local'])
df_filtrado = df[(df['magnitud'] > 5) & (df['profundidad'] < 70)]
df_filtrado['estacion'] = df_filtrado['fecha_local'].dt.month.apply(lambda x: (x % 12 + 3) // 3)
frecuencia_estaciones = df_filtrado['estacion'].value_counts()
etiquetas = ['Primavera', 'Verano', 'Otoño', 'Invierno']
valores = frecuencia_estaciones.reindex([1, 2, 3, 4])
etiquetas_filtradas = []
valores_filtrados = []
for etiqueta, valor in zip(etiquetas, valores):
    if valor > 0:
        etiquetas_filtradas.append(etiqueta)
        valores_filtrados.append(valor)
fig, ax = plt.subplots()
ax.pie(valores_filtrados, labels=etiquetas_filtradas, autopct='%1.1f%%', startangle=90, colors=[ '#e11e30', '#00BFFF', '#FFA500', '#8B4513'])





def show_kpi_3():
    cargar_estilos()
    
    
    # Calcular la cantidad de sismos por estación del año
    
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
        st.header('Estacion del año en que mas sismos se producen')
        '''
        GRAFICO
        '''
        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
    with col2:
        st.empty()
    with col3:
        #st.empty()
         # Utilizar la clase CSS en el elemento
        #st.markdown('<div class="espacio_conclusion"></div>', unsafe_allow_html=True)
        st.write('<div class="cuerpo_titulo">Conclusion</div>', unsafe_allow_html=True)
        
        st.markdown(
            '<div class="texto_conclusion">Este KPI muestra la estacion del año donde mas sismos ocurren en la Region de Chile es en la estacion de Verano</div>', 
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


