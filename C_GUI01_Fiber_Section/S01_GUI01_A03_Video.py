# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-05-15
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI01_A03_Video.py
COMENTARIOS:    Genera video a partir de fotogramas.
"""

# %% TODO: [00] LIBRERIAS
import os
import imageio.v2 as imageio  # Usa imageio.v2 para evitar el aviso de deprecación
import glob


# %% TODO: [01] FUNCIONES
def video(carpeta_foto, URL_video, FPS):
    """
    Genera un video a partir de una secuencia de imágenes.
    Args:
        carpeta_foto: Define la ruta a la carpeta con las imágenes
        URL_video: Ruta de carpeta y nombre de video.
        FPS: Fotogramas por segundo
    """
    # Obtiene una lista de todos los archivos .png en la carpeta especificada
    archivos_png = glob.glob(os.path.join(carpeta_foto, '*.png'))

    # Ordena la lista de archivos
    archivos_png.sort()

    cont = 0
    # Crea un objeto 'writer' para escribir el video
    with imageio.get_writer(URL_video, fps=FPS) as writer:
        # Recorre todos los archivos .png en la lista ordenada
        for archivo_png in archivos_png:
            img = imageio.imread(archivo_png)
            writer.append_data(img)
            cont += 1
