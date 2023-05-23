import pandas as pd
import utils
from google.cloud import storage

# utils.autenticar()

# df_chile = carga.get_chile_limpio()
df_japon = utils.get_japon_limpio()
# df_eeuu = carga.get_eeuu_limpio()

print(df_japon.head(5))

