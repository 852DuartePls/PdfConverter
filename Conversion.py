import os
import fitz
from PIL import Image
from reportlab.lib.pagesizes import portrait, landscape
from reportlab.pdfgen import canvas
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def convertir_pdf_a_imagen(archivo_pdf, extension_imagen, dir_salida):
    documento_pdf = fitz.open(archivo_pdf)
    nombre_base = os.path.splitext(os.path.basename(archivo_pdf))[0]

    for num_pagina in range(documento_pdf.page_count):
        pagina = documento_pdf.load_page(num_pagina)
        pixeles = pagina.get_pixmap()
        imagen = Image.frombytes("RGB", [pixeles.width, pixeles.height], pixeles.samples)

        ruta_imagen = os.path.join(dir_salida, f'{nombre_base}.{extension_imagen}')
        ruta_imagen = hacer_nombre_unico(ruta_imagen)
        imagen.save(ruta_imagen, extension_imagen.upper())

        print(f'Convertido {archivo_pdf} a {ruta_imagen}')

def hacer_nombre_unico(nombre_archivo):
    base, ext = os.path.splitext(nombre_archivo)
    contador = 1
    while os.path.exists(nombre_archivo):
        nombre_archivo = f'{base} ({contador}){ext}'
        contador += 1
    return nombre_archivo

def convertir_imagen_a_pdf(archivos_imagen, archivo_pdf_salida, dir_salida):
    primera_imagen = Image.open(archivos_imagen[0])
    ancho, alto = primera_imagen.size
    tamano_pagina = (ancho, alto)

    nombre_base = os.path.splitext(os.path.basename(archivos_imagen[0]))[0]

    archivo_pdf_salida = hacer_nombre_unico(os.path.join(dir_salida, f'{nombre_base}.pdf'))

    c = canvas.Canvas(archivo_pdf_salida, pagesize=tamano_pagina)
    for archivo_imagen in archivos_imagen:
        c.drawImage(archivo_imagen, 0, 0, width=tamano_pagina[0], height=tamano_pagina[1])
        c.showPage()
    c.save()

    print(f'Convertidas imágenes a {archivo_pdf_salida}')

def on_convertir_pdf_a_imagen():
    dir_entrada = input_folder_pdf.get()
    archivos_pdf = [archivo for archivo in os.listdir(dir_entrada) if archivo.lower().endswith('.pdf')]
    dir_salida = output_folder_pdf.get()
    
    for archivo_pdf in archivos_pdf:
        formato_imagen = image_format_choice.get()
        convertir_pdf_a_imagen(archivo_pdf, formato_imagen, dir_salida)
    
    messagebox.showinfo("Conversión Completada", "Conversión de PDF a Imagen completada con éxito.")

def on_convertir_imagen_a_pdf():
    dir_entrada = input_folder_image.get()
    archivos_imagen = [archivo for archivo in os.listdir(dir_entrada) if archivo.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if archivos_imagen:
        dir_salida = output_folder_image.get()
        convertir_imagen_a_pdf(archivos_imagen, os.path.join(dir_salida, f'output.pdf'), dir_salida)
    
    messagebox.showinfo("Conversión Completada", "Conversión de Imagen a PDF completada con éxito.")

def buscar_carpeta_entrada_pdf():
    folder_path = filedialog.askdirectory()
    input_folder_pdf.set(folder_path)

def buscar_carpeta_salida_pdf():
    folder_path = filedialog.askdirectory()
    output_folder_pdf.set(folder_path)

def buscar_carpeta_entrada_imagen():
    folder_path = filedialog.askdirectory()
    input_folder_image.set(folder_path)

def buscar_carpeta_salida_imagen():
    folder_path = filedialog.askdirectory()
    output_folder_image.set(folder_path)

# Crear la ventana principal de la GUI
root = tk.Tk()
root.title("Convertidor hecho por 852Duarte")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='PDF a Imagen')
tab_control.add(tab2, text='Imagen a PDF')
tab_control.pack(expand=1, fill="both")

# Pestaña de PDF a Imagen
tk.Label(tab1, text="Carpeta de Entrada:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
input_folder_pdf = tk.StringVar()
input_folder_pdf.set(os.getcwd())
tk.Entry(tab1, textvariable=input_folder_pdf).grid(row=0, column=1, padx=10, pady=5, sticky='w')
tk.Button(tab1, text="Buscar", command=buscar_carpeta_entrada_pdf).grid(row=0, column=2, padx=10, pady=5, sticky='w')

tk.Label(tab1, text="Carpeta de Salida:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
output_folder_pdf = tk.StringVar()
output_folder_pdf.set(os.getcwd())
tk.Entry(tab1, textvariable=output_folder_pdf).grid(row=1, column=1, padx=10, pady=5, sticky='w')
tk.Button(tab1, text="Buscar", command=buscar_carpeta_salida_pdf).grid(row=1, column=2, padx=10, pady=5, sticky='w')

image_format_choice = tk.StringVar()
image_format_choice.set("jpeg")
tk.Label(tab1, text="Formato de Imagen:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
image_format_menu = tk.OptionMenu(tab1, image_format_choice, "jpeg", "png")
image_format_menu.grid(row=2, column=1, padx=10, pady=5, sticky='w')

convert_button_pdf = tk.Button(tab1, text="Convertir", command=on_convertir_pdf_a_imagen)
convert_button_pdf.grid(row=3, column=0, padx=10, pady=10)

# Pestaña de Imagen a PDF
tk.Label(tab2, text="Carpeta de Entrada:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
input_folder_image = tk.StringVar()
input_folder_image.set(os.getcwd())
tk.Entry(tab2, textvariable=input_folder_image).grid(row=0, column=1, padx=10, pady=5, sticky='w')
tk.Button(tab2, text="Buscar", command=buscar_carpeta_entrada_imagen).grid(row=0, column=2, padx=10, pady=5, sticky='w')

tk.Label(tab2, text="Carpeta de Salida:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
output_folder_image = tk.StringVar()
output_folder_image.set(os.getcwd())
tk.Entry(tab2, textvariable=output_folder_image).grid(row=1, column=1, padx=10, pady=5, sticky='w')
tk.Button(tab2, text="Buscar", command=buscar_carpeta_salida_imagen).grid(row=1, column=2, padx=10, pady=5, sticky='w')

convert_button_image = tk.Button(tab2, text="Convertir", command=on_convertir_imagen_a_pdf)
convert_button_image.grid(row=2, column=0, padx=10, pady=10)

root.geometry("400x300")  # Establecer un tamaño de ventana inicial

root.mainloop()