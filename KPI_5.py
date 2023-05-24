import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from datetime import datetime
import os

def show_kpi_5():
    
    def cargar_estilos():
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
            st.markdown('<link href="style.css" rel="stylesheet">', unsafe_allow_html=True)

    
    # Punto de depuración para verificar la carga de style.css
    cargar_estilos()
    
    
    def cargar_dataframes():
        # Cargar los dataframes
        df = pd.read_csv('regiones_chile_categorias.csv', delimiter=',')
        df_po = pd.read_csv('regiones_chile.csv', delimiter=',')
        # Convertir la columna 'fecha_local' a objetos datetime
        df['fecha_local'] = pd.to_datetime(df['fecha_local'])
        
        '''
        st.write("Columnas en df:")
        st.write(df.columns)  # Punto de depuración: Imprimir las columnas en df

        st.write("Columnas en df_po:")
        st.write(df_po.columns)  # Punto de depuración: Imprimir las columnas en df_po
        '''
        
        # Renombrar las columnas en df_po
        df_po.rename(columns={'Latitud': 'latitud_C', 'Longitud': 'longitud_C'}, inplace=True)

        # Renombrar las columnas en df
        df.rename(columns={'longitud': 'longitud_po', 'latitud': 'latitud_po'}, inplace=True)

        return df, df_po

    

    '''
    SELECCION DE REGION
    '''
    def select_region(regiones):
        region_seleccionada = st.selectbox("Selecciona una región:", regiones)
        return region_seleccionada
    
    '''
    SELECCION DE FECHAS
    '''
    def select_dates():
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

        return fecha_inicio, fecha_fin



    def definir_coordenadas_poligonos():
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
        return regiones_poligonos


    def show_map(df, df_po, region_seleccionada, fecha_inicio, fecha_fin):
        
        regiones_poligonos = definir_coordenadas_poligonos()
        
        '''
        FILTROS
        '''
        # Filtrar los epicentros por región seleccionada
        df_region_seleccionada = df_po[df_po['Region'] == region_seleccionada]

        '''
        st.write("Columnas en df_region_seleccionada:")
        st.write(df_region_seleccionada.columns)  # Punto de depuración: Imprimir las columnas en df_region_seleccionada
        '''
        
        # Verificar si 'fecha_local' está presente en df
        if 'fecha_local' not in df.columns:
            st.error("La columna 'fecha_local' no está presente en df.")
            return
        
       # Convertir las fechas de inicio y fin a formato datetime
        #fecha_inicio = pd.to_datetime(fecha_inicio)
        #fecha_fin = pd.to_datetime(fecha_fin)
        
        # Convertir las fechas de inicio y fin a objetos datetime
        fecha_inicio = datetime.combine(fecha_inicio, datetime.min.time())
        fecha_fin = datetime.combine(fecha_fin, datetime.max.time())

        # Filtrar los epicentros por fecha y categoría de profundidad utilizando df_po
        #df_filtered = df[(df['profundidad_categoria'] == 'Superficial') & (df['fecha_local'] >= fecha_inicio) & (df['fecha_local'] <= fecha_fin)]
        df_fecha_filtered = df[(df['fecha_local'] >= fecha_inicio) & (df['fecha_local'] <= fecha_fin)]
        #st.write("Resultado del filtrado por fecha:")
        #st.write(df_fecha_filtered)

        df_filtered = df_fecha_filtered[df_fecha_filtered['profundidad_categoria'] == 'Superficial']
        #st.write("Resultado del filtrado por fecha y categoría:")
        #st.write(df_filtered)


        '''
        st.write("Columnas en df_filtered:")
        st.write(df_filtered.columns)  # Punto de depuración: Imprimir las columnas en df_filtered
        '''
        
        '''
        MAPA
        '''
        # Crear el mapa utilizando la biblioteca folium
        mapa = folium.Map(location=[-33.45, -70.65], zoom_start=9)

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

        '''
        # Agregar marcadores para los epicentros filtrados
        for index, row in df_filtered.iterrows():
            folium.Marker(location=[row['latitud_po'], row['longitud_po']]).add_to(mapa)
        
        # Mostrar el mapa en Streamlit
        folium_static(mapa)
        '''
        # Agregar marcadores para los epicentros filtrados
        for index, row in df_filtered.iterrows():
            # Crear un objeto Marker personalizado
            marker = folium.Marker(
                location=[row['latitud_po'], row['longitud_po']],
                icon=folium.Icon(color='blue', icon='info-sign', prefix='fa'),  # Personalizar el ícono del marcador
                popup=f"Ubicación: {row['latitud_po']}, {row['longitud_po']}"  # Personalizar el contenido emergente del marcador
            )
            marker.add_to(mapa)

        # Personalizar el estilo del mapa
        #mapa.get_root().header.add_child(folium.Element('<style>.mapouter{position:relative;text-align:right;height:500px;width:900px;}</style>'))
        
        # Mostrar el mapa en Streamlit
        folium_static(mapa)

    def calcular_promedios(df, fecha_inicio, fecha_fin):
        # Filtrar el DataFrame por fecha
        df_filtrado = df[(df['fecha_local'] >= fecha_inicio) & (df['fecha_local'] <= fecha_fin)]
        
        ocurrencias = df_filtrado['profundidad_categoria'].value_counts()
        total_categorias = ocurrencias.sum()
        promedios = {}

        for categoria, count in ocurrencias.items():
            promedio = round(count / total_categorias * 100, 2)
            promedios[categoria] = promedio

        # Calcular el promedio de la categoría "superficial"
        promedio_superficial = df_filtrado[df_filtrado['profundidad_categoria'] == 'Superficial']['profundidad'].mean()

        return promedios, promedio_superficial

    
        # Aplicar los estilos en la interfaz
        st.markdown(f'<style>{estilos}</style>', unsafe_allow_html=True)


    def mostrar_interfaz(df, df_po):
        # Llamar a la función definir_estilos() para aplicar los estilos personalizados
        df, df_po = cargar_dataframes()
        cargar_estilos()
        
        regiones = df_po['Region'].unique()
        
        '''
        # Encabezado
        '''
        with st.container():
            col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
            with col1:
                col1.image('logo.png')
            with col2: 
                st.empty()
                #col2.write('Encabezado desde main.py')
        
        '''
        # KPI
        '''
        with st.container():
            col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
            with col1:
                #st.markdown("### Filtros")
                fecha_inicio, fecha_fin = select_dates()
                #fecha_inicio_kpi, fecha_fin_kpi = show_filters(regiones)
            with col2:
                st.empty()
                
            with col3:
                # Utilizar la clase CSS en el elemento
                st.write('<div class="cuerpo_titulo_head">Promedio Categorías Profundidad:</div>', unsafe_allow_html=True)
            
        '''
        # Cuerpo
        '''
        with st.container():
            col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
            with col1:
                #fecha_inicio, fecha_fin = select_dates()
                #promedio_superficial = calcular_promedio_superficial(df, fecha_inicio, fecha_fin)
                promedios, promedio_superficial = calcular_promedios(df, fecha_inicio, fecha_fin)


                # Mostrar los controles de filtros debajo del KPI
                
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
                        <h2 class="kpi-title">KPI Promedio Profundidad Superficial</h2>
                        <h1 class="kpi-value">{promedio_superficial:.2f}%</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                
                #st.write("KPI Promedio Profundidad Superficial =", promedio_superficial, "%")
                #st.metric("Promedio Profundidad Superficial", promedio_superficial, "%")
                #st.markdown("### Mapa de Epicentros y Región de Santiago")
                st.markdown('<div class="encabezado-texto"> Mapa de Epicentros y Región de Santiago</div>', unsafe_allow_html=True)

                '''
                IMPRESION MAPA CON FILTROS
                '''
                # Obtener la región seleccionada a través de un dropdown
                # Obtener la región seleccionada
                region_seleccionada = select_region(regiones)
                
                # Llamar a la función show_filters y asignar los valores retornados
                #show_map(df, df_po, region_seleccionada, fecha_inicio, fecha_fin)
                # Ajustar el ancho del mapa utilizando el atributo width del markdown
                #st.markdown(f'<div class="mapa">{show_map(df, df_po, region_seleccionada, fecha_inicio, fecha_fin)}</div>', unsafe_allow_html=True)
                
                st.markdown(
                    """
                    <style>
                    .mapa {
                        width: 100% !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True)
            
                #st.markdown(f'<div class="mapa">{show_map(df, df_po, region_seleccionada, fecha_inicio, fecha_fin)}</div>', unsafe_allow_html=True)
                st.markdown(f'<div id="#map_cffe5f175db52399f3aa9bf7819dd646.folium-map.leaflet-container.leaflet-touch.leaflet-fade-anim.leaflet-grab.leaflet-touch-drag.leaflet-touch-zoom">{show_map(df, df_po, region_seleccionada, fecha_inicio, fecha_fin)}</div>', unsafe_allow_html=True)

            with col2:
                st.empty()
                
            
            with col3:
                
                '''
                IMPRESION PROMEDIO CATEGORIAS
                '''
                
                df_promedios = pd.DataFrame.from_dict(promedios, orient='index', columns=['Promedio'])
                df_promedios_rounded = df_promedios.round(2)
                df_promedios_formatted = df_promedios_rounded.applymap("{:.2f}%".format)
                #st.dataframe(df_promedios_formatted.style.highlight_max(axis=0), height=300)
                st.table(df_promedios_formatted.style.highlight_max(axis=0).set_properties(**{'width': '300px','height': '350px'}))




                # Utilizar la clase CSS en el elemento
                st.markdown('<div class="espacio_conclusion"></div>', unsafe_allow_html=True)
                st.write('<div class="cuerpo_titulo">Conclusion</div>', unsafe_allow_html=True)
                
                st.markdown(
                    '<div class="texto_conclusion">En este KPI primero se discretizan los valores de profundidad de los sismos en categorias Superficial (<70kms), Intermedio(70-300kms), Profundo(>300kms), estos se relacionan en un mapa para mostrar mediante marcadores los epicentros de categoria Superficial en relacion a una Region de Chile seleccionada y por otro se muestra en una tarjeta destacada el KPI promedio de sismos con Profundidad Superficial, hacemos hincapie en la categoria superficial de los valores mostrados en ambos casos ya que son los que causan mayor daño en los sismos</div>', 
                    unsafe_allow_html=True
                    )

        '''
        # Pie de página
        '''
        
        with st.container():
            col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
            with col1:
                st.markdown('<div class="espacio_footer"></div>', unsafe_allow_html=True)
                col1.image('logo_footer.png')
            with col2:
                st.empty()


   # Cargar los dataframes
    #st.write("Cargando dataframes...")
    df, df_po = cargar_dataframes()
    #st.write("Dataframes cargados con éxito.")

    # Verificar los campos en df
    #st.write("Campos en df:")
    #st.write(df.columns)

    # Mostrar la interfaz
    #st.write("Mostrando la interfaz...")
    mostrar_interfaz(df, df_po)
    #st.write("Interfaz mostrada correctamente.")


