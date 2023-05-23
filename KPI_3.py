import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static

'''
def show_kpi_3():
    st.title("KPI 3")
    st.write("Antes de llamar a KPI_3.show_kpi_3()")
    st.write("Iniciando la función show_kpi_3()")
'''
 

@st.cache_data
def cargar_datos():
    df = pd.read_csv('chile.csv')
    return df

def calcular_sismos_por_estacion(df):
    df['fecha_local'] = pd.to_datetime(df['fecha_local'])
    df['estacion'] = df['fecha_local'].dt.to_period('Q').dt.strftime('%b')
    sismos_por_estacion = df['estacion'].value_counts()
    return sismos_por_estacion

def graficar_sismos_por_estacion(sismos_por_estacion):
    estaciones_ordenadas = ['Dec', 'Mar', 'Jun', 'Sep']
    colores = {'Dec': 'orange', 'Mar': 'yellow', 'Jun': 'blue', 'Sep': 'green'}
    etiquetas = {'Dec': 'Verano', 'Mar': 'Otoño', 'Jun': 'Invierno', 'Sep': 'Primavera'}

    kpi_sismos_estaciones = pd.DataFrame({
        'Estacion': estaciones_ordenadas,
        'Cantidad de Sismos': [sismos_por_estacion.get(estacion, 0) for estacion in estaciones_ordenadas]
    })

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(kpi_sismos_estaciones['Estacion'], kpi_sismos_estaciones['Cantidad de Sismos'],
           color=[colores.get(estacion, 'gray') for estacion in kpi_sismos_estaciones['Estacion']])
    ax.set_xlabel('Estación del Año')
    ax.set_ylabel('Cantidad de Sismos')
    ax.set_title('Cantidad de Sismos por Estación del Año')
    ax.set_xticks(kpi_sismos_estaciones['Estacion'])
    ax.set_xticklabels([etiquetas.get(estacion, 'Desconocida') for estacion in kpi_sismos_estaciones['Estacion']])

    return fig

def generar_kpi(df, sismos_por_estacion):
    estacion_max_sismos = sismos_por_estacion.idxmax()
    cantidad_max_sismos = sismos_por_estacion.max()

    estaciones_ordenadas = ['Dec', 'Mar', 'Jun', 'Sep']
    colores = {'Dec': 'orange', 'Mar': 'yellow', 'Jun': 'blue', 'Sep': 'green'}
    etiquetas = {'Dec': 'Verano', 'Mar': 'Otoño', 'Jun': 'Invierno', 'Sep': 'Primavera'}

    # Configurar el tamaño del gráfico
    plt.figure(figsize=(10, 6))

    # Graficar las barras de cantidad de sismos por estación del año con colores personalizados
    plt.bar([etiquetas.get(estacion, 'Desconocida') for estacion in estaciones_ordenadas], [sismos_por_estacion.get(estacion, 0) for estacion in estaciones_ordenadas],
            color=[colores.get(estacion, 'gray') for estacion in estaciones_ordenadas])

    # Configurar los ejes y etiquetas
    plt.xlabel('Estación del Año')
    plt.ylabel('Cantidad de Sismos')
    #plt.title('Cantidad de Sismos por Estación del Año', loc='left')

    # Anotar el KPI en el gráfico
    plt.annotate(f"{etiquetas.get(estacion_max_sismos, 'Desconocida')} ({cantidad_max_sismos} sismos)",
                xy=(etiquetas.get(estacion_max_sismos, 'Desconocida'), cantidad_max_sismos),
                xytext=(10, 30),
                textcoords="offset points",
                ha='center',
                va='center',
                fontsize=15,
                color='red',
                arrowprops=dict(arrowstyle="->"))

    # Devolver la figura generada
    return plt.gcf()

def show_kpi_3():
    st.title("KPI 3")
    st.write("Iniciando la función show_kpi_3()")

    # Cargar los datos
    df = cargar_datos()

    # Calcular la cantidad de sismos por estación del año
    sismos_por_estacion = calcular_sismos_por_estacion(df)
    st.write(sismos_por_estacion)  # Punto de depuración: muestra los valores de sismos_por_estacion en Streamlit

    # Bloque 3: Gráfico de barras de la cantidad de sismos por estación del año
    col1, col2 = st.columns([0.65, 0.35])
    with col1:
        st.header('Gráfico de barras de la cantidad de sismos por estación del año')
        fig = graficar_sismos_por_estacion(sismos_por_estacion)
        st.pyplot(fig)

    # Bloque 4: Generación del KPI (Indicador Clave de Rendimiento)
    with col2:
        st.header('KPI: Estación con más sismos')
        kpi_fig = generar_kpi(df, sismos_por_estacion)
        st.pyplot(kpi_fig)




