import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import folium
from streamlit_folium import folium_static

def show_kpi_5():
    st.title("KPI")

    df = pd.read_csv('regiones_chile_categorias.csv')
    df_po = pd.read_csv('regiones_chile.csv')

    df_po.rename(columns={'Latitud': 'latitud_C', 'Longitud': 'longitud_C'}, inplace=True)
    df.rename(columns={'longitud': 'longitud_po', 'latitud': 'latitud_po'}, inplace=True)

    col1, col2 = st.columns([0.65, 0.35])

    with col1:
        st.markdown("<h1 style='font-size: 30px;'>Promedio Profundidad Superficial Regiones de Chile</h1>", unsafe_allow_html=True)

    with col2:
        regiones = df_po['Region'].unique()

    col1, col2 = st.columns([0.65, 0.35])

    def show_map(region_seleccionada, fecha_inicio, fecha_fin, df_po, df):
        with col1:
            df_region_seleccionada = df_po[df_po['Region'] == region_seleccionada]

            df_region_seleccionada['latitud_C'] = df_region_seleccionada['latitud_C'].astype(str).str.replace('.', '')
            df_region_seleccionada['longitud_C'] = df_region_seleccionada['longitud_C'].astype(str).str.replace('.', '')
            df_region_seleccionada['latitud_C'] = df_region_seleccionada['latitud_C'].astype(float)
            df_region_seleccionada['longitud_C'] = df_region_seleccionada['longitud_C'].astype(float)

            df_filtrado = df[(df['profundidad_categoria'] == 'Superficial') & df['fecha_local'].between(str(fecha_inicio), str(fecha_fin))]

            if region_seleccionada in df_po['Region'].values:
                df_region_seleccionada = df_po[df_po['Region'] == region_seleccionada]
                latitud = df_region_seleccionada.loc[df_region_seleccionada['Region'] == region_seleccionada, 'latitud_C'].iloc[0]
            else:
                print("La región seleccionada no existe en el DataFrame.")

            regiones_poligonos = {
                'Santiago': [[-33.65, -71.15], [-33.65, -70.55], [-33.2, -70.55], [-33.2, -71.15]],
                'Valparaíso': [[-32.9, -71.5], [-32.9, -70.9], [-33.4, -70.9], [-33.4, -71.5]],
                'Biobío': [[-36.9, -73.8], [-36.9, -71.5], [-38.3, -71.5], [-38.3, -73.8]],
                'Coquimbo': [[-29.7, -71.8], [-29.7, -70.9], [-30.7, -70.9], [-30.7, -71.8]],
                'Antofagasta': [[-22.2, -69.8], [-22.2, -68.9], [-23.9, -68.9], [-23.9, -69.8]],
                'Araucanía': [[-38.2, -73.5], [-38.2, -71.9], [-39.7, -71.9], [-39.7, -73.5]]
            }

            mapa = folium.Map(location=[latitud, longitud], zoom_start=8, control_scale=True)

            if region_seleccionada in regiones_poligonos.keys():
                folium.Polygon(
                    locations=regiones_poligonos[region_seleccionada],
                    color='blue',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.2
                ).add_to(mapa)

            for i in range(len(df_filtrado)):
                folium.CircleMarker(
                    location=[df_filtrado.iloc[i]['latitud_po'], df_filtrado.iloc[i]['longitud_po']],
                    radius=3,
                    color='#FF0000',
                    fill=True,
                    fill_color='#FF0000'
                ).add_to(mapa)

            folium_static(mapa)

    with col2:
        region_seleccionada = st.selectbox('Selecciona una región', regiones)

        fecha_inicio = st.date_input("Fecha de inicio", value=pd.to_datetime('2020-01-01'), min_value=pd.to_datetime('2020-01-01'), max_value=pd.to_datetime('2022-12-31'))
        fecha_fin = st.date_input("Fecha de fin", value=pd.to_datetime('2022-12-31'), min_value=pd.to_datetime('2020-01-01'), max_value=pd.to_datetime('2022-12-31'))

        show_map(region_seleccionada, fecha_inicio, fecha_fin, df_po, df)

show_kpi_5()
