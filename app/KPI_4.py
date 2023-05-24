import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import time

def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def show_kpi_4():
    #st.title("KPI 4")
             
    cargar_estilos()

    def leer_datos_csv(archivo_csv):
        df = pd.read_csv(archivo_csv)
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        return df

    def filtrar_sismos(df, magnitud_min, profundidad_max):
        filtro = (df['magnitud'] > magnitud_min) & (df['profundidad'] < profundidad_max)
        df_filtrado = df[filtro]
        return df_filtrado

    def contar_sismos_por_hora(df, hora_inicio, hora_fin):
        filtro = (df['fecha_hora'].dt.hour >= hora_inicio.hour) & (df['fecha_hora'].dt.hour <= hora_fin.hour)
        sismos_por_hora = df[filtro]['fecha_hora'].dt.hour.value_counts().sort_index()
        return sismos_por_hora

    '''
    def graficar_sismos_por_hora(sismos_por_hora):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(sismos_por_hora.index, sismos_por_hora.values)
        ax.set_xlabel('Hora del Día')
        ax.set_ylabel('Cantidad de Sismos')
        ax.set_title('Cantidad de Sismos por Hora del Día (Magnitud > 5, Profundidad < 70 km)')
        return fig
    '''
    
    def graficar_sismos_por_hora_barras_y_lineas(sismos_por_hora):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(sismos_por_hora.index, sismos_por_hora.values, color='blue', label='Barras')
        ax.plot(sismos_por_hora.index, sismos_por_hora.values, color='red', label='Líneas')
        ax.set_xlabel('Hora del Día')
        ax.set_ylabel('Cantidad de Sismos')
        ax.set_title('Cantidad de Sismos por Hora del Día (Magnitud > 5, Profundidad < 70 km)')
        ax.legend()
        return fig

    # Leer datos del archivo CSV y procesarlos
    df = leer_datos_csv('chileFrec.csv')
    df_filtrado = filtrar_sismos(df, 5, 70)
    sismos_por_hora = contar_sismos_por_hora(df_filtrado, time(0, 0), time(23, 59))
    
    
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
        #st.markdown("<h1 style='font-size: 30px;'>KPI 1: Distribución de sismos por categoría de magnitud</h1>", unsafe_allow_html=True)
        appointment = st.slider(
            "Selecciona un rango horario:",
            value=(time(0, 0), time(23, 59))
        )
    with col2:
        st.empty()
    with col3:
        st.empty()
    
    
    '''
    SECCION CUERPO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown("<h1 style='font-size: 30px;'>KPI 1: Distribución de sismos por categoría de magnitud</h1>", unsafe_allow_html=True)
        sismos_por_hora = contar_sismos_por_hora(df_filtrado, appointment[0], appointment[1])
        '''
        fig = graficar_sismos_por_hora(sismos_por_hora)
        st.pyplot(fig)
        '''
        fig = graficar_sismos_por_hora_barras_y_lineas(sismos_por_hora)
        st.pyplot(fig)
    with col2:
        st.empty()
    with col3:
        st.empty()
        

    
    '''
    SECCION FOOTER
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown('<div class="EMPTY_footer"></div>', unsafe_allow_html=True)
        col1.image('logo_footer.png')
    with col2:
        st.empty()
