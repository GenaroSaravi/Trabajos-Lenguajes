Descripción general:

Este proyecto analiza el dataset TMDB 5000 Movies/Credits mediante un Notebook en Google Colab, donde se realiza la limpieza, el análisis exploratorio, los gráficos y las estadísticas principales.
Los resultados finales se exportan como archivos JSON.

Estos JSON son utilizados por una mini-API local en Flask, que expone los datos procesados a través de endpoints en formato JSON.
Así, el Notebook cumple la función de generar y preparar los resultados, mientras que la API permite consultarlos y mostrarlos de manera simple para la presentación del trabajo final.

Instrucciones para ejecutar el Notebook y la API

1. Ejecución del Notebook (.ipynb)

Abrir Google Colab.

Montar Google Drive:

from google.colab import drive
drive.mount('/content/drive')


Cambiar al directorio donde se encuentran los archivos:

import os
base = "/content/drive/MyDrive/Colab Notebooks/Trabajo Practico Final"
os.chdir(base)

Ejecutar todas las celdas del Notebook con:

Runtime → Ejecutar todo.
O correr celda por celda.


2. Ejecución de la Mini API Local

Requisitos
Python instalado en la PC
Flask instalado: pip install flask

Los JSON deben haber sido descargados desde el Notebook y colocados en API/salidas/.

Cómo ejecutar la API

Abrir terminal en la carpeta API/:
cd API

Ejecutar la API:
python app.py

Si todo está correcto, verás:
 * Running on http://127.0.0.1:5000

3. Probar los endpoints en el navegador

Abrir el navegador y poner en la barra:

ROI por género:
http://127.0.0.1:5000/roi

Duración por década:
http://127.0.0.1:5000/runtime

Relación presupuesto–rating:
http://127.0.0.1:5000/budget_rating

Cada uno devolverá JSON con los resultados del análisis.