import requests
from bs4 import BeautifulSoup
import time

class WebScraperMasivo:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def search_product(self, url, tags_dict):
        response = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extraer URLs de fichas
        urls_ficha = []
        for a_tag in soup.select(tags_dict['url_ficha']):
            href = a_tag.get("href")
            if href:
                urls_ficha.append(href)

        resultados = {
            'nombre_producto': [],
            'url_img': [],
            'precio_actual': [],
            'precio_antes': [],
            'porcentaje_descuento': [],
            'cuotas': [],
            'envio': [],
            'url_ficha': []
        }

        for link in urls_ficha[:5]:  # Limitar a 5
            try:
                r = self.session.get(link, headers=self.headers)
                s = BeautifulSoup(r.content, "html.parser")

                def get_text(selector):
                    tag = s.select_one(selector)
                    return tag.get_text(strip=True) if tag else ''

                def get_img_url():
                    # 1. Usar el selector del dict si funciona
                    tag = s.select_one(tags_dict['url_img'])
                    if tag and tag.get("src"):
                        return tag["src"]
                    if tag and tag.get("data-src"):
                        return tag["data-src"]
                    
                    # 2. Buscar meta og:image
                    meta_img = s.find("meta", property="og:image")
                    if meta_img:
                        return meta_img.get("content", "")
                    
                    # 3. Buscar cualquier imagen en galería
                    fallback = s.select_one("img.ui-pdp-image")
                    if fallback and fallback.get("src"):
                        return fallback["src"]

                    return ''

                resultados['nombre_producto'].append(get_text(tags_dict['nombre_producto']))
                resultados['url_img'].append(get_img_url())
                resultados['precio_actual'].append(get_text(tags_dict['precio_actual']))
                resultados['precio_antes'].append(get_text(tags_dict['precio_antes']))
                resultados['porcentaje_descuento'].append(get_text(tags_dict['porcentaje_descuento']))
                resultados['cuotas'].append(get_text(tags_dict['cuotas']))
                resultados['envio'].append(get_text(tags_dict['envio']))
                resultados['url_ficha'].append(link)

                time.sleep(1)

            except Exception as e:
                print(f"Error al procesar {link}: {e}")

        return resultados
