import requests
import json
import os
import threading
import logging
import time
from PIL import Image
import numpy as np
from skimage import io, img_as_ubyte, transform, exposure
from skimage.color import rgb2gray
from pathlib import Path
import cv2

directorio_actual = Path.cwd()

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class PixabayAPI:
  def __init__(self, key, carpeta_imagenes):
    self.key = '15310819-177b76768182e60465fa86c2d'
    self.carpeta_imagenes = carpeta_imagenes
    self.listaI = []
    #self.listaG = []
    #self.listaC = []
    #self.listaR = []
    self.cont = 3
    self.nombre = "rojelio"
    self.monitorC = threading.Condition()
    self.monitorR = threading.Condition()
    
    
  def buscar_imagenes(self, query, cantidad):
    # URL de búsqueda. Ver la documentación en https://pixabay.com/api/docs/#api_search_images
    url = f'https://pixabay.com/api/?key={self.key}&per_page={cantidad}&q={query}&image_type=photo&lang=es'

    # Hago la request y parseo el JSON que viene como respuesta
    response = requests.get(url)
    jsonResponse = json.loads(response.text)

    # La respuesta tiene esta pinta:
    # {
    # 	"total": 4692,
    # 	"totalHits": 500,
    # 	"hits": [{
    # 			"id": 195893,
    # 			"pageURL": "https://pixabay.com/en/blossom-bloom-flower-195893/",
    # 			"type": "photo",
    # 			"tags": "blossom, bloom, flower",
    # 			"largeImageURL": "https://pixabay.com/get/ed6a99fd0a76647_1280.jpg",
    #       ... más campos que no interesan
    # 		}, {
    #       ...otra imagen
    #     }
    # 	]
    # }
    #
    # Pero solo nos interesa el campo "largeImageURL" que está dentro de la lista de "hits".
    # Para que la función devuelva eso usamos un map, que en Wollok sería algo así:
    #
    # jsonResponse.hits.map { x => x.largeImageURL }
    #
    # Pero en Python las funciones de listas son funciones globales y no métodos, así que queda así:
    return map(lambda h: h['largeImageURL'], jsonResponse['hits'])

  def descargar_imagen(self, url):
    # Bajo la imagen (una chorrera de bytes)
    bytes_imagen = requests.get(url)

    # Corto a la URL por cada barra - split('/') - 
    # y me quedo con el último pedazo - [-1] -, 
    # que es el nombre del archivo
    nombre_imagen = url.split('/')[-1]

    # Armo la ruta final del archivo, 
    # el os.path.join mete las barritas en el medio
    ruta_archivo = os.path.join(self.carpeta_imagenes, nombre_imagen)
    with open(ruta_archivo, 'wb') as archivo:
      archivo.write(bytes_imagen.content)
    self.listaI.append(nombre_imagen)
    #print(self.listaI)
  
  def lista_imagenes(self):
    return self.lista_imagenes
  
  def armar_ruta(self,nombre):
   return (directorio_actual / 'imagenes' / nombre).resolve()

  def leer_imagen(self,nombre):
   return io.imread(self.armar_ruta(nombre))

  def escribir_imagen(self,nombre, imagen):
   io.imsave(self.armar_ruta(nombre), img_as_ubyte(imagen))

  def concatenar_vertical(self, imagenes):
  # Buscamos el ancho menor entre todas las imágenes
   ancho_minimo = min(im.shape[1] for im in imagenes)

  # Redimensionamos las imágenes para que tengan todas el mismo ancho
   imagenes_redimensionadas = [cv2.resize(im, (ancho_minimo, int(im.shape[0] * ancho_minimo / im.shape[1])))
                    for im in imagenes]

  # Concatenamos
   return cv2.vconcat(imagenes_redimensionadas)
  
  def escala_de_grises(self, imagene):
    return rgb2gray(imagene)

  def rotacion(self, img, angulo):
   return transform.rotate(img, angulo)

  def contraste_adaptativo(self,img):
   return exposure.equalize_adapthist(img, clip_limit=0.03)
  
  def contrastar(self):
    with self.monitorC:
      while(True):
       nombre = self.listaI.pop(0)
       aux = self.leer_imagen(nombre)
       aux2 = self.contraste_adaptativo(aux)
       self.escribir_imagen("Cont"+nombre, aux2)
       self.listaI.append("Cont"+nombre)
      self.monitorR.notify()

    #self.listaC.append(aux2)
    #for i in self.listaI:
    #  aux = self.leer_imagen(i)
    #  aux2 = self.contraste_adaptativo(aux)
    #  self.escribir_imagen("C"+i,aux2)

  def rotar(self):
    self.monitorR.wait()
    listAux = [ palabra for palabra in self.listaI if palabra[:4] == 'Cont' ]
    with self.monitorR:
      while(True):
       nombre = listAux.pop(0)
       aux = self.leer_imagen(nombre)
       aux2 = self.rotacion(aux, 25)
       self.escribir_imagen("Rot"+ nombre, aux2)
       self.listaI.append("Rot"+ nombre)
       self.cont -= 1
      self.cont = 3
      #aux = self.listaC.pop(0)
      #self.listaR.append(aux2)
      #self.listaR.append(aux2)
    #for i in self.listaI:
    #  aux = self.leer_imagen(i)
    #  aux2 = self.rotacion(aux, 25)
    #  self.escribir_imagen(i + "R.jpg",aux2)


  def transform_Gris(self):
    listAux = [ palabra for palabra in self.listaI if palabra[:3] == 'Rot' ]
    while(self.cont > 0):
      nombre = listAux.pop(0)
      aux = self.leer_imagen(nombre)
      aux2 = self.escala_de_grises(aux)
      self.escribir_imagen("Gris"+nombre,aux2)
      self.listaI.append("Gris"+nombre)
      #self.listaG.append(self.leer_imagen(f"{self.cont}.jpg"))
      self.cont -= 1
    self.cont = 3

  def concatenacion(self):
    listAux = [ palabra for palabra in self.listaI if palabra[:4] == 'Gris' ]#esto esta mal, falta poner el leer
    self.escribir_imagen("roberto.jpg",self.concatenar_vertical(listAux))
    #for i in self.listaI:
    #  aux = self.leer_imagen(i)
    #  aux2 = self.escala_de_grises(aux)
    #  self.escribir_imagen(i +"N.jpg",aux2)

  #def armar_ruta(self,nombre):
  #  return os.path.join(self.carpeta_imagen, nombre)
    #for i in self.listaI:
    #  aux = i
    #  aux1 = aux[:10]
    #  return os.path.join(aux1,nombre)
    #return os.path.join(self.carpeta_imagenes, nombre)
  
  #def escribir_imagen(self, nombre, imagen):
  # Image.fromarray(imagen).save(self.armar_ruta(nombre))
  
  #def concatenar_horizontal(self):
  # min_img_shape = sorted([(np.sum(i.size), i.size) for i in self.listaL])[0][1]
  # return np.hstack(list((np.asarray(i.resize(min_img_shape, Image.ANTIALIAS)) for i in self.listaL)))
  #def leer_imagen(self):
  #  for i in self.listaI:
  #    aux = i
  #    self.listaL.append(Image.open(self.armar_ruta(aux[11:])))
   # return self.listaL #Image.open(self.armar_ruta(aux1))
  

  #def concatenar_horizontal(imagenes):
  # min_img_shape = sorted([(np.sum(i.size), i.size) for i in imagenes])[0][1]
  # return np.hstack(list((np.asarray(i.resize(min_img_shape, Image.ANTIALIAS)) for i in imagenes)))