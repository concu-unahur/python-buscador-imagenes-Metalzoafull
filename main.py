import threading
import time
import logging
import numpy
from api import PixabayAPI

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


carpeta_imagenes = './imagenes'
query = 'computadoras'
api = PixabayAPI('PONER ACÁ EL API KEY', carpeta_imagenes)

logging.info(f'Buscando imagenes de {query}')
urls = api.buscar_imagenes(query, 5)

for u in urls:
  logging.info(f'Descargando {u}')
  des = threading.Thread(target=api.descargar_imagen(u))

comedia = threading.Thread(target=api.contrastar())
logging.info(f"caca {threading.Thread(target=api.rotar())}")
risas = threading.Thread(target=api.transform_Gris())
#conc = threading.Thread(target=api.concatenacion())

#lista = api.lista_imagenes()
#logging.info(f'caca{lista}')
#hola = []

#for i in lista:
#  hola.append(api.leer_imagen(i))

#dox = threading.Thread(target=api.concatenar_horizontal(hola))
#con = threading.Thread(target=api.concatenar_horizontal())
#con = threading.Thread(target=api.escribir_imagen('caca',api.concatenar_horizontal()))

  


#  logging.info(f'Descargando {u}')
#  api.descargar_imagen(u)

#des = threading.Thread(target=api.descargar_imagen(urls(1)))
#des = threading.Thread(target=api.descargar_imagen(urls(2)))