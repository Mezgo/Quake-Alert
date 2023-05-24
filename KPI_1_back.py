import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#from app import carga
#from app.carga import *

def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
            #st.markdown('<link href="style.css" rel="stylesheet">', unsafe_allow_html=True)


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
    
    ax.set_xticklabels(etiquetas_magnitud)

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
    cargar_estilos()
    '''
    SECCION LOGO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
            col1.image('logo.png')
    with col2: 
            st.empty()


    # Obtener las fechas mínima y máxima del DataFrame
    fecha_min = pd.to_datetime(df['fecha_local']).min().date()
    fecha_max = pd.to_datetime(df['fecha_local']).max().date()

    '''
    SECCION KPI
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        
        # Definir las fechas de inicio y fin predeterminadas
        fecha_inicio_default = datetime(2023, 1, 1)
        fecha_fin_default = datetime(2023, 5, 9)

        # Obtener el rango de fechas seleccionado por el usuario
        fecha_inicio, fecha_fin = st.slider(
            "Selecciona un rango de fechas:",
            value=(fecha_inicio_default, fecha_fin_default),
            format="YYYY-MM-DD"  # Cambio de formato a "YYYY-MM-DD"
        )

        # Convertir las fechas de inicio y fin a formato datetime
        fecha_inicio = pd.to_datetime(fecha_inicio)
        fecha_fin = pd.to_datetime(fecha_fin)
        
        df_filtrado = df[(pd.to_datetime(df['fecha_local']).dt.date >= fecha_inicio.date()) &
                 (pd.to_datetime(df['fecha_local']).dt.date <= fecha_fin.date())]


        '''
        st.markdown("<h1 style='font-size: 30px;'>KPI 1: Distribución de sismos por categoría de magnitud</h1>", unsafe_allow_html=True)
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
            
            
         df_filtrado = df[(pd.to_datetime(df['fecha_local']).dt.date >= fecha_inicio) &
                  (pd.to_datetime(df['fecha_local']).dt.date <= fecha_fin)]
   
        '''
        
    with col2:
        st.empty()
    with col3:
        st.empty()
    
        fig = generar_grafico(df_filtrado)

        # Obtener el conteo de sismos por categoría de magnitud
        magnitud_counts = df_filtrado['magnitud_categoria'].value_counts()
        total_sismos = magnitud_counts.sum()

        # Calcular los porcentajes de cada categoría
        porcentajes = magnitud_counts / total_sismos * 100

        # Obtener la categoría con el porcentaje mayor
        categoria_mayor = porcentajes.idxmax()
        porcentaje_mayor = porcentajes.max()
        
    '''
    SECCION CUERPO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown("<h1 style='font-size: 30px;'>KPI 1: Distribución de sismos por categoría de magnitud</h1>", unsafe_allow_html=True)
        
        
        css = """
        .card {
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        """
        # Estilo personalizado CSS para resaltar la tarjeta
        
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

        # Mostrar el KPI utilizando st.markdown() y las clases CSS definidas
        st.markdown(
            f"""
            <div class="card">
                <h2 class="kpi-title">KPI: Categoría con mayor porcentaje</h2>
                <h1 class="kpi-value">{porcentaje_mayor:.2f}%</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        #st.subheader('KPI: Categoría con mayor porcentaje')
        #st.write(f"Categoría: {categoria_mayor}, Porcentaje: {porcentaje_mayor:.2f}%")
        
        #st.subheader('Gráfico de Barras')
        fig = generar_grafico(df_filtrado)
        st.pyplot(fig)
        
    with col2:
        st.empty()
    with col3:
        st.empty()
        st.subheader('Porcentajes de las categorías de magnitud')
        #st.dataframe(porcentajes)
        
        # Convertir la Serie porcentajes en un DataFrame
        df_porcentajes = porcentajes.to_frame()

        # Define una función que aplique el formato deseado al valor máximo
        def highlight_max(value):
            if value == porcentaje_mayor:
                return 'background-color: yellow'
            else:
                return ''

        #styled_df_porcentajes = df_porcentajes.style.applymap(highlight_max)
        # Aplicar el formato al DataFrame usando el método style.applymap()
        styled_df_porcentajes = df_porcentajes.style.applymap(highlight_max).set_properties(**{'width': '300px','height': '350px'})
        # Muestra el DataFrame estilizado
        st.dataframe(styled_df_porcentajes)
        
        
        # Utilizar la clase CSS en el elemento
        st.markdown('<div class="espacio_conclusion"></div>', unsafe_allow_html=True)
        st.write('<div class="cuerpo_titulo">Conclusion</div>', unsafe_allow_html=True)
        
        st.markdown(
            '<div class="texto_conclusion">En este KPI primero se discretizan los valores de magnitud de los sismos en 7 categorias segun valores de la columna magnitud ⚠️Ligero,⚠️Moderado,⚠️Menor,⚠️Fuerte,⚠️Micro,⚠️Mayor,⚠️Gran, segun una fecha seleccionada se muestran los porcentajes de estos valores teniendo en cuenta la categoria que mas prevalece y tiene mayor frecuencia en el pais de Chile  </div>', 
            unsafe_allow_html=True
            )
        
    '''
    # Mostrar el gráfico de barras en la columna 1
    with col1:
        

    # Mostrar los porcentajes de cada categoría y el dato KPI
    with col2:
    '''
        

    
    '''
    SECCION FOOTER
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown('<div class="EMPTY_footer"></div>', unsafe_allow_html=True)
        col1.image('logo_footer.png')
    with col2:
        st.empty()
