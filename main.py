from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import csv
import time

def cambiar_valor_plan(navegador, nuevo_valor):
    try:
        # Esperar a que se cargue el contenido dinámico
        print("Esperando a que se cargue el contenido dinámico...")
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "planId"))
        )
        
        # Encontrar el elemento input
        input_plan = navegador.find_element(By.ID, "planId")
        
        # Cambiar el valor usando JavaScript
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_plan)
        
        # Verificar si el valor se cambió
        valor_actual = navegador.execute_script("return arguments[0].value;", input_plan)
        print(f"Nuevo valor de planId: {valor_actual}")
        
        # Disparar un evento de cambio para asegurarnos de que la página reaccione al cambio
        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_plan)
        
        # Esperar un momento para que la página procese el cambio
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor del plan: {e}")
        return None

def cambiar_valor_provincia(navegador, nuevo_valor):
    try:
        # Esperar a que se cargue el contenido dinámico
        print("Esperando a que se cargue el contenido dinámico...")
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "provinciaId"))
        )
        
        # Encontrar el elemento input
        input_provincia = navegador.find_element(By.ID, "provinciaId")
        
        # Cambiar el valor usando JavaScript
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_provincia)
        
        # Verificar si el valor se cambió
        valor_actual = navegador.execute_script("return arguments[0].value;", input_provincia)
        print(f"Nuevo valor de provinciaId: {valor_actual}")
        
        # Disparar un evento de cambio para asegurarnos de que la página reaccione al cambio
        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_provincia)
        
        # Esperar un momento para que la página procese el cambio
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor de la provincia: {e}")
        return None

def cambiar_valor_localidad(navegador, nuevo_valor):
    try:
        # Esperar a que se cargue el contenido dinámico
        print("Esperando a que se cargue el contenido dinámico...")
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "localidadId"))
        )
        
        # Encontrar el elemento input
        input_localidad = navegador.find_element(By.ID, "localidadId")
        
        # Cambiar el valor usando JavaScript
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_localidad)
        
        # Verificar si el valor se cambió
        valor_actual = navegador.execute_script("return arguments[0].value;", input_localidad)
        print(f"Nuevo valor de localidadId: {valor_actual}")
        
        # Disparar un evento de cambio para asegurarnos de que la página reaccione al cambio
        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_localidad)
        
        # Esperar un momento para que la página procese el cambio
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor de la localidad: {e}")
        return None

def cambiar_valor_especialidad(navegador, nuevo_valor):
    try:
        # Esperar a que se cargue el contenido dinámico
        print("Esperando a que se cargue el contenido dinámico...")
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "especialidadId"))
        )
        
        # Encontrar el elemento input
        input_especialidad = navegador.find_element(By.ID, "especialidadId")
        
        # Cambiar el valor usando JavaScript
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_especialidad)
        
        # Verificar si el valor se cambió
        valor_actual = navegador.execute_script("return arguments[0].value;", input_especialidad)
        print(f"Nuevo valor de especialidadId: {valor_actual}")
        
        # Disparar un evento de cambio para asegurarnos de que la página reaccione al cambio
        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_especialidad)
        
        # Esperar un momento para que la página procese el cambio
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor de la especialidad: {e}")
        return None

def extraer_datos_profesionales(navegador):
    try:
        # Esperar a que la tabla se cargue
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "listadoTabla"))
        )
        
        # Obtener el HTML de la tabla
        tabla_html = navegador.find_element(By.ID, "listadoTabla").get_attribute('outerHTML')
        
        # Parsear el HTML con BeautifulSoup
        sopa = BeautifulSoup(tabla_html, 'html.parser')
        
        profesionales = []
        
        # Iterar sobre cada prestador
        for prestador in sopa.find_all('tr', class_='prestadorEspecialidad'):
            nombre = prestador.find('div', class_='nombrePrestador').text.strip()
            
            # Obtener los datos del consultorio
            consultorio = prestador.find_next_sibling('tr', class_='consultoriosPrestados')
            if consultorio:
                direccion = consultorio.find('div', class_='direccionPrestador').text.strip()
                localidad = consultorio.find('div', class_='localidadPrestador').text.strip()
                telefono = consultorio.find('td', width='20%').find('div').text.strip()
                email = consultorio.find('td', width='20%').find_all('div')[1].text.strip()
                
                profesional = {
                    'nombre': nombre,
                    'direccion': direccion,
                    'localidad': localidad,
                    'telefono': telefono,
                    'email': email
                }
                
                profesionales.append(profesional)
        
        return profesionales
    except Exception as e:
        print(f"Error al extraer datos de profesionales: {e}")
        return []

