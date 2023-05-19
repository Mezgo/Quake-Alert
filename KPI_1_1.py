import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def generar_grafico(df):
    """
    Genera un gráfico de barras que muestra la distribución de sismos por categoría de magnitud.

    Args:
        df (DataFrame): DataFrame que contiene los datos de los sismos.

    Returns:
        fig (Figure): Figura del gráfico generado.
    """
    # Definir los rangos y etiquetas de las categorías de magnitud
    rangos_magnitud = [0, 2.0, 3.9, 4.9, 5.9, 6.9, 7.9, float('inf')]
    etiquetas_magnitud = ['Micro', 'Menor', 'Ligero', 'Moderado', 'Fuerte', 'Mayor', 'Gran']

    # Crear una columna 'magnitud_categoria' en el DataFrame, que asigna una categoría de magnitud a cada sismo
    df['magnitud_categoria'] = pd.cut(df['magnitud'], bins=rangos_magnitud, labels=etiquetas_magnitud, right=False)

    # Contar la cantidad de sismos por categoría de magnitud
    kpi_data = df['magnitud_categoria'].value_counts().reset_index()
    kpi_data.columns = ['Categoría de Magnitud', 'Cantidad de Sismos']

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(kpi_data['Categoría de Magnitud'], kpi_data['Cantidad de Sismos'])
    ax.set_xlabel('Categoría de Magnitud')
    ax.set_ylabel('Cantidad de Sismos')
    ax.set_title('Distribución de Sismos por Categoría de Magnitud')
    plt.xticks(rotation=45)

    return fig


def show_kpi_1():
    """
    Muestra el KPI 1: Distribución de sismos por categoría de magnitud.
    Permite filtrar los sismos por fecha y muestra un gráfico de barras con la distribución resultante.
    """
    st.title("KPI 1: Distribución de sismos por categoría de magnitud")

    # Cargar los datos
    df = pd.read_csv('chile.csv')

    # Obtener las fechas mínima y máxima del DataFrame
    fecha_min = pd.to_datetime(df['fecha_local']).min().date()
    fecha_max = pd.to_datetime(df['fecha_local']).max().date()

    # Mostrar los selectores de fecha en la columna 2
    col1, col2 = st.columns([0.6, 0.4])

    with col2:
        st.subheader('Filtrar por Fecha')

        # Mostrar el selector de fecha de inicio con una clave única 'fecha_inicio_selector'
        fecha_inicio = st.date_input('Fecha de inicio', value=fecha_min, min_value=fecha_min, max_value=fecha_max, key='fecha_inicio_selector')

        # Mostrar el selector de fecha de fin con una clave única 'fecha_fin_selector'
        fecha_fin = st.date_input('Fecha de fin', value=fecha_max, min_value=fecha_min, max_value=fecha_max, key='fecha_fin_selector')

        if fecha_inicio > fecha_fin:
            st.error('La fecha de inicio no puede ser posterior a la fecha de fin.')
            return

    # Filtrar el DataFrame según las fechas seleccionadas
    df_filtrado = df[(pd.to_datetime(df['fecha_local']).dt.date >= pd.Timestamp(fecha_inicio)) &
                     (pd.to_datetime(df['fecha_local']).dt.date <= pd.Timestamp(fecha_fin))]

    # Mostrar el gráfico de barras en la columna 1
    with col1:
        st.subheader('Gráfico de Barras')
        fig = generar_grafico(df_filtrado)
        st.pyplot(fig)


