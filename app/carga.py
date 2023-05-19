# Importar librerias
import requests
import pandas as pd
import datetime
import json
import google.auth
from google.cloud import storage
from geopy.geocoders import Nominatim

PROJECT_ID = 'quake-alert-e44c3'
BUCKET = 'buket-geodata'


def authenticate_implicit_with_adc(project_id):
    """
    When interacting with Google Cloud Client libraries, the library can auto-detect the
    credentials to use.

    // TODO(Developer):
    //  1. Before running this sample,
    //  set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable.
    //  3. Make sure that the user account or service account that you are using
    //  has the required permissions. For this sample, you must have "storage.buckets.list".
    Args:
        project_id: The project id of your Google Cloud project.
    """

    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


def autenticar():
    """activa la funcion que autentica al usuaio"""
    authenticate_implicit_with_adc(PROJECT_ID)


client = storage.Client()


class EEUU:

    def history(self):

        history = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2022-01-01%2000:00:00&endtime=2023-05-11%2023:59:59&maxlatitude=50&minlatitude=24.6&maxlongitude=-65&minlongitude=-125&minmagnitude=1&orderby=time-asc'
        history = requests.get(history).json()
        history = pd.json_normalize(history, record_path =['features'])
        history = history.to_json(orient = 'records')
        with open('data/datos_eeuu.json', 'w') as f: f.write(history)

        return f

    def now(self):

        now = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2023-05-12%2000:00:00&maxlatitude=50&minlatitude=24.6&maxlongitude=-65&minlongitude=-125&minmagnitude=1&orderby=time-asc'
        now = requests.get(now).json()
        now = pd.json_normalize(now, record_path=['features'])
        now = now.to_json(orient='records')
        now = json.loads(now)
        now = list(now)
        with open('data/datos_eeuu.json', 'r') as f: history = json.load(f)
        for entry in now:
            if entry != history[-1]:
                history.append(entry)
        history = json.dumps(history)
        with open('data/datos_eeuu.json', 'w') as f: f.write(history)

        return

    def etl(self, df):
        eeuu = pd.read_json('data/datos_eeuu.json')
        columnas = [p.replace('properties.', '') for p in eeuu.columns.to_list()]
        new_names = dict(zip(eeuu.columns.to_list(), columnas))
        eeuu = eeuu.rename(new_names, axis='columns')
        variables = ['type', 'id', 'updated', 'tz', 'url', 'detail', 'felt', 'cdi', 'mmi', 'alert', 'status', 
                'tsunami', 'sig', 'net', 'code', 'ids', 'sources', 'types' , 'nst', 'dmin', 'rms', 
                'gap', 'magType', 'type', 'title', 'geometry.type'] 
        eeuu = eeuu.drop(variables, axis='columns')
        eeuu.rename({'geometry.coordinates':'coordinates'}, axis='columns', inplace=True)
        eeuu[['longitude','latitude', 'depth']] = pd.DataFrame(eeuu.coordinates.tolist(), index= eeuu.index)
        eeuu.drop('coordinates',axis=1, inplace= True)

        def formatear_time(x):
            time = x/1000
            return datetime.datetime.fromtimestamp(time)

        eeuu.time = eeuu.time.apply(formatear_time)
        eeuu['date'] = eeuu.time.dt.date
        eeuu['time_hour'] = eeuu.time.dt.time
        eeuu['time_hour'] = eeuu['time_hour'].apply(lambda x: x.replace(microsecond=0))
        eeuu.drop('time', axis='columns', inplace=True)
        eeuu.rename({'mag':'magnitud', 'time_hour':'hora_local','date':'fecha_local','depth':'profundidad','latitude':'latitud','longitude':'longitud'}, axis='columns', inplace=True)
        def separate_date(row):
            try:
                row.place.split("km")
            except:
                row['distancia'] = 100000
            else:
                row['distancia'] = row.place.split("km")[0]
            return row
        eeuu = eeuu.apply(separate_date, axis=1)
        def replace_as_0(row):
            try:
                int(row['distancia'])
            except:
                row['distancia'] = 100000
            else:
                row['distancia'] = int(row['distancia'])
            return row
        eeuu = eeuu.apply(replace_as_0, axis=1)
        eeuu.drop('place',axis=1,inplace=True)
        def codigo_region(row):
            point = row.latitud,row.longitud
            geolocator = Nominatim(user_agent='Google Maps') 
            location = geolocator.reverse(point)
            try:
                location.raw['address']['ISO3166-2-lvl4']
            except:
                row['codigo_region'] = ' region'
            else:
                location = location.raw['address']['ISO3166-2-lvl4']
                row['codigo_region'] = str(location)
            return row
        eeuu.head.apply(codigo_region, axis=1)
        eeuu = eeuu[['fecha_local','hora_local','magnitud','profundidad','latitud','longitud','distancia','codigo_region']]
        eeuu['fecha_local'] = eeuu['fecha_local'].apply(lambda x: str(x))
        eeuu_json = eeuu.to_json(orient = 'records')
        with open('data/datos_eeuu_etl.json', 'w') as f: f.write(eeuu_json)

        return f


