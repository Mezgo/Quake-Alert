import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import pdfkit

def show_presentacion():
    """
    Muestra el KPI 1: Distribución de sismos por categoría de magnitud.
    Permite filtrar los sismos por fecha y muestra un gráfico de barras con la distribución resultante,
    junto con los porcentajes de las categorías y el dato KPI correspondiente.
    """
    '''
    def streamlit_page():
    
        if st.button('Exportar a PDF'):
            pdfkit.from_string(st._arrow_html_report.get_html(), 'streamlit_page.pdf')
            st.success('Página exportada a PDF con éxito')
    '''
    
    def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
    cargar_estilos()
    
    
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
    col1, col2, col3 = st.columns([0.475, 0.05, 0.475])
    with col1:
        st.image('metricas_presentacion.jpg', width=800, caption='Metricas Promedio')
    with col2:
        st.empty()
    with col3:
        st.empty()
        st.write('<div style="width: 400px; margin-left: 64px; font-size:38px">Marco de Problematica</div>', unsafe_allow_html=True)
        
        st.markdown(
        '<div style="width: 405px; margin-left: 64px; font-size:27px">La problemática principal radica en la imposibilidad de prevenir los sismos, pero es posible generar conciencia en la sociedad sobre cómo mitigar los peligros asociados a estos eventos.</div>', 
        unsafe_allow_html=True
        )

    '''
    SECCION CUERPO
    '''
    col1, col2, col3 = st.columns([0.4, 0.05, 0.55])
    with col1:
        st.image('medidas_prevencion.jpg', width=800, caption='Medidas de Prevención')
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
        
    # Llamar a la función principal
    #show_presentacion()