'''
BLOQUE 1
'''
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import folium
from streamlit_folium import folium_static

# BLOQUE 1

def show_kpi_5():
    st.title("KPI")


    # Cargar los dataframes
    df = pd.read_csv('regiones_chile_categorias.csv')
    df_po = pd.read_csv('regiones_chile.csv')

    
    # Renombrar las columnas en df_po
    df_po.rename(columns={'Latitud': 'latitud_C', 'Longitud': 'longitud_C'}, inplace=True)

    # Renombrar las columnas en df
    df.rename(columns={'longitud': 'longitud_po', 'latitud': 'latitud_po'}, inplace=True)

    
    
        
       
    '''
    FILTER
    '''
    
    '''
    BLOQUE 2
    '''
    def show_map(region_seleccionada, fecha_inicio, fecha_fin,df_po, df):
            '''
            FILTER
            '''
            # Seleccionar una región
            #region_seleccionada = st.selectbox("Selecciona una región", regiones)
            
            '''
            # Punto de depuración 1: Verificar que los dataframes se carguen correctamente
            st.write("Dataframe df:")
            st.write(df)
            st.write("Dataframe df_po:")
            st.write(df_po)
            '''
            # Filtrar los epicentros por región en df_po
            df_region_seleccionada = df_po[df_po['Region'] == region_seleccionada]
            '''
            # Corregir los campos de latitud y longitud
            st.write(f"Antes de corrección:")
            st.write(df_region_seleccionada[['latitud_C', 'longitud_C']])
            '''
            df_region_seleccionada['latitud_C'] = df_region_seleccionada['latitud_C'].astype(str).str.replace('.', '')
            df_region_seleccionada['longitud_C'] = df_region_seleccionada['longitud_C'].astype(str).str.replace('.', '')
            df_region_seleccionada['latitud_C'] = df_region_seleccionada['latitud_C'].astype(float)
            df_region_seleccionada['longitud_C'] = df_region_seleccionada['longitud_C'].astype(float)
            '''
            # Corregir los campos de latitud y longitud
            st.write(f"Después de corrección:")
            st.write(df_region_seleccionada[['latitud_C', 'longitud_C']])
            st.write(df_region_seleccionada[['latitud_C', 'longitud_C']].dtypes)
            '''
            '''
            FILTER
            '''# Filtrar los epicentros superficiales por fecha
            #fecha_inicio = st.date_input("Fecha de inicio")
            #fecha_fin = st.date_input("Fecha de fin")
            '''
            # Punto de depuración 2: Verificar los valores únicos de 'profundidad_categoria'
            st.write("Valores únicos de 'profundidad_categoria':")
            st.write(df['profundidad_categoria'].unique())
            
            # Punto de depuración 3: Verificar los valores únicos de 'fecha_local'
            st.write("Valores únicos de 'fecha_local':")
            st.write(df['fecha_local'].unique())
            '''
            df_filtrado = df[(df['profundidad_categoria'] == 'Superficial') & df['fecha_local'].between(str(fecha_inicio), str(fecha_fin))]

            '''
            # Depuración para verificar los valores de df_filtrado
            st.write("Valores de df_filtrado:")
            st.write(df_filtrado)
            '''
            
            '''
            BLOQUE MAPA
            '''
            #Función para mostrar el KPI
        
            #latitud = df_region_seleccionada.loc[df_region_seleccionada['Region'] == region_seleccionada, 'latitud_C'].iloc[0]
            #longitud = df_region_seleccionada.loc[df_region_seleccionada['Region'] == region_seleccionada, 'longitud_C'].iloc[0]

            
            # Verificar si la región seleccionada existe en el DataFrame
            if region_seleccionada in df_po['Region'].values:
                df_region_seleccionada = df_po[df_po['Region'] == region_seleccionada]

                # Obtener la latitud utilizando la variable asignada correctamente
                latitud = df_region_seleccionada.loc[df_region_seleccionada['Region'] == region_seleccionada, 'latitud_C'].iloc[0]
                
                # Resto del código
            else:
                # Manejar el caso cuando la región seleccionada no existe en el DataFrame
                print("La región seleccionada no existe en el DataFrame.")
            
            # Punto de depuración: Verificar las coordenadas de la región seleccionada
            #st.write("Latitud de la región seleccionada:", latitud)
            #st.write("Longitud de la región seleccionada:", longitud)

            # Definir las coordenadas de los polígonos de las regiones
            regiones_poligonos = {
                'Santiago': [[-33.65, -71.15], [-33.65, -70.55], [-33.2, -70.55], [-33.2, -71.15]],
                'Valparaíso': [[-32.9, -71.5], [-32.9, -70.9], [-33.4, -70.9], [-33.4, -71.5]],
                'Biobío': [[-36.9, -73.8], [-36.9, -71.5], [-38.3, -71.5], [-38.3, -73.8]],
                'Coquimbo': [[-29.7, -71.8], [-29.7, -70.9], [-30.7, -70.9], [-30.7, -71.8]],
                'Antofagasta': [[-22.2, -69.8], [-22.2, -68.9], [-23.9, -68.9], [-23.9, -69.8]],
                'Araucania': [[-38.6, -72.6], [-38.6, -71.3], [-39.9, -71.3], [-39.9, -72.6]],
                'Tarapaca': [[-18.2, -70.6], [-18.2, -69.3], [-19.4, -69.3], [-19.4, -70.6]],
                'Ohiggins': [[-34.2, -72.5], [-34.2, -70.9], [-35.7, -70.9], [-35.7, -72.5]],
                'Loslagos': [[-40.8, -73.9], [-40.8, -71.5], [-42.3, -71.5], [-42.3, -73.9]],
                'Maule': [[-35.6, -71.8], [-35.6, -70.0], [-36.8, -70.0], [-36.8, -71.8]]
            }

            # Crear el mapa
            mapa = folium.Map(location=[-33.4489, -70.6693], zoom_start=7)

            # Obtener el polígono de la región seleccionada
            poligono = folium.Polygon(
                locations=regiones_poligonos[region_seleccionada],
                color='red',  # Color del borde del polígono
                fill=True,  # Rellenar el polígono
                fill_color='red',  # Color de relleno del polígono
                fill_opacity=0.2  # Opacidad del relleno
            )

            # Agregar el polígono al mapa
            poligono.add_to(mapa)

            # Agregar los marcadores de los epicentros
            for index, row in df_filtrado.iterrows():
                if row['profundidad_categoria'] == 'Superficial':
                    folium.Marker(
                        location=[row['latitud_po'], row['longitud_po']],
                        popup=row['profundidad_categoria'],
                        icon=folium.Icon(color='green', icon='glyphicon glyphicon-map-marker', icon_color='white')
                    ).add_to(mapa)
                else:
                    folium.Marker(
                        location=[row['latitud_po'], row['longitud_po']],
                        popup=row['profundidad_categoria'],
                        icon=folium.Icon(color='blue', icon='glyphicon glyphicon-map-marker', icon_color='white')
                    ).add_to(mapa)

            # Mostrar el mapa en Streamlit
            #st.markdown("### Mapa de Epicentros y Región de Santiago")
            #folium_static(mapa)
            
            
            # Filtrar los epicentros por región en df_po
            df_region_seleccionada = df_po[df_po['Region'] == region_seleccionada]
            '''
            # Corregir los campos de latitud y longitud
            st.write(f"Antes de corrección:")
            st.write(df_region_seleccionada[['latitud_C', 'longitud_C']])
            '''
            df_region_seleccionada['latitud_C'] = df_region_seleccionada['latitud_C'].astype(str).str.replace('.', '')
            df_region_seleccionada['longitud_C'] = df_region_seleccionada['longitud_C'].astype(str).str.replace('.', '')
            df_region_seleccionada['latitud_C'] = df_region_seleccionada['latitud_C'].astype(float)
            df_region_seleccionada['longitud_C'] = df_region_seleccionada['longitud_C'].astype(float)
            '''
            # Corregir los campos de latitud y longitud
            st.write(f"Después de corrección:")
            st.write(df_region_seleccionada[['latitud_C', 'longitud_C']])
            st.write(df_region_seleccionada[['latitud_C', 'longitud_C']].dtypes)
            
            # Punto de depuración 2: Verificar los valores únicos de 'profundidad_categoria'
            st.write("Valores únicos de 'profundidad_categoria':")
            st.write(df['profundidad_categoria'].unique())
            
            # Punto de depuración 3: Verificar los valores únicos de 'fecha_local'
            st.write("Valores únicos de 'fecha_local':")
            st.write(df['fecha_local'].unique())
            '''
            
            df_filtrado = df[(df['profundidad_categoria'] == 'Superficial') & df['fecha_local'].between(str(fecha_inicio), str(fecha_fin))]
            '''
            # Depuración para verificar los valores de df_filtrado
            st.write("Valores de df_filtrado:")
            st.write(df_filtrado)
            '''
            
            latitud = df_region_seleccionada.loc[df_region_seleccionada['Region'] == region_seleccionada, 'latitud_C'].iloc[0]
            longitud = df_region_seleccionada.loc[df_region_seleccionada['Region'] == region_seleccionada, 'longitud_C'].iloc[0]

            
            
            # Definir las coordenadas de los polígonos de las regiones
            regiones_poligonos = {
                'Santiago': [[-33.65, -71.15], [-33.65, -70.55], [-33.2, -70.55], [-33.2, -71.15]],
                'Valparaíso': [[-32.9, -71.5], [-32.9, -70.9], [-33.4, -70.9], [-33.4, -71.5]],
                'Biobío': [[-36.9, -73.8], [-36.9, -71.5], [-38.3, -71.5], [-38.3, -73.8]],
                'Coquimbo': [[-29.7, -71.8], [-29.7, -70.9], [-30.7, -70.9], [-30.7, -71.8]],
                'Antofagasta': [[-22.2, -69.8], [-22.2, -68.9], [-23.9, -68.9], [-23.9, -69.8]],
                'Araucania': [[-38.6, -72.6], [-38.6, -71.3], [-39.9, -71.3], [-39.9, -72.6]],
                'Tarapaca': [[-18.2, -70.6], [-18.2, -69.3], [-19.4, -69.3], [-19.4, -70.6]],
                'Ohiggins': [[-34.2, -72.5], [-34.2, -70.9], [-35.7, -70.9], [-35.7, -72.5]],
                'Loslagos': [[-40.8, -73.9], [-40.8, -71.5], [-42.3, -71.5], [-42.3, -73.9]],
                'Maule': [[-35.6, -71.8], [-35.6, -70.0], [-36.8, -70.0], [-36.8, -71.8]]
            }


            # Crear el mapa
            mapa = folium.Map(location=[-33.4489, -70.6693], zoom_start=7)
            
           
            # Mostrar el mapa en Streamlit
            #st.markdown(mapa._repr_html_(), unsafe_allow_html=True)


            # Obtener el polígono de la región seleccionada
            poligono = folium.Polygon(
                locations=regiones_poligonos[region_seleccionada],
                color='red',  # Color del borde del polígono
                fill=True,  # Rellenar el polígono
                fill_color='red',  # Color de relleno del polígono
                fill_opacity=0.2  # Opacidad del relleno
            )

            # Agregar el polígono al mapa
            poligono.add_to(mapa)

            # Agregar los marcadores de los epicentros
            for index, row in df_filtrado.iterrows():
                if row['profundidad_categoria'] == 'Superficial':
                    folium.Marker(
                        location=[row['latitud_po'], row['longitud_po']],
                        popup=row['profundidad_categoria'],
                        icon=folium.Icon(color='green', icon='glyphicon glyphicon-map-marker', icon_color='white')
                    ).add_to(mapa)
                else:
                    folium.Marker(
                        location=[row['latitud_po'], row['longitud_po']],
                        popup=row['profundidad_categoria'],
                        icon=folium.Icon(color='blue', icon='glyphicon glyphicon-map-marker', icon_color='white')
                    ).add_to(mapa)


            '''
            BLOQUE MAPA
            '''
            # Mostrar el mapa en Streamlit        
            # Construir el título con el valor seleccionado
            titulo = "Mapa de Epicentros Region " + region_seleccionada
            # Mostrar el mapa en Streamlit con el título dinámico
            st.markdown(f"### {titulo}")        
            folium_static(mapa)
            
            # Punto de depuración: Verificar las coordenadas de la región seleccionada
            st.write("Latitud de la región seleccionada:", latitud)
            st.write("Longitud de la región seleccionada:", longitud)
            
            '''
            # Punto de depuración 1
            st.write("Valores de df_filtrado:")
            st.write(df_filtrado)
            '''
            
            # Verificar si hay datos en el dataframe filtrado
            if not df_filtrado.empty:
                '''
                st.write("Valores de df_filtrado:")
                st.write(df_filtrado)
                '''
                ocurrencias = df['profundidad_categoria'].value_counts()
                st.write("Cantidad de ocurrencias por categoría de profundidad:")
                st.write(ocurrencias)

                total_categorias = ocurrencias.sum()
                promedio_superficial = round(ocurrencias.get("Superficial", 0) / total_categorias * 100, 2)
                st.write("KPI Promedio Profundidad Superficial =", promedio_superficial, "%")

                        

            else:
                st.write("No se encontraron datos para el filtro aplicado.")


    def show_filters():
        
            
            # Seleccionar una región
            region_seleccionada = st.selectbox("Selecciona una región", regiones)

            # Filtrar los epicentros por fecha
            fecha_inicio = st.date_input("Fecha de inicio")
            fecha_fin = st.date_input("Fecha de fin")

            return region_seleccionada, fecha_inicio, fecha_fin
    

    def main():
        # Título de la aplicación
        st.title("Mi Aplicación")

        # Definir la estructura con container
        col1, col2 = st.beta_columns([0.4, 0.6])

        # Contenido de la primera columna
        with col1:
            st.write("KPI Promedio Profundidad Superficial = {:.2f} %".format(kpi_promedio_profundidad_superficial))
            st.markdown("### Mapa de Epicentros y Región de Santiago")
            folium_static(mapa)

        # Contenido de la segunda columna
        with col2:
            regiones = df_po['Region'].unique()
            st.write('Conclusion')

        # Definir la estructura con container para el footer
        col3, col4 = st.beta_columns([0.4, 0.6])

        # Contenido de la tercera columna (footer)
        with col3:
            # Contenido de la tercera columna del footer
            st.write('Conclusion')
        # Contenido de la cuarta columna (footer)
        with col4:
            # Contenido de la cuarta columna del footer
            st.write('Conclusion')
    
    # Iniciar la aplicación
    if __name__ == "__main__":
        main()
        
    '''
    LLAMADA FUNCIONES
    '''

    #Llamada a la función show_filters() para obtener los valores seleccionados
    region_seleccionada, fecha_inicio, fecha_fin = show_filters()
        
    # Ejecutar la función para mostrar el KPI
    show_map(region_seleccionada, fecha_inicio, fecha_fin, df_po, df)        
