import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Funciones
#df = pd.read_json('datos_chile_etl.json')
df = pd.read_csv('chile_etl.csv')

def show_notificacion():
    """
    Muestra el KPI 1: Distribución de sismos por categoría de magnitud.
    Permite filtrar los sismos por fecha y muestra un gráfico de barras con la distribución resultante,
    junto con los porcentajes de las categorías y el dato KPI correspondiente.
    """
    
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'])
    sismos_filtrados = df[(df['magnitude'] > 4) & (df['depth'] < 70)]

    sismos_filtrados = sismos_filtrados.sort_values(by=['date', 'time'], ascending=False)
    ultimo_sismo = sismos_filtrados.iloc[0]
    hora_minutos = ultimo_sismo['time'].strftime('%H:%M')
    magnitud = ultimo_sismo['magnitude']
    profundidad = ultimo_sismo['depth']
    #region = ultimo_sismo['region']


    print("Último sismo mayor a 4 grados y a menos de 70 km de profundidad:")
    print("Hora y minutos:", hora_minutos)
    print("Magnitud:", magnitud)
    print("Profundidad:", profundidad)
    #print("Región:", region)


    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'])

    sismos_filtrados = df[(df['magnitude'] > 4) & (df['depth'] < 70)]
    sismos_filtrados = sismos_filtrados.sort_values(by=['date', 'time'], ascending=False)
    ultimo_sismo = sismos_filtrados.iloc[0]
    latitud = ultimo_sismo['latitude']
    longitud = ultimo_sismo['longitude']
    mapa = folium.Map(location=[latitud, longitud], zoom_start=6)

    folium.Marker(
        location=[latitud, longitud],
        popup='Último sismo',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(mapa)

    mapa
    
    
    def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    cargar_estilos()


    # SECCION LOGO
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        col1.image('logo.png')
    with col2:
        st.empty()

    # SECCION ENCABEZADO
    col1, col2, col3 = st.columns([0.475, 0.05, 0.475])
    with col1:
        st.markdown("<h1 style='font-size: 30px;'>Ultimo Sismo de Temblor Fuerte</h1>", unsafe_allow_html=True)
    with col2:
        st.empty()
    with col3:
        st.empty()
    
    # CONTENEDOR
    col_container = st.columns([0.475, 0.05, 0.475])
    with col_container[0]:
        col_container_nested = st.columns([0.5, 0.5])
        with col_container_nested[0]:
            # KPI 1: Magnitud > 4.5
            css = """
            .card_1 {
                padding: 10px;
                background-color: #f5f5f5;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-right: 10px;
            }
            """
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="card_1">
                    <h2 class="kpi-title_1">Magnitud > 4.5</h2>
                    <h1 class="kpi-value_1">{magnitud:.2f}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_container_nested[1]:
            # KPI 2: Profundidad < 70kms
            css = """
            .card_1 {
                padding: 10px;
                background-color: #f5f5f5;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            """
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="card_1">
                    <h2 class="kpi-title_1">Profundidad < 70kms</h2>
                    <h1 class="kpi-value_1">{profundidad:.2f}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            
            
    with col_container[1]:
        st.empty()
        

    with col_container[2]:
        st.write("Medidas de Prevencion")
        st.image('medidas_prevencion.jpg', width=500, caption='Medidas de Prevención')

    # SECCION MAPA
    col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.05, 0.4])
    with col1:
        st.empty()
        # folium_static(mapa)
        
        css = """
        .map-container {
            margin-top: -150px;
        }
        """
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        #folium_static(mapa)
        folium_static(mapa)

    with col2:
        st.empty()

    with col3:
        st.empty()

    with col4:
        st.empty()

    # SECCION FOOTER
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown('<div class="EMPTY_footer"></div>', unsafe_allow_html=True)
        col1.image('logo_footer.png')

    with col2:
        st.empty()


