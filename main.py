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
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "planId"))
        )
        
        input_plan = navegador.find_element(By.ID, "planId")
        
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_plan)
        
        valor_actual = navegador.execute_script("return arguments[0].value;", input_plan)

        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_plan)
        
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor del plan: {e}")
        return None

def cambiar_valor_provincia(navegador, nuevo_valor):
    try:
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "provinciaId"))
        )
        
        input_provincia = navegador.find_element(By.ID, "provinciaId")
        
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_provincia)
        
        valor_actual = navegador.execute_script("return arguments[0].value;", input_provincia)

        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_provincia)
        
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor de la provincia: {e}")
        return None

def cambiar_valor_localidad(navegador, nuevo_valor):
    try:
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "localidadId"))
        )
        
        input_localidad = navegador.find_element(By.ID, "localidadId")
        
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_localidad)
        
        valor_actual = navegador.execute_script("return arguments[0].value;", input_localidad)

        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_localidad)
        
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor de la localidad: {e}")
        return None

def cambiar_valor_especialidad(navegador, nuevo_valor):
    try:
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "especialidadId"))
        )
        
        input_especialidad = navegador.find_element(By.ID, "especialidadId")
        
        navegador.execute_script(f"arguments[0].value = '{nuevo_valor}';", input_especialidad)
        
        valor_actual = navegador.execute_script("return arguments[0].value;", input_especialidad)
       
        navegador.execute_script("""
            var event = new Event('change');
            arguments[0].dispatchEvent(event);
        """, input_especialidad)
        
        time.sleep(2)
        
        return valor_actual
    except Exception as e:
        print(f"Error al cambiar el valor de la especialidad: {e}")
        return None

def cargar_todos_los_resultados(navegador):
    try:
        while True:
            try:
                boton_cargar_mas = WebDriverWait(navegador, 10).until(
                    EC.element_to_be_clickable((By.ID, "barraCargarMas"))
                )
                navegador.execute_script("arguments[0].scrollIntoView();", boton_cargar_mas)
                time.sleep(1)
                boton_cargar_mas.click()
                time.sleep(2)
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                break
    except Exception as e:
        print(f"Error al cargar todos los resultados: {e}")

def extraer_datos_profesionales(navegador):
    try:
        WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.ID, "listadoTabla"))
        )
        
        tabla_html = navegador.find_element(By.ID, "listadoTabla").get_attribute('outerHTML')
        
        sopa = BeautifulSoup(tabla_html, 'html.parser')
        
        profesionales = []
        
        for prestador in sopa.find_all('tr', class_='prestadorEspecialidad'):
            nombre = prestador.find('div', class_='nombrePrestador').text.strip()
            
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
            else:
                print(f"No se reconoce el campo {nombre}")
        
        try:
            aviso_cookies = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            aviso_cookies.click()
        except:
            pass
        
        try:
            boton_buscar = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.ID, "botonBuscar"))
            )
            navegador.execute_script("arguments[0].click();", boton_buscar)
        except Exception as e:
            print(f"Error al hacer clic en el botón de búsqueda: {e}")
            try:
                actions = ActionChains(navegador)
                actions.move_to_element(boton_buscar).click().perform()
            except Exception as e:
                print(f"Error al hacer clic usando Actions: {e}")
                raise
        
        try:
            WebDriverWait(navegador, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#listadoTabla tbody tr"))
            )
        except TimeoutException:
            print("La tabla no se llenó con datos en el tiempo esperado")
            raise

        cargar_todos_los_resultados(navegador)
        
        profesionales = extraer_datos_profesionales(navegador)
        
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
    print("Obteniendo profesionales adultos...")
    profesionales_adultos = obtener_profesionales(url_base, valores_adultos)
    guardar_csv(profesionales_adultos, "profesionales_adultos.csv")
    print(f"Se han guardado {len(profesionales_adultos)} profesionales en el archivo CSV.")

    valores_ninios = {
        "plan": "51",
        "provincia": "1",
        "localidad": "0",
        "especialidad": "870"
    }
    print("Obteniendo profesionales ninos...")
    profesionales_ninos = obtener_profesionales(url_base, valores_ninios)
    guardar_csv(profesionales_ninos, "profesionales_ninos_adolescentes.csv")
    print(f"Se han guardado {len(profesionales_ninos)} profesionales en el archivo CSV.")

    valores_adultos_zona_oeste = {
        "plan": "21",
        "provincia": "4",
        "localidad": "0",
        "especialidad": "810"
    }
    print("Obteniendo profesionales adultos zona oeste...")
    profesionales_adultos_zona_oeste = obtener_profesionales(url_base, valores_adultos_zona_oeste)
    guardar_csv(profesionales_adultos_zona_oeste, "profesionales_adultos_zona_oeste.csv")
    print(f"Se han guardado {len(profesionales_adultos_zona_oeste)} profesionales en el archivo CSV.")

    valores_adultos_zona_norte = {
        "plan": "21",
        "provincia": "2",
        "localidad": "0",
        "especialidad": "810"
    }
    print("Obteniendo profesionales adultos zona norte...")
    profesionales_adultos_zona_norte = obtener_profesionales(url_base, valores_adultos_zona_norte)
    guardar_csv(profesionales_adultos_zona_norte, "profesionales_adultos_zona_norte.csv")
    print(f"Se han guardado {len(profesionales_adultos_zona_norte)} profesionales en el archivo CSV.")