# eeuu = eeuu()


class Chile:

    def history(self):

        history = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2022-01-01%2000:00:00&endtime=2023-05-11%2023:59:59&maxlatitude=-17.5&minlatitude=-56.0&maxlongitude=-66.0&minlongitude=-81.0&minmagnitude=1&orderby=time-asc'
        history = requests.get(history).json()
        history = pd.json_normalize(history, record_path =['features'])
        history = history.to_json(orient = 'records')
        with open('data/datos_chile.json', 'w') as f: f.write(history)

        return f

    def now(self):

        now = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2023-05-12%2000:00:00&maxlatitude=-17.5&minlatitude=-56.0&maxlongitude=-66.0&minlongitude=-81.0&minmagnitude=1&orderby=time-asc'
        now = requests.get(now).json()
        now = pd.json_normalize(now, record_path =['features'])
        now = now.to_json(orient = 'records')
        now = json.loads(now)
        now = list(now)
        with open('data/datos_chile.json', 'r') as f: history = json.load(f)
        for entry in now:
            if entry != history[-1]:
                history.append(entry)
        history = json.dumps(history)
        with open('data/datos_chile.json', 'w') as f: f.write(history)

        return

    def etl(self, df):
        chile = pd.read_json('data/datos_chile.json')
        columnas = [p.replace('properties.', '') for p in chile.columns.to_list()]
        new_names = dict(zip(chile.columns.to_list(), columnas))
        chile = chile.rename(new_names, axis='columns')
        chile = chile[chile.place.str.contains('Chile',na=False)]
        variables = ['type', 'id', 'updated', 'tz', 'url', 'detail', 'felt', 'cdi', 'mmi', 'alert', 'status', 
                'tsunami', 'sig', 'net', 'code', 'ids', 'sources', 'types' , 'nst', 'dmin', 'rms', 
                'gap', 'magType', 'type', 'title', 'geometry.type'] 
        chile = chile.drop(variables, axis='columns')
        chile.rename({'geometry.coordinates':'coordinates'}, axis='columns', inplace=True)
        chile[['longitude','latitude', 'depth']] = pd.DataFrame(chile.coordinates.tolist(), index= chile.index)
        chile.drop('coordinates',axis=1, inplace= True)

        def formatear_time(x):
            time = x/1000
            return datetime.datetime.fromtimestamp(time)

        chile.time = chile.time.apply(formatear_time)
        chile['date'] = chile.time.dt.date
        chile['time_hour'] = chile.time.dt.time
        chile['time_hour'] = chile['time_hour'].apply(lambda x: x.replace(microsecond=0))
        chile.drop('time', axis='columns', inplace=True)
        chile.rename({'mag':'magnitud', 'time_hour':'hora_local','date':'fecha_local','depth':'profundidad','latitude':'latitud','longitude':'longitud'}, axis='columns', inplace=True)

        def separate_date(row):
            part = row.place.split(" ")
            row['distancia'] = part[0]
            return row
        chile = chile.apply(separate_date, axis=1)
        def replace_as_0(row):
            try:
                int(row['distancia'])
            except:
                row['dist'] = 100000
            else:
                row['dist'] = int(row['distancia'])
            return row
        chile = chile.apply(replace_as_0, axis=1)
        chile.drop('distancia',axis=1,inplace=True)
        chile.rename({'dist':'distancia'}, axis='columns', inplace=True)
        chile.drop('place',axis=1,inplace=True)
        def codigo_region(row):
            point = row.latitud,row.longitude
            geolocator = Nominatim(user_agent='Google Maps') 
            location = geolocator.reverse(point)
            try:
                location.raw['address']['ISO3166-2-lvl4']
            except:
                row['codigo_region'] = 'Fuera de region'
            else:
                location = location.raw['address']['ISO3166-2-lvl4']
                row['codigo_region'] = str(location)
            return row
        chile = chile.apply(codigo_region, axis=1)
        
        chile = chile[['fecha_local','hora_local','magnitud','profundidad','latitud','longitud','distancia','codigo_region']]
        chile['fecha_local'] = chile['fecha_local'].apply(lambda x: str(x))
        
        chile_json = chile.to_json(orient = 'records')
        with open('data/datos_chile_etl.json', 'w') as f: f.write(chile_json)

        return f


