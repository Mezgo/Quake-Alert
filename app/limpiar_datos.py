import utils

utils.autenticar()

# utils.vacear_bucket(['datos_chile_etl.json', 'datos_eeuu_etl.json', 'datos_japon_etl.json'])

# try:
#     utils.limpieza_japon()
# except:
#     utils.borrar_archivo('datos_japon_etl.json')
#     utils.limpieza_japon()

try:
    utils.limpieza_chile()
except:
    utils.borrar_archivo('datos_chile_etl.json')
    utils.limpieza_chile()

# try:
#     utils.limpieza_eeuu()
# except:
#     utils.borrar_archivo('datos_eeuu_etl.json')
#     utils.limpieza_eeuu()
