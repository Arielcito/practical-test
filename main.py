import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def obtener_profesionales(url, especialidad):
    profesionales = []
    pagina = 1
    
    # Parámetros fijos y variables
    params = {
        'rubros': '2',  # Profesionales
        'provincia': '2',  # Ciudad de Buenos Aires
        'plan': '510',  # Plan 510
        'localidad': '0',  # Todas las localidades
        'especialidad': especialidad
    }
    
    while True:
        # Construir la URL de la página actual con los parámetros
        url_pagina = f"{url}&page={pagina}"
        
        # Realizar la solicitud HTTP con manejo de errores y reintentos
        for intento in range(3):
            try:
                respuesta = requests.get(url_pagina, params=params, timeout=10)
                respuesta.raise_for_status()
                break
            except (requests.RequestException, requests.Timeout) as e:
                print(f"Error en el intento {intento + 1}: {e}")
                if intento == 2:
                    print("No se pudo obtener la página. Pasando a la siguiente.")
                    return profesionales
                time.sleep(random.uniform(1, 3))
        
        # Parsear el contenido HTML
        sopa = BeautifulSoup(respuesta.content, 'html.parser')
        
        # Encontrar todos los profesionales en la página
        resultados = sopa.find_all('div', class_='result-item')
        
        if not resultados:
            break
        
        for resultado in resultados:
            nombre = resultado.find('h2', class_='title').text.strip()
            especialidad = resultado.find('p', class_='specialty').text.strip()
            direccion = resultado.find('p', class_='address').text.strip()
            telefono = resultado.find('p', class_='phone').text.strip()
            
            profesionales.append({
                'nombre': nombre,
                'especialidad': especialidad,
                'direccion': direccion,
                'telefono': telefono
            })
        
        print(f"Página {pagina} procesada. Profesionales encontrados: {len(profesionales)}")
        
        # Esperar antes de la siguiente solicitud para respetar los límites de tasa
        time.sleep(random.uniform(1, 2))
        
        pagina += 1
    
    return profesionales

def guardar_csv(profesionales, nombre_archivo):
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=['nombre', 'especialidad', 'direccion', 'telefono'])
        escritor.writeheader()
        for profesional in profesionales:
            escritor.writerow(profesional)

if __name__ == "__main__":
    url_base = "https://www.osde.com.ar/index1.html#!cartilla.html"
    
    # Psicología adultos
    especialidad_adultos = '66'  # Ajusta este código según corresponda
    profesionales_adultos = obtener_profesionales(url_base, especialidad_adultos)
    guardar_csv(profesionales_adultos, "psicologia_adultos_osde.csv")
    print(f"Se han guardado {len(profesionales_adultos)} profesionales de psicología adultos en el archivo CSV.")
    
    # Psicología niños y adolescentes
    especialidad_ninos = '67'  # Ajusta este código según corresponda
    profesionales_ninos = obtener_profesionales(url_base, especialidad_ninos)
    guardar_csv(profesionales_ninos, "psicologia_ninos_adolescentes_osde.csv")
    print(f"Se han guardado {len(profesionales_ninos)} profesionales de psicología niños y adolescentes en el archivo CSV.")
