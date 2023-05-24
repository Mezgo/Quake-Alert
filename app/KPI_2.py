import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
from datetime import timedelta
import seaborn as sns

def cargar_estilos():
        with open('app/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
def show_kpi_2():
    #st.title("KPI 2")
    
    cargar_estilos()
    
    # Funciones
    df = pd.read_csv('data/chile_poblacion_es.csv')
    
    st.write(df.columns)

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

    # Convertir la columna 'fecha_local' a tipo datetime
    df['fecha_local'] = pd.to_datetime(df['fecha_local'])

    # Convertir la columna 'hora_local' a tipo datetime y formatearla a horas y minutos
    df['hora_local'] = pd.to_datetime(df['hora_local']).dt.strftime('%H:%M')

    # Crear la columna 'fechaHora' concatenando las columnas 'fecha_local' y 'hora_local'
    df['fechaHora'] = df['fecha_local'].astype(str) + ' ' + df['hora_local']

    # Verificar el resultado
    print(df['fechaHora'])

    

    df['fechaHora'] = pd.to_datetime(df['fechaHora'])
    # Ordenar el DataFrame por la columna 'fecha_hora'
    df = df.sort_values('fechaHora')

    # Calcular la diferencia de tiempo entre filas consecutivas
    df['diferencia_tiempo'] = df['fechaHora'].diff()

    # Mostrar el DataFrame resultante
    df

    df_dif = df.copy()
    filtered_df = df_dif[(df_dif['magnitud'] > 6) & (df_dif['profundidad'] < 70)]
    filtered_df['dif_tiempo'] = filtered_df['fechaHora'].diff()
    filtered_df

    '''
    ***************FIN CARGA DATOS
    '''


    """Graficamos """

    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    x = df['magnitud']
    y = df['dif_tiempo'].dt.days
    plt.xlabel('Magnitud')
    plt.ylabel('Días desde el último sismo')
    plt.title('Relación entre Magnitud y Días desde el último sismo')
    plt.xlim(0, 8.5)
    plt.ylim(0, 20)
    plt.scatter(x, y)
    



    # Código Streamlit

    # Cargar y preprocesar los datos
    #df = cargar_datos()
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


    '''
    SECCION LOGO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
            col1.image('logo.PNG')
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
        st.markdown("<h1 style='font-size: 30px;'>KPI: Confirmacion o no de un mito</h1>", unsafe_allow_html=True)
        '''
        GRAFICO
        '''
        #st.subheader('Gráfico de barras')
        plt.show()
    with col2:
        st.empty()
    with col3:
        st.subheader('Estadísticas descriptivas')
        st.write(stats)
        
    
    '''
    SECCION FOOTER
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown('<div class="EMPTY_footer"></div>', unsafe_allow_html=True)
        col1.image('logo_footer.png')
    with col2:
        st.empty()


