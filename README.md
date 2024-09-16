# Extractor de Profesionales de Salud Mental OSDE

Este programa extrae información de profesionales de salud mental del sitio web de OSDE y la guarda en archivos CSV.

## Requisitos previos

1. Python 3.7 o superior instalado en tu sistema.
2. Navegador Google Chrome instalado.
3. ChromeDriver compatible con tu versión de Chrome.

## Instalación

1. Clona este repositorio o descarga los archivos en tu computadora.

2. Instala las dependencias necesarias ejecutando el siguiente comando en tu terminal:

   ```
   pip install selenium beautifulsoup4
   ```

3. Descarga el ChromeDriver adecuado para tu versión de Chrome desde [aquí](https://sites.google.com/a/chromium.org/chromedriver/downloads) y colócalo en el mismo directorio que el script `main.py`.

## Configuración

1. Abre el archivo `main.py` en un editor de texto.

2. En la sección `if __name__ == "__main__":`, puedes modificar los valores de los diccionarios `valores_adultos`, `valores_ninios`, `valores_adultos_zona_oeste` y `valores_adultos_zona_norte` según tus necesidades. Estos diccionarios controlan los parámetros de búsqueda para cada extracción.

## Ejecución

1. Abre una terminal o línea de comandos.

2. Navega hasta el directorio donde se encuentra el archivo `main.py`.

3. Ejecuta el siguiente comando:

   ```
   python main.py
   ```

4. El programa comenzará a ejecutarse y verás mensajes en la consola indicando el progreso.

5. Una vez finalizada la ejecución, se crearán varios archivos CSV en el mismo directorio:
   - `profesionales_adultos.csv`
   - `profesionales_ninos_adolescentes.csv`
   - `profesionales_adultos_zona_oeste.csv`
   - `profesionales_adultos_zona_norte.csv`
