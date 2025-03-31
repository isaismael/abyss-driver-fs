from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebScraper:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        """Configura el driver de Selenium."""
        options = Options()
        options.add_argument("--no-sandbox")  # Desactiva el sandboxing
        options.add_argument("--headless")    # Ejecuta en modo headless
        options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memoria
        options.add_argument("--disable-gpu")  # Desactiva la GPU
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)

    def extraer_urls(self, url, tags_dict):
        """Extrae URLs y datos de productos."""
        self.url = url
        if self.url is None:
            raise ValueError("La URL no puede ser None")

        self.setup_driver()
        self.driver.get(self.url)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Extraer todos los enlaces de la página
            enlace_ficha = []
            enlaces = self.driver.find_elements(By.XPATH, tags_dict['url_ficha'])
            for enlace in enlaces:
                href = enlace.get_attribute("href")
                if href:
                    enlace_ficha.append(href)

        except Exception as e:
            print(f"Error al extraer URLs: {e}")
            return

        # Extraer datos de cada ficha
        nombre_producto = []
        precio_actual = []
        precio_antes = []
        porcentaje_descuento = []
        cuotas = []
        envio = []
        
        if enlace_ficha:
            print(f'No está vacío, tiene longitud: {len(enlace_ficha)}')
            # recorremos las url
            for recorrido in enlace_ficha:
                # empezamos a recorrer los url de ficha productos y extramos la info
                # extraemos nombre_producto
            
                try:
                    self.driver.get(recorrido)
                    
                    try:
                        WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body")))
                    except Exception as e:
                        print(e)
                    
                    # extraemos el name
                    try:
                        nombre = self.driver.find_element(By.XPATH, tags_dict['nombre_producto']).text
                        nombre_producto.append(nombre)
                    except Exception as e:
                        print(f"Error al extraer datos de {recorrido}: {e}")
                        nombre_producto.append('')
                    
                    # extraemos precio_actual
                    try:
                        precio = self.driver.find_element(By.XPATH, tags_dict['precio_actual']).text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
                        precio_actual.append(precio)
                    except Exception as e:
                        print(f"Error al extraer datos de {recorrido}: {e}")
                        precio_actual.append('')
                    
                    # extramos precio_antes
                    try:
                        pre_antes = self.driver.find_element(By.XPATH, tags_dict['precio_antes']).text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
                        precio_antes.append(pre_antes)
                    except Exception as e:
                        print(f"Error al extraer datos de {recorrido}: {e}")
                        precio_actual.append('')
                    
                    # extraemos porcentaje de descuento
                    try:
                        descuento = self.driver.find_element(By.XPATH, tags_dict['porcentaje_descuento']).text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
                        porcentaje_descuento.append(descuento)
                    except Exception as e:
                        print(f"Error al extraer datos de {recorrido}: {e}")
                        porcentaje_descuento.append('')
                        
                    # extraemos cuotas o cuotas mas alta
                    try:
                        tag_cuotas = self.driver.find_element(By.XPATH, tags_dict['cuotas']).text.replace('\n', '').replace('\r', '').replace('\t', '').strip()
                        cuotas.append(tag_cuotas)
                    except Exception as e:
                        print(f"Error al extraer datos de {recorrido}: {e}")
                        cuotas.append('')
                        
                    # extraemos info envio
                    try:
                        envio_info = self.driver.find_element(By.XPATH, tags_dict['envio']).text()
                        envio.append(envio_info)
                    except Exception as e:
                        print(f"Error al extraer datos de {recorrido}: {e}")
                        envio.append('')
                        
                        
                except Exception as e:
                    return print(e)
                
        # Cerrar el navegador
        self.driver.quit()

        self.info_scrapper = {
            'nombre_producto': nombre_producto,
            'precio_actual': precio_actual,
            'precio_antes': precio_antes,
            'porcentaje_descuento': porcentaje_descuento,
            'cuotas': cuotas,
            'envio': envio,
            'url_ficha': enlace_ficha
        }
        
        
        #print(self.info_scrapper)
        return self.info_scrapper