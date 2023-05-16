# Importar librerias
import requests                    
import pandas as pd                                        
import datetime
import json


class eeuu:

    def history(self):

        history = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2023-01-01%2000:00:00&endtime=2023-05-11%2023:59:59&maxlatitude=50&minlatitude=24.6&maxlongitude=-65&minlongitude=-125&minmagnitude=1&orderby=time-asc'
        history = requests.get(history).json()
        history = pd.json_normalize(history, record_path =['features'])
        history = history.to_json(orient = 'records')
        with open('datos_eeuu.json', 'w') as f: f.write(history)

        return
    
    def now(self):

        now = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2023-05-12%2000:00:00&maxlatitude=50&minlatitude=24.6&maxlongitude=-65&minlongitude=-125&minmagnitude=1&orderby=time-asc'
        now = requests.get(now).json()
        now = pd.json_normalize(now, record_path =['features'])
        now = now.to_json(orient = 'records')
        now = json.loads(now)
        now = list(now)
        with open('datos_eeuu.json', 'r') as f: history = json.load(f)
        for entry in now:
            if entry != history[-1]:
                history.append(entry)
        history = json.dumps(history)
        with open('datos_eeuu.json', 'w') as f: f.write(history)

        return

    def etl(self):
        eeuu = pd.read_json('datos_eeuu.json')
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
        eeuu.rename({'mag':'magnitude', 'time_hour':'time'}, axis='columns', inplace=True)
        eeuu.drop('place', axis='columns', inplace=True)
        eeuu = eeuu[['date','time',	'magnitude','depth','latitude','longitude']]
        eeuu['date'] = eeuu['date'].apply(lambda x: str(x))
        eeuu_json = eeuu.to_json(orient = 'records')
        with open('datos_eeuu_etl.json', 'w') as f: f.write(eeuu_json)

        return
        
eeuu = eeuu()

class chile:

    def history(self):

        history = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2023-01-01%2000:00:00&endtime=2023-05-11%2023:59:59&maxlatitude=-17.5&minlatitude=-56.0&maxlongitude=-66.0&minlongitude=-81.0&minmagnitude=1&orderby=time-asc'
        history = requests.get(history).json()
        history = pd.json_normalize(history, record_path =['features'])
        history = history.to_json(orient = 'records')
        with open('datos_chile.json', 'w') as f: f.write(history)

        return
    
    def now(self):

        now = 'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2023-05-12%2000:00:00&maxlatitude=-17.5&minlatitude=-56.0&maxlongitude=-66.0&minlongitude=-81.0&minmagnitude=1&orderby=time-asc'
        now = requests.get(now).json()
        now = pd.json_normalize(now, record_path =['features'])
        now = now.to_json(orient = 'records')
        now = json.loads(now)
        now = list(now)
        with open('datos_chile.json', 'r') as f: history = json.load(f)
        for entry in now:
            if entry != history[-1]:
                history.append(entry)
        history = json.dumps(history)
        with open('datos_chile.json', 'w') as f: f.write(history)

        return

    def etl(self):
        chile = pd.read_json('datos_chile.json')
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
        chile.rename({'mag':'magnitude', 'time_hour':'time'}, axis='columns', inplace=True)
        chile.drop('place', axis='columns', inplace=True)
        chile = chile[['date','time',	'magnitude','depth','latitude','longitude']]
        chile['date'] = chile['date'].apply(lambda x: str(x))
        chile_json = chile.to_json(orient = 'records')
        with open('datos_chile_etl.json', 'w') as f: f.write(chile_json)

        return
        
chile = chile()

class japon:

    def history(self):
        
        history = "https://service.iris.edu/fdsnws/event/1/query?starttime=2023-01-01T00:00:00&&endtime=2023-05-11T23:59:59&orderby=time&format=geocsv&maxlat=47.587&minlon=128.288&maxlon=157.029&minlat=30.234&nodata=404"
        history = pd.read_csv(history, sep='|', skiprows=4)
        history = history[history.EventLocationName.str.contains('JAPAN')]
        history = history.sort_values('Time')
        history = history.to_json(orient = 'records')
        with open('datos_japon.json', 'w') as f: f.write(history)

        return    

    def now(self):

        now = "https://service.iris.edu/fdsnws/event/1/query?starttime=2023-05-12T00:00:00&&orderby=time&format=geocsv&maxlat=47.587&minlon=128.288&maxlon=157.029&minlat=30.234&nodata=404"
        now = pd.read_csv(now, sep='|', skiprows=4)
        now = now[now.EventLocationName.str.contains('JAPAN')]
        now = now.sort_values('Time')
        now = now.to_json(orient = 'records')
        now = json.loads(now)
        now = list(now)
        with open('datos_japon.json', 'r') as f: history = json.load(f)
        for entry in now:
            if entry != history[-1]:
                history.append(entry)
        history = json.dumps(history)
        with open('datos_japon.json', 'w') as f: f.write(history)

        return
    
    def etl(self):

        japon = pd.read_json('datos_japon.json')
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
        with open('datos_japon_etl.json', 'w') as f: f.write(japon_json)

        return
    
japon = japon()









    







