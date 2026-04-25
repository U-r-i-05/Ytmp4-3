#cosas a importar
from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import filedialog
import os
from pytubefix import YouTube
from PIL import Image, ImageTk  # Importa Pillow
import random
import sys

#-----------------------------------funciones a usar---------------------------------------------------------------

def resoluciones_disponibles(event=None):
    url = enlace.get()  # Obtiene la URL de la caja de texto  
    try:
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
        
        # Lista para guardar las resoluciones
        resoluciones = []
        
        # Bucle para obtener las resoluciones
        for stream in yt.streams.filter(progressive=False):
            if stream.resolution:  # Comprobamos si tiene resolución
                resoluciones.append(stream.resolution)
        
        # Actualizamos el combobox con las resoluciones
        combo['values'] = resoluciones

    except Exception as e:
        ventana.after(0,lambda:messagebox.showerror("Error", f"Hubo un problema al obtener el video: {str(e)}")) 
        
def descargar_video(event=None):
    url = enlace.get()
    directorio= filedialog.askdirectory()# Obtiene la carpeta de destino seleccionandola
    if not directorio:
        print("No existe el directorio seleccionado.")
    carpeta = directorio 
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
    titulo=yt.title # ahora el nombre será el del video
    resolucion_seleccionada = combo.get()

    # Filtrar el stream de video según la resolución seleccionada (ahora no nos importa el tipo)
    stream_video_seleccionado = yt.streams.filter(res=resolucion_seleccionada, type="video").first()

    if stream_video_seleccionado:
        stream_video_seleccionado.download(output_path=carpeta, filename=f"{titulo} video.mp4")# Descargar el video en la resolución seleccionada
    else: # Si no está disponible el stream de la resolución seleccionada, selecciona el de mayor resolución
        ventana.after(0,lambda:messagebox.showwarning(title="resolucion no encontrada", message="No se encontró un stream de video con resolución asignada. Descargando el mejor disponible..."))
        mejor_disponible = yt.streams.get_highest_resolution()
        mejor_disponible.download(output_path=carpeta, filename=f"{titulo} video.mp4")  # Descargar el video con la mejor resolución
        ventana.after(0,lambda:messagebox.showinfo(title="estado de descarga",message="Descarga completa de video."))
        
# Descargar el mejor stream de audio disponible
    audio_stream = yt.streams.filter(type="audio").first()
    if audio_stream:
        audio_stream.download(output_path=carpeta, filename=f"{titulo} audio.mp3")
    else:
        ventana.after(0,lambda:messagebox.showerror(title="error en descarga", message="No se encontró un stream de audio adecuado."))

    ventana.after(0,lambda:messagebox.showinfo(title="estado de descarga",message="Descarga de video y audio por separado completada"))  
  
def descargar_audio(event=None):
    url = enlace.get()
    directorio= filedialog.askdirectory()
    if not directorio:
        ventana.after(0,lambda:messagebox.showwarning(title="error de directorio",message="no se seleccionó un directorio"))
    carpeta = directorio
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
    titulo=yt.title # ahora el nombre será el del video
    audio_stream = yt.streams.filter(type="audio").first()
    audio_stream.download(output_path=carpeta, filename=f"{titulo} audio.mp3")
    ventana.after(0,lambda:messagebox.showinfo(title="estado de descarga",message="Descarga de audio completada"))

def cambiar_fondo(event=None):
    global image
    # Ruta de la imagen con respecto al script o .exe
    ruta = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )
    if ruta:
        image=Image.open(ruta)
        image=image.resize((900,300))
        fondo=bg = ImageTk.PhotoImage(image)
        label1.config(image=fondo)
        

#                                                 config de ventana
ventana = tk.Tk()#--------------------------------inicia la ventana------------------------------------------------
ventana.config(width=900, height=300)
ventana.title("Convertidor Youtube a mp4/mp3")
ventana.resizable(False, False)  # Desactiva la opción de cambiar el tamaño

# Obtener la ruta donde está el script o .exe
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)  # carpeta del .exe
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))  # carpeta del script

archivos=os.listdir(script_dir)

imagenes = [
        f for f in archivos
        if os.path.isfile(os.path.join(script_dir, f))
        and f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

# Ruta de la imagen con respecto al script o .exe (y agarra cualquier imagen que tenga ese directorio)
ruta = os.path.join(script_dir, random.choice(imagenes))
# Carga la imagen usando Pillow
image = Image.open(ruta)
image=image.resize((900,300))
# Convierte la imagen a un formato compatible con Tkinter
bg = ImageTk.PhotoImage(image)
# Muestra la imagen en un label
label1 = tk.Label(ventana, image=bg)

#textos
calidad=tk.Label(ventana,text='calidad disponible',font=("Consolas", 12), fg='white', bg="black")# texto arriba de desplegable
resoluciones = []# Lista para guardar las resoluciones
combo = ttk.Combobox(values=resoluciones)# menu desplegable
enlace_t=tk.Label(ventana,text='Ingrese la url del vídeo a descargar',font=("Consolas", 13), fg='white', bg="black")
directorio_t=tk.Label(ventana,text='Ingrese el directorio donde guardar la descarga',font=("Consolas", 13), fg='white', bg="black")

#botones
b_descargar_audio=tk.Button(ventana,text='descargar audio',command=descargar_audio,font=("Consolas", 11))
b_descargar_video=tk.Button(ventana,text='descargar video + audio',command=descargar_video,font=("Consolas", 11))
b_cambiar_fondo=tk.Button(ventana,text='probar otro fondo',command=cambiar_fondo,font=("Consolas",11))
#cajas de texto y entrada
enlace=tk.Entry(ventana, width=50,font=("Consolas", 13))# caja de texto 1(.get toma de aca)


# Evento para actualizar las resoluciones cuando se cambia la URL
enlace.bind("<FocusOut>", resoluciones_disponibles)  # Actualiza resoluciones cuando el campo pierde foco
enlace.bind("<Return>", resoluciones_disponibles)  # Actualiza resoluciones cuando presionas Enter

#donde colocamos todo
label1.place(x=-2, y=0)
calidad.place(x=645, y=160)# posicion texto arriba de desplegable
combo.place(x=650, y=180)# posicion de menu desplegable
b_descargar_audio.place(x=650, y=100)# posicion de boton descarga audio
b_descargar_video.place(x=650, y=50)# posicion de boton descarga video+audio
b_cambiar_fondo.place(x=80, y=150)# posicion de boton cambio de fondo
enlace.place(x=80, y=80,height=30)# posicion de caja de texto 1
enlace_t.place(x=80, y=50,height=30)# posicion de texto caja de texto 1

ventana.mainloop()#-------------------------------termina la ventana------------------------------------------------