def obtener_profesionales(url, valores):
    profesionales = []
    
    opciones_chrome = Options()
    opciones_chrome.add_argument("--headless")
    
    servicio = Service("./chromedriver.exe")
    navegador = webdriver.Chrome(service=servicio, options=opciones_chrome)
    
    try:
        navegador.get(url)
        
        funciones_cambio = {
            "plan": cambiar_valor_plan,
            "provincia": cambiar_valor_provincia,
            "localidad": cambiar_valor_localidad,
            "especialidad": cambiar_valor_especialidad
        }
        
        for nombre, valor in valores.items():
            if nombre in funciones_cambio:
                nuevo_valor = funciones_cambio[nombre](navegador, valor)
                if nuevo_valor is None:
                    raise Exception(f"No se pudo cambiar el valor de {nombre}")
                print(f"El valor de {nombre} se cambió exitosamente a: {nuevo_valor}")
            else:
                print(f"No se reconoce el campo {nombre}")
        
        # Intentar cerrar el aviso de cookies
        try:
            aviso_cookies = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            aviso_cookies.click()
            print("Aviso de cookies cerrado")
        except:
            print("No se encontró aviso de cookies o no se pudo cerrar")
        
        # Hacer clic en el botón de búsqueda
        try:
            boton_buscar = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.ID, "botonBuscar"))
            )
            
            # Intentar hacer clic usando JavaScript
            navegador.execute_script("arguments[0].click();", boton_buscar)
            print("Se hizo clic en el botón de búsqueda usando JavaScript")
        except Exception as e:
            print(f"Error al hacer clic en el botón de búsqueda: {e}")
            
            # Si falla, intentar con Actions
            try:
                actions = ActionChains(navegador)
                actions.move_to_element(boton_buscar).click().perform()
                print("Se hizo clic en el botón de búsqueda usando Actions")
            except Exception as e:
                print(f"Error al hacer clic usando Actions: {e}")
                raise
        
        # Esperar a que la tabla se llene con datos
        try:
            WebDriverWait(navegador, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#listadoTabla tbody tr"))
            )
            print("La tabla se ha llenado con datos")
        except TimeoutException:
            print("La tabla no se llenó con datos en el tiempo esperado")
            
            # Guardar una captura de pantalla para depuración
            navegador.save_screenshot("error_screenshot.png")
            print("Se ha guardado una captura de pantalla para depuración")
            
            # Guardar el HTML de la página para depuración
            with open("error_page.html", "w", encoding="utf-8") as f:
                f.write(navegador.page_source)
            print("Se ha guardado el HTML de la página para depuración")
            
            raise
        
        # Extraer los datos de los profesionales
        profesionales = extraer_datos_profesionales(navegador)
        
        # Imprimir o procesar los datos extraídos
        for profesional in profesionales:
            print(profesional)
        
        print(f"Se encontraron {len(profesionales)} profesionales")
        
    except Exception as e:
        print(f"Error al obtener profesionales: {e}")
    finally:
        navegador.quit()
    
    return profesionales

def guardar_csv(profesionales, nombre_archivo):
    fieldnames = ['nombre', 'direccion', 'localidad', 'telefono', 'email']
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
        escritor.writeheader()
        for profesional in profesionales:
            escritor.writerow(profesional)

if __name__ == "__main__":
    url_base = "https://www.osde.com.ar/index1.html#!cartilla.html"
    valores_adultos = {
        "plan": "51",
        "provincia": "1",
        "localidad": "0",
        "especialidad": "810"
    }
    profesionales_adultos = obtener_profesionales(url_base, valores_adultos)
    guardar_csv(profesionales_adultos, "profesionales_adultos.csv")
    print(f"Se han guardado {len(profesionales_adultos)} profesionales en el archivo CSV.")

    valores_ninios = {
        "plan": "51",
        "provincia": "1",
        "localidad": "0",
        "especialidad": "870"
    }
    profesionales_ninos = obtener_profesionales(url_base, valores_ninios)
    guardar_csv(profesionales_ninos, "profesionales_ninos_adolescentes.csv")
    print(f"Se han guardado {len(profesionales_ninos)} profesionales en el archivo CSV.")

    valores_adultos_zona_oeste = {
        "plan": "21",
        "provincia": "4",
        "localidad": "0",
        "especialidad": "810"
    }
    profesionales_adultos_zona_oeste = obtener_profesionales(url_base, valores_adultos_zona_oeste)
    guardar_csv(profesionales_adultos_zona_oeste, "profesionales_adultos_zona_oeste.csv")
    print(f"Se han guardado {len(profesionales_adultos_zona_oeste)} profesionales en el archivo CSV.")

    valores_adultos_zona_norte = {
        "plan": "21",
        "provincia": "2",
        "localidad": "0",
        "especialidad": "810"
    }
    profesionales_adultos_zona_norte = obtener_profesionales(url_base, valores_adultos_zona_norte)
    guardar_csv(profesionales_adultos_zona_norte, "profesionales_adultos_zona_norte.csv")
    print(f"Se han guardado {len(profesionales_adultos_zona_norte)} profesionales en el archivo CSV.")
