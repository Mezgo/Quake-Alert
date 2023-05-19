import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import KPI_1
import KPI_2
import KPI_3
import KPI_4
import KPI_5

 # Crear un DataFrame de ejemplo
data = pd.read_csv('chile.csv')
df = pd.DataFrame(data)
    
# Configurar la página
st.set_page_config(
    page_title="Alerta sísmica Chile",
    page_icon="🌎",
    layout="wide"    
)

# Mostrar la imagen en el encabezado
st.markdown(
    """
    <div>
        <img src="https://github.com/Mezgo/Quake-Alert/blob/Dibujos/imagenes/logo_slogan.PNG" style="width: 200px; margin-bottom: 20px;">
    </div>
    """,
    unsafe_allow_html=True
)


# Opciones del menú de navegación
menu = ["Inicio", "KPI 1", "KPI 2", "KPI 3", "KPI 4", "KPI 5"]
choice = st.sidebar.selectbox("Menú de navegación", menu)

# Mostrar contenido según la opción seleccionada
if choice == "Inicio":
    st.title("PROYECTO ANALISIS SISMOS")
    # Mostrar contenido de la página de inicio
    import matplotlib.pyplot as plt

    # Crear dos columnas con proporciones 60% y 40%
    col1, col2 = st.columns([0.5, 0.5])

    # Texto en la columna izquierda
    with col1:        
        st.write("Quienes somos:")
        st.write("Somos parte del equipo de Prevención de eventos sísmicos de la ONG 'Quake Alert' de Chile e integramos el departamento de ciencia de datos y machine learning de la misma.")
        st.write("Somos un grupo de profesionales altamente capacitados, utilizamos herramientas tecnológicas para poder brindar soluciones innovadoras en la prevención de desastres de eventos sísmicos. Los datos aportan mucha información, es por eso que nos esforzamos por interpretar qué es lo que la ONG realmente necesita y proporcionar soluciones innovadoras y personalizadas.")

    # Gráfico en la columna derecha
    with col2:
        # Crear la figura de Matplotlib
        fig = plt.figure(figsize=(8, 4))
        ax = fig.add_subplot(111)

        # Generar el histograma
        n, bins, patches = ax.hist(df['magnitud'], bins=20)

        # Personalizar la apariencia del histograma
        for patch in patches:
            patch.set_facecolor('#4287f5')
            patch.set_edgecolor('white')
            patch.set_linewidth(0.5)

        # Agregar etiquetas y título al gráfico
        ax.set_xlabel('Magnitud')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Distribución de Magnitudes en Chile')

        # Personalizar el fondo y la cuadrícula
        ax.set_facecolor('#f5f5f5')
        ax.grid(color='white')

        # Mostrar la figura en Streamlit
        st.pyplot(fig)
        
    # Estilo CSS para el footer
    footer_style = """
            text-align: center;
            background-color: #f5f5f5;
            margin:30px;
            padding: 50px;
            color: #777777;
        """

        # Contenido del footer
    footer_text = "Quake Alert ONG Prevención eventos sísmicos"

        # Agregar el footer a tu aplicación
    st.markdown(f'<p style="{footer_style}">{footer_text}</p>', unsafe_allow_html=True)    
        
        
elif choice == "KPI 1":
    KPI_1.show_kpi_1()

elif choice == "KPI 2":
    KPI_2.show_kpi_2()

elif choice == "KPI 3":
    st.write("Antes de llamar a KPI_3.show_kpi_3()")
    KPI_3.show_kpi_3()
    st.write("Después de llamar a KPI_3.show_kpi_3()")
    
elif choice == "KPI 4":
    KPI_4.show_kpi_4()
    
elif choice == "KPI 5":
    KPI_5.show_kpi_5()