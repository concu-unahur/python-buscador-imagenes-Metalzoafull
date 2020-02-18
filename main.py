import logging
from api import PixabayAPI

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

carpeta_imagenes = './imagenes'
query = 'computadoras'
api = PixabayAPI('PONER ACÁ EL API KEY', carpeta_imagenes)

logging.info(f'Buscando imagenes de {query}')
urls = api.buscar_imagenes(query, 5)

for u in urls:
  logging.info(f'Descargando {u}')
  api.descargar_imagen(u)