# chile = chile()


class Japon:

    def history(self):

        history = "https://service.iris.edu/fdsnws/event/1/query?starttime=2022-01-01T00:00:00&&endtime=2023-05-11T23:59:59&orderby=time&format=geocsv&maxlat=47.587&minlon=128.288&maxlon=157.029&minlat=30.234&nodata=404"
        history = pd.read_csv(history, sep='|', skiprows=4)
        history = history[history.EventLocationName.str.contains('JAPAN')]
        history = history.sort_values('Time')
        history = history.to_json(orient = 'records')
        with open('data/datos_japon.json', 'w') as f: f.write(history)

        return f

    def now(self):

        now = "https://service.iris.edu/fdsnws/event/1/query?starttime=2023-05-12T00:00:00&&orderby=time&format=geocsv&maxlat=47.587&minlon=128.288&maxlon=157.029&minlat=30.234&nodata=404"
        now = pd.read_csv(now, sep='|', skiprows=4)
        now = now[now.EventLocationName.str.contains('JAPAN')]
        now = now.sort_values('Time')
        now = now.to_json(orient = 'records')
        now = json.loads(now)
        now = list(now)
        with open('data/datos_japon.json', 'r') as f: history = json.load(f)
        for entry in now:
            if entry != history[-1]:
                history.append(entry)
        history = json.dumps(history)
        with open('data/datos_japon.json', 'w') as f: f.write(history)

        return

    def etl(self, df):

        japon = df

        def separate_date(row):
            part = row.Time.split("T")
            row['date'] = part[0]
            row['time'] = part[1].strip("Z")
            return row

        japon = japon.apply(separate_date, axis=1)
        japon = japon.drop(['EventID', 'Author', 'Catalog', 'Contributor','ContributorID','MagType','MagAuthor','EventLocationName','Time'],
                           axis='columns')
        japon = japon.rename(columns={"Latitude":"latitude","Longitude":"longitude","Depth":"depth","Magnitude":"magnitude"})
        japon = japon[['date','time',	'magnitude','depth','latitude','longitude']]
        japon_json = japon.to_json(orient = 'records')

        with open('data/datos_japon_etl.json', 'w') as f: f.write(japon_json)

        return f


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name,
                              if_generation_match=generation_match_precondition
                              )

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def upload_limpio(file):

    """Sube al bucket del proyecto los datos en bruto
    de las distintas fuentes de datos sismicos de los
    paises"""

    name = file.split('/')[-1]
    print(name)
    upload_blob(BUCKET, file, name)


