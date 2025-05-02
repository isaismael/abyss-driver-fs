import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScraperFravega:
    def __init__(self):
        '''Configuracion de Selenium.'''
        options = Options()
        options.add_argument("--no-sandbox")  # Desactiva el sandboxing
        options.add_argument("--headless")    # Ejecuta en modo headless
        options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memoria
        options.add_argument("--disable-gpu")  # Desactiva la GPU
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)
        
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    # Scraping masivo con excel
    def search_product_fravega(self, url, tags_dict):
        self.driver.get(url)

        try:
            #
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-test-id='modal-wrapper']"))
            )
            #
            input_postal = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input[data-test-id='header-geo-location-form-postal-number']"))
            )
            input_postal.clear()
            input_postal.send_keys("4000")
            #
            btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[data-test-id='button-save-postal-code']"))
            )
            self.driver.execute_script("arguments[0].click();", btn)

            # Esperar que se actualice la página
            WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "div[data-test-id='modal-wrapper']"))
            )

        except Exception as e:
            print(f"Error en modal principal: {e}")

        # Obtener TODOS los enlaces correctamente
        enlace_ficha = []
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, tags_dict['url_ficha']))
            )

            enlaces = self.driver.find_elements(
                By.XPATH, tags_dict['url_ficha'])
            enlace_ficha = [enlace.get_attribute(
                "href") for enlace in enlaces if enlace.get_attribute("href")]

            # Verificar URLs obtenidas
            print("Enlaces encontrados:", enlace_ficha)

        except Exception as e:
            print(f"Error al extraer URLs: {e}")
            return

        plan_cuotas = []
        precio_tachado = []
        off = []
        pvp = []
        envio = []

        # Procesar solo el primer enlace
        if enlace_ficha:
            # Solo tomar el primer enlace
            url_producto = enlace_ficha[0]
            try:
                respuesta = self.session.get(url_producto, headers=self.headers)
                soup = BeautifulSoup(respuesta.content, "html.parser")
                print("\nNavegando a:", url_producto)

                # Usar Selenium para mantener la sesión y cargar la página
                self.driver.get(url_producto)

                # Esperar carga básica de la página
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # extraemos cuotas
                try:
                    # Localizar todos los planes de cuotas
                    planes = self.driver.find_elements(
                        By.CSS_SELECTOR, "div.sc-f6cfc5e5-0.fwGXma:not(.oqTiN)")

                    textos_cuotas = []
                    for plan in planes:
                        try:
                            elemento_texto = plan.find_element(
                                By.CSS_SELECTOR, "span.sc-f6cfc5e5-10.hvWATc")
                            texto = elemento_texto.text.strip()
                            # Limpiar formato y unir
                            texto_limpio = ' '.join(texto.split())
                            textos_cuotas.append(texto_limpio)
                        except Exception as e:
                            print(f"Error procesando un plan: {str(e)}")
                            continue

                    # Unir todos los textos con pipe y guardar
                    cuotas = "|".join(
                        textos_cuotas) if textos_cuotas else ''
                    plan_cuotas.append(cuotas)
                    print(f"Cuotas extraídas: {cuotas}")

                except Exception as e:
                    print(f"Error al extraer datos de {url_producto}: {e}")
                    plan_cuotas.append('')
                    
                try:
                    # Esperamos a que el elemento esté visible
                    wait = WebDriverWait(self.driver, 10)
                    valores_envio = wait.until(EC.presence_of_all_elements_located((By.XPATH, tags_dict['envio'])))

                    # Recorremos los elementos encontrados
                    for v in valores_envio:
                        texto = v.get_attribute("innerText").strip()
                        if texto:  # Solo agregamos si no está vacío
                            envio.append(texto)

                    print("Envío:", envio)
                    if not envio:
                        print("No se encontró texto en los elementos de envío.")
                except Exception as e:
                    print("Error al extraer datos de envío:", e)

                # precio_tachado
                try:
                    # Encuentra el precio tachado
                    precio_tachado_element = soup.find('span', class_='sc-66d25270-0')
                    if precio_tachado_element and precio_tachado_element.text:
                        precio_tachado = precio_tachado_element.text.strip()
                        print(precio_tachado)
                    else:
                        print(f"Precio tachado no encontrado para {url_producto}")
                        precio_tachado = ''
                except Exception as e:
                    print(f"Error al intentar encontrar el precio tachado para {url_producto}: {e}")
                    precio_tachado = ''

                # Descuento
                try:
                    descuento = soup.find('span', class_='sc-e2aca368-0')
                    if descuento and descuento.text:
                        off = descuento.text.strip()
                        print(off)
                    else:
                        print(f"no se encuentra descuento en {url_producto}")
                        descuento = ''
                except Exception as e:
                    print(e)
                    off = ''

                # PVP
                try:
                    precio = soup.find('span', class_='sc-1d9b1d9e-0')
                    if precio and precio.text:
                        pvp = precio.text.strip()
                        print(pvp)
                    else:
                        print(f"no se encuentra precio en {url_producto}")
                        pvp = ''
                except Exception as e:
                    print(e)
                    pvp = ''

            except Exception as e:
                print(f"Error en producto {url_producto}: {str(e)}")

        self.driver.quit()

        self.scraper_fravega = {
            'plan_cuotas': plan_cuotas,
            'precio_tachado': precio_tachado,
            'off': off,
            'pvp': pvp,
            'envio': envio
        }

        print(ScraperFravega)
        return self.scraper_fravega
