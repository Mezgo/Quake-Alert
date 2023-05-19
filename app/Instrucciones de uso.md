# Instrucciones usar de forma correcta el modulo _carga_

## Preparar entorno

1. Instalar las dependencias del proyecto

    ```shell
    pip install -r requirements.txt
    ```

2. Seguir las instrucciones de instalacion de la linea de comandos de Google Cloud -> [link](https://cloud.google.com/sdk/docs/install?hl=es-419#installation_instructions)

3. Inicializar el CLI

    ```shell
    gcloud init
    ```

## Funciones

> __IMPORTANTE__: correr la funcion _`autenticar()`_ para acceder al proyecto

- Para extraer de fuente y subir datos crudos

    ```python
    llenar_bucket()
    ```

- Para limpiar los datos del punto anterior y subir nuevos archivos limpios

    ```python
    limpieza_japon()
    limpieza_chile()
    limpieza_eeuu()
    ```

- Para extraer los datos limpios del bucket

    ```python
    get_japon_limpio()
    get_chile_limpio()
    get_eeuu_limpio()
    ```
