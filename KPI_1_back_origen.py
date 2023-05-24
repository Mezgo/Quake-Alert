import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#from app import carga
#from app.carga import *

def cargar_estilos():
    st.markdown('<link href="style.css" rel="stylesheet">', unsafe_allow_html=True)


# Cargar los datos
def cargar_datos():
    # Cargar los datos desde el archivo CSV
    df = pd.read_csv('chile.csv')
    return df

df = cargar_datos()


#df = get_chile_limpio()

def generar_grafico(df):
    rangos_magnitud = [0, 2.0, 3.9, 4.9, 5.9, 6.9, 7.9, float('inf')]
    etiquetas_magnitud = ['Micro', 'Menor', 'Ligero', 'Moderado', 'Fuerte', 'Mayor', 'Gran']

    df['magnitud_categoria'] = pd.cut(df['magnitud'], bins=rangos_magnitud, labels=etiquetas_magnitud, right=False)

    fig, ax = plt.subplots()

    # Generar Gráfico de barras
    magnitud_counts = df['magnitud_categoria'].value_counts()
    magnitud_counts = magnitud_counts.reindex(etiquetas_magnitud)
    magnitud_counts.plot(kind='bar', ax=ax, alpha=0.7)

    #ax.set_xlabel('Categoría de Magnitud')
    ax.set_ylabel('Cantidad de Sismos')
    ax.set_title('Distribución de Sismos por Categoría de Magnitud')

    return fig


def show_kpi_1():
    """
    Muestra el KPI 1: Distribución de sismos por categoría de magnitud.
    Permite filtrar los sismos por fecha y muestra un gráfico de barras con la distribución resultante,
    junto con los porcentajes de las categorías y el dato KPI correspondiente.
    """
    st.markdown("<h1 style='font-size: 30px;'>KPI 1: Distribución de sismos por categoría de magnitud</h1>", unsafe_allow_html=True)


    # Obtener las fechas mínima y máxima del DataFrame
    fecha_min = pd.to_datetime(df['fecha_local']).min().date()
    fecha_max = pd.to_datetime(df['fecha_local']).max().date()

    # Mostrar los selectores de fecha en la columna 2
    col1, col2 = st.columns([0.6, 0.4])

    with col2:
        st.subheader('Rango de Fechas')

        # Mostrar el selector de fecha de inicio con una clave única 'fecha_inicio_selector'
        fecha_inicio = st.date_input('Fecha de inicio', value=fecha_min, min_value=fecha_min, max_value=fecha_max,
                                     key='fecha_inicio_selector')

        # Mostrar el selector de fecha de fin con una clave única 'fecha_fin_selector'
        fecha_fin = st.date_input('Fecha de fin', value=fecha_max, min_value=fecha_min, max_value=fecha_max,
                                  key='fecha_fin_selector')

        if fecha_inicio > fecha_fin:
            st.error('La fecha de inicio no puede ser posterior a la fecha de fin.')
            return

        # Filtrar el DataFrame según las fechas seleccionadas
        
        
        #df_filtrado = df[(pd.to_datetime(df['fecha_local']).dt.date >= pd.Timestamp(fecha_inicio)) &
        #          (pd.to_datetime(df['fecha_local']).dt.date <= pd.Timestamp(fecha_fin))]
        
        df_filtrado = df[(pd.to_datetime(df['fecha_local']).dt.date >= fecha_inicio) &
                  (pd.to_datetime(df['fecha_local']).dt.date <= fecha_fin)]


    # Mostrar el gráfico de barras en la columna 1
    with col1:
        st.subheader('Gráfico de Barras')
        fig = generar_grafico(df_filtrado)
        st.pyplot(fig)

        # Obtener el conteo de sismos por categoría de magnitud
        magnitud_counts = df_filtrado['magnitud_categoria'].value_counts()
        total_sismos = magnitud_counts.sum()

        # Calcular los porcentajes de cada categoría
        porcentajes = magnitud_counts / total_sismos * 100

        # Obtener la categoría con el porcentaje mayor
        categoria_mayor = porcentajes.idxmax()
        porcentaje_mayor = porcentajes.max()

    # Mostrar los porcentajes de cada categoría y el dato KPI
    with col2:
        st.subheader('Porcentajes de las categorías de magnitud')
        st.dataframe(porcentajes)
        st.subheader('KPI: Categoría con mayor porcentaje')
        st.write(f"Categoría: {categoria_mayor}, Porcentaje: {porcentaje_mayor:.2f}%")


    