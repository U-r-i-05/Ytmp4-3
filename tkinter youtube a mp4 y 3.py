#cosas a importar
from tkinter import messagebox, ttk
import tkinter as tk
from tkinter import filedialog
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from PIL import Image, ImageTk  # Importa Pillow

#-----------------------------------funciones a usar---------------------------------------------------------------

# Función para descargar el video o audio(todas las funcionalidades de pytube poner como funcion/command)
def resoluciones_disponibles(event=None):
    url = enlace.get()  # Obtiene la URL de la caja de texto  
    try:
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=False, on_progress_callback=on_progress)
        
        # Lista para guardar las resoluciones
        resoluciones = []
        
        # Bucle para obtener las resoluciones
        for stream in yt.streams.filter(progressive=False):
            if stream.resolution:  # Comprobamos si tiene resolución
                resoluciones.append(stream.resolution)
        
        # Actualizamos el combobox con las resoluciones
        combo['values'] = resoluciones

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al obtener el video: {str(e)}") 
        
#funcion para descargar video
def descargar_video(event=None):
    url = enlace.get()
    directorio= filedialog.askdirectory()
    if not directorio:
        print("No directory selected.")
    carpeta = directorio # Obtiene la carpeta de destino seleccionandola
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False, on_progress_callback=on_progress)
    titulo=yt.title # ahora el nombre será el del video
    selected_resolution = combo.get()

    # Filtrar el stream de video según la resolución seleccionada (ahora no nos importa el tipo)
    selected_stream = yt.streams.filter(res=selected_resolution, type="video").first()

    if selected_stream:
        selected_stream.download(output_path=carpeta, filename=f"{titulo} video.mp4")# Descargar el video en la resolución seleccionada
    else: # Si no está disponible el stream de la resolución seleccionada, selecciona el de mayor resolución
        messagebox.showwarning(title="resolucion no encontrada", message="No se encontró un stream de video con resolución asignada. Descargando el mejor disponible...")
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path=carpeta, filename=f"{titulo} video.mp4")  # Descargar el video con la mejor resolución
        messagebox.showinfo(title="estado de descarga",message="Descarga completa de video.")
        
# Descargar el mejor stream de audio disponible
    audio_stream = yt.streams.filter(type="audio").first()
    if audio_stream:
        audio_stream.download(output_path=carpeta, filename=f"{titulo} audio.mp4")# Cambia la extensión si lo prefieres
    else:
        messagebox.showerror(title="error en descarga", message="No se encontró un stream de audio adecuado.")

    messagebox.showinfo(title="estado de descarga",message="Descarga de video y audio por separado completada")  
    #pass

#funcion para descargar audio.    (NO USAR VARIABLES GLOBALES,rompen todo)
def descargar_audio(event=None):
    url = enlace.get()
    directorio= filedialog.askdirectory()
    if not directorio:
        print("No directory selected.")
    carpeta = directorio
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False, on_progress_callback=on_progress)
    titulo=yt.title # ahora el nombre será el del video
    audio_stream = yt.streams.filter(type="audio").first()
    audio_stream.download(output_path=carpeta, filename=f"{titulo} audio.mp4")
    messagebox.showinfo(title="estado de descarga",message="Descarga de audio completada")
    

#                                                 config de ventana
ventana = tk.Tk()#--------------------------------inicia la ventana------------------------------------------------
ventana.config(width=900, height=300)
ventana.title("Convertidor Youtube a mp4/mp3")
ventana.resizable(False, False)  # Desactiva la opción de cambiar el tamaño

#imagen de fondo
# Obtener la ruta donde está el script o .exe
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta de la imagen con respecto al script o .exe
image_path = os.path.join(script_dir, 'fondo del convertidor.jpg')
# Carga la imagen usando Pillow
image = Image.open(image_path)
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

#cajas de texto y entrada
enlace=tk.Entry(ventana, width=50,font=("Consolas", 13))# caja de texto 1(.get de aca)


# Evento para actualizar las resoluciones cuando se cambia la URL
enlace.bind("<FocusOut>", resoluciones_disponibles)  # Actualiza resoluciones cuando el campo pierde foco
enlace.bind("<Return>", resoluciones_disponibles)  # Actualiza resoluciones cuando presionas Enter

#donde colocamos todo
label1.place(x=-2, y=0)
calidad.place(x=645, y=160)# posicion texto arriba de desplegable
combo.place(x=650, y=180)# posicion de menu desplegable
b_descargar_audio.place(x=650, y=100)# posicion de boton descarga audio
b_descargar_video.place(x=650, y=50)# posicion de boton descarga video+audio
enlace.place(x=80, y=80,height=30)# posicion de caja de texto 1
enlace_t.place(x=80, y=50,height=30)# posicion de texto caja de texto 1

ventana.mainloop()#-------------------------------termina la ventana------------------------------------------------
