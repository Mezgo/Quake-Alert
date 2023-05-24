import pyperclip

def copiar_codigo_con_numeros_linea(ruta_archivo_fuente):
    # Leer el archivo fuente
    with open(ruta_archivo_fuente, "r") as archivo_fuente:
        lineas = archivo_fuente.readlines()

    # Crear una cadena con el código y los números de línea
    codigo_con_numeros_linea = ""
    for i, linea in enumerate(lineas, start=1):
        codigo_con_numeros_linea += f"{i}: {linea}"

    # Copiar al portapapeles
    pyperclip.copy(codigo_con_numeros_linea)

    # Imprimir el mensaje de éxito
    print("Código con números de línea copiado al portapapeles.")

# Ruta del archivo que deseas copiar al portapapeles
ruta_archivo_fuente = "KPI_1.py"

# Llamar a la función para copiar el código con números de línea al portapapeles
copiar_codigo_con_numeros_linea(ruta_archivo_fuente)
