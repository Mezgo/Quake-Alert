import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
from datetime import timedelta
import seaborn as sns

@st.cache_data
def show_kpi_2():
    st.title("KPI 2")

    # Funciones
    def cargar_datos():
        df = pd.read_csv('chileFrec.csv')
        return df

    def preprocesar_datos(df):
        df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
        df.sort_values(by='fecha_hora', ascending=True, inplace=True)
        df['diferencia_tiempo'] = df['fecha_hora'].diff().dt.total_seconds() / (24 * 60 * 60)  # Convertir a días
        return df

    def filtrar_datos(df):
        filtered_df = df[(df['magnitud'] > 6) & (df['profundidad'] < 70)]
        filtered_df['dif_tiempo'] = filtered_df['fecha_hora'].diff().dt.total_seconds() / (24 * 60 * 60)  # Convertir a días
        return filtered_df

    def obtener_estadisticas(df):
        return df.describe()

    def grafico_dispersion(df):
        # Configurar el tamaño del gráfico
        plt.figure(figsize=(10, 6))

        # Convertir la diferencia de tiempo a días
        dif_tiempo_dias = df['dif_tiempo']

        # Crear una lista de colores rojos en un degradado
        colormap = plt.cm.get_cmap('Reds')
        normalize = mcolors.Normalize(vmin=6, vmax=8)  # Rango de magnitudes

        # Generar el gráfico de dispersión
        scatter = plt.scatter(dif_tiempo_dias, df['magnitud'], c=df['magnitud'], cmap=colormap, norm=normalize)

        # Añadir una barra de colores
        cbar = plt.colorbar(scatter)
        cbar.set_label('Magnitud')

        # Configurar los ejes y etiquetas
        plt.xlabel('Diferencia de tiempo (días)')
        plt.ylabel('Magnitud')
        plt.title('Relación entre magnitud y diferencia de tiempo de sismos seleccionados')

        # Mostrar el gráfico
        st.pyplot(plt)

    def grafico_barras(df):
        # Configurar el tamaño del gráfico
        plt.figure(figsize=(10, 6))

        # Convertir la diferencia de tiempo a días
        dif_tiempo_dias = df['dif_tiempo']

        # Calcular las posiciones de las barras
        x_pos = range(len(df))

        # Crear una lista de colores rojos en un degradado
        colormap = plt.cm.get_cmap('Reds')
        normalize = mcolors.Normalize(vmin=6, vmax=8)  # Rango de magnitudes

        # Crear una instancia de ScalarMappable con los colores correspondientes
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=normalize)
        sm.set_array([])  # Establecer un array vacío para la asignación de colores

        # Graficar las barras de magnitud con colores asignados por sm
        plt.bar(x_pos, df['magnitud'], color=sm.to_rgba(df['magnitud']))

        # Configurar los ejes y etiquetas
        plt.xlabel('Diferencia de tiempo (días)')
        plt.ylabel('Magnitud')
        plt.title('Magnitud de sismos seleccionados')
        plt.xticks(x_pos, dif_tiempo_dias, rotation=90)

        # Añadir una barra de colores al eje actual
        ax = plt.gca()
        cbar = plt.colorbar(sm, label='Magnitud', ax=ax)

        # Mostrar el gráfico
        st.pyplot(plt)


    # Código Streamlit

    # Cargar y preprocesar los datos
    df = cargar_datos()
    #st.write("DataFrame cargado:")
    #st.write(df)  # Punto de depuración para verificar el DataFrame cargado

    df = preprocesar_datos(df)
    #st.write("DataFrame preprocesado:")
    #st.write(df)  # Punto de depuración para verificar el DataFrame preprocesado

    # Filtrar los datos
    filtered_df = filtrar_datos(df)
    #st.write("DataFrame filtrado:")
    #st.write(filtered_df)  # Punto de depuración para verificar el DataFrame filtrado

    # Obtener estadísticas descriptivas
    stats = obtener_estadisticas(filtered_df)
    #st.write("Estadísticas descriptivas:")
    #st.write(stats)  # Punto de depuración para verificar las estadísticas descriptivas

    # Dividir la interfaz en columnas
    col1, col2 = st.columns([0.65, 0.35])

    # Gráfico de dispersión en col1
    with col1:
        st.subheader('Gráfico de dispersión')
        grafico_dispersion(filtered_df)

    # Gráfico de barras en col1
    with col1:
        st.subheader('Gráfico de barras')
        grafico_barras(filtered_df)

    # Estadísticas descriptivas en col2
    with col2:
        st.subheader('Estadísticas descriptivas')
        st.write(stats)

