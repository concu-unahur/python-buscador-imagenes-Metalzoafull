# Buscador de imágenes

Esta es una versión preliminar del enunciado de TP. La idea es que se familiaricen con la API de Pixabay y puedan verla funcionando en su entorno.

## Pasos a seguir

1. Crearse una cuenta en Pixabay.
1. Obtener el API key desde la [página de la documentación](https://pixabay.com/api/docs/#api_search_images).
1. Agregar la API key al código y ejecutarlo.
1. Modificar el código para que la bajada de imágenes se haga en threads distintos.
1. Parametrizar la query y la cantidad de imágenes, para poder cambiarlo desde la consola.

Ejemplo de lo último:

```python
import sys

nombre = sys.argv[1]
edad = sys.argv[2]

print(f'¡Hola {nombre}! Tenés {edad} años...')

# > python3 main.py Marcos 34 
# ¡Hola Marcos! Tenés 34 años...
```

## Links útiles

* [Documentación de la API de Pixabay](https://pixabay.com/api/docs/#api_search_images)
* [Ejemplos de manipulaciones con scikit](https://scikit-image.org/docs/dev/auto_examples/)
