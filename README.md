
# Ytmp4-3

Este fue un side project hecho más que nada para descargar vídeos (extrayendo solo audio o audio y vídeo) y para probar git y git-hub (mediante subir el repositorio de este proyecto).

El programa posee 2 cajas de texto, 1 para ingresar el enlace y el 2do para ingresar la ruta donde se va a descargar el video.

En caso de querer desargar video puedes escoger la calidad del mismo, en el caso del audio, solo se descargará la mejor resolucion disponible.


## Uso del ejecutable:
como todo código python convertido a .exe mediante pyinstaller, es detectado como virus por el antivirus, por ende, habrá un esfuerzo extra por parte del usuario para poner el directorio donde se guarde el ejecutable como excepción.

## Uso del código fuente:
Se usan las librerías tkinter, pytubefix, os y pillow. por lo que hay que instalarlas en caso de querer usar el código. Además de tener una imagen para el fondo con la misma resolución de la ventana (900x300).
## Authors

- [@uri](https://www.github.com/U-r-i-05)


## FAQ (preguntas freguentes)

#### ERROR: pytubefix.exceptions.RegexMatchError: regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*".

Solución/causa: Ver las variables que tengan acceso al enlace, por lo general este error ocurre cuando hay un error con en enlace, más que nada debido a que o url o enlace no están en la función, o que te hayas olvidado de poner el event=none.Y si te pasó que quisiste usar url como variable global y te salió este error, descarta la variable global, es un desperdicio hacerlo ¿quién usaría variables globales para eso?.

#### ERROR:"File"c:\Users\usuario\AppData\Local\Programs\Python\Python312\Lib\tkinter\__init__.py", line 1968, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
TypeError: resoluciones_disponibles() takes 0 positional arguments but 1 was given"

Solución/causa: Se agrega el event=none. Esto se debe a que estará esperando todo el tiempo que se ingrese el enlace, pero como seguramente estas buscando el enlace para pegar en la caja de texto, no tiene todavia, por eso el error, así que esto esta para que no salte error desde el minuto 0.

#### DETALLE: yt = YouTube(url, use_oauth=False, allow_oauth_cache=False, on_progress_callback=on_progress)

esto es una aclaración para evitar que pida validación mediante poner como falso use_oauth y allow_oauth_cache.
