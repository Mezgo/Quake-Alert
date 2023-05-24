import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import presentacion
import KPI_1
import KPI_2
import KPI_3
import KPI_4
import KPI_5
import notificacion

 # Crear un DataFrame de ejemplo
data = pd.read_csv('chile.csv')
df = pd.DataFrame(data)

def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# Configurar la página
st.set_page_config(
    page_title="Alerta sísmica Chile",
    page_icon="🌎",
    layout="wide"    
)


# Opciones del menú de navegación
#menu = ["Inicio", "Presentacion", "KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5", "Notificacion"]
menu = ["Inicio", "Presentacion", "Categoria magnitud", "Confirmacion Mito", "Estacion del año", "Horas del dia", "Promedio Profundidad Superficie", "Notificacion"]
choice = st.sidebar.selectbox("Menú de navegación", menu)


# Mostrar contenido según la opción seleccionada
if choice == "Inicio":
    
    cargar_estilos()
    
    '''
    SECCION LOGO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
            col1.image('logo.png')
    with col2: 
            st.empty()

    
    #SECCION KPI
    
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='titulo_main'>Problemática</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()
    
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='texto_main'>Chile se encuentra en el Cinturon de Fuego del Pacífico en el cual se produce el 90% de los sismos del mundo</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()
    
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='titulo_main'>Análisis de Sismos</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()        
    
    
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='texto_main'>Analisis Sismos en Chile Magnitud de sus sismos</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()
    
    
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='texto_main'>Analisis del Mito: cuanto más tiempo pasa sin que alla sismo gran magnitud, mayor probabilidad de que ocurraun sismo de gran magnitud</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()
   
   
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='texto_main'>En que estacion del año se producen mas sismos</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()
    
    
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='texto_main'>En que hora del día se producen mas sismos</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()  
        
        
    col1, col2, col3 = st.columns([0.03, 0.90, 0.07])
    with col1:
        st.empty()
    with col2:
        st.markdown("<h1 class='texto_main'>Dependiendo donde se producen los sismos como puede afectar la población</h1>", unsafe_allow_html=True)
    with col3:
        st.empty()  
        
        
    
    #SECCION FOOTER
    
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown('<div class="EMPTY_footer"></div>', unsafe_allow_html=True)
        col1.image('logo_footer.png')
    with col2:
        st.empty()
     
        
elif choice == "Presentacion":
    presentacion.show_presentacion()
            
elif choice == "Categoria magnitud":
    KPI_1.show_kpi_1()
    
elif choice == "Confirmacion Mito":
    KPI_2.show_kpi_2()

elif choice == "Estacion del año":
    
    KPI_3.show_kpi_3()
    
elif choice == "Horas del dia":
    KPI_4.show_kpi_4()
    
elif choice == "Promedio Profundidad Superficie":
    KPI_5.show_kpi_5()

elif choice == "Notificacion":
    notificacion.show_notificacion()
    