###############################################################################
###############################################################################
###############################################################################
###############################################################################

# CARGAR DATOS CRUDOS A BUCKET

def upload_to_bucket():

    """Sube al bucket del proyecto los datos en bruto
    de las distintas fuentes de datos sismicos de los
    paises"""

    # Carga de datos de japon
    japon = Japon()
    file_japon = japon.history().name
    name = file_japon.split('/')[-1]
    print(name)
    upload_blob(BUCKET, file_japon, name)

    # Carga de datos de eeuu
    eeuu = EEUU()
    file_eeuu = eeuu.history().name
    name = file_eeuu.split('/')[-1]
    print(name)
    upload_blob(BUCKET, file_eeuu, name)

    # Carga de datos de chile
    chile = Chile()
    file_chile = chile.history().name
    name = file_chile.split('/')[-1]
    print(name)
    upload_blob(BUCKET, file_chile, name)


def llenar_bucket():
    """activa la funcion que carga los datos al bucket"""
    upload_to_bucket()


# se obtiene el archivo de los datos de japon sin limpiar
def get_json_gcs(bucket_name, file_name):
    """lee un archivo json del bucket y
    lo retorna como DataFrame"""

    # get bucket with name
    BUCKET = client.get_bucket(bucket_name)

    # get the blob
    blob = BUCKET.get_blob(file_name)

    # load blob using json
    file_data = json.loads(blob.download_as_string())

    df = pd.DataFrame(file_data)

    return df


###############################################################################
###############################################################################
###############################################################################
###############################################################################


# LIMPIEZA DE JAPON
def limpieza_japon():
    """lanza la limpieza de los datos de japon y los sube al bucket"""
    japon_raw = get_json_gcs(BUCKET, "datos_japon.json")

    # Enviar a limpieza

    japon = Japon()
    file_japon = japon.etl(japon_raw).name

    # subir el archivo a bucket

    upload_limpio(file_japon)


###############################################################################
###############################################################################
###############################################################################
###############################################################################

# LIMPIEZA DE CHILE
def limpieza_chile():
    """lanza la limpieza de los datos de chile y los sube al bucket"""

    # se obtiene el archivo de los datos de chile sin limpiar

    chile_raw = get_json_gcs(BUCKET, "datos_chile.json")

    # Enviar a limpieza

    chile = Chile()
    file_chile = chile.etl(chile_raw).name

    # subir el archivo a bucket

    upload_limpio(file_chile)


###############################################################################
###############################################################################
###############################################################################
###############################################################################

# LIMPIEZA DE EEUU
def limpieza_eeuu():
    """lanza la limpieza de los datos de eeuu y los sube al bucket"""

    # se obtiene el archivo de los datos de eeuu sin limpiar

    eeuu_raw = get_json_gcs(BUCKET, "datos_eeuu.json")

    # Enviar a limpieza

    eeuu = EEUU()
    file_eeuu = eeuu.etl(eeuu_raw).name

    # subir el archivo a bucket

    upload_limpio(file_eeuu)


###############################################################################
###############################################################################
###############################################################################
###############################################################################

# ACCEDER A LOS DATOS LIMPIOS
# JAPON
def get_japon_limpio():
    """extrae los datos limpio de japon y los devuelve como dataframe"""
    return get_json_gcs(BUCKET, 'datos_japon_etl.json')


# CHILE
def get_chile_limpio():
    """extrae los datos limpio de chile y los devuelve como dataframe"""
    return get_json_gcs(BUCKET, 'datos_chile_etl.json')


# EEUU
def get_eeuu_limpio():
    """extrae los datos limpio de eeuu y los devuelve como dataframe"""
    return get_json_gcs(BUCKET, 'datos_eeuu_etl.json')
