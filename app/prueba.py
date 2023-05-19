import pandas as pd
import carga

carga.autenticar()

df_chile = carga.get_chile_limpio()
df_japon = carga.get_japon_limpio()
df_eeuu = carga.get_eeuu_limpio()

print(df_chile.head())
