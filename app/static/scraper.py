import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self):
        self.info_scrapper = {}

    def extraer_urls(self, url, tags_dict):
        """Extrae URLs y datos de productos usando BeautifulSoup."""
        if url is None:
            raise ValueError("La URL no puede ser None")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Obtener HTML de la página principal
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            enlaces = soup.select(tags_dict['url_ficha'])
            enlace_ficha = [a['href'] for a in enlaces if a.has_attr('href')]
        except Exception as e:
            print(f"Error al extraer URLs: {e}")
            return

        # Inicializar listas
        nombre_producto = []
        url_img = []
        precio_actual = []
        precio_antes = []
        porcentaje_descuento = []
        cuotas = []
        envio = []

        for recorrido in enlace_ficha:
            try:
                r = requests.get(recorrido, headers=headers)
                s = BeautifulSoup(r.content, 'html.parser')

                def get_text(selector):
                    tag = s.select_one(selector)
                    return tag.text.strip() if tag else ''
                
                def get_attr(selector, attr):
                    tag = s.select_one(selector)
                    return tag[attr] if tag and tag.has_attr(attr) else ''

                nombre_producto.append(get_text(tags_dict['nombre_producto']))
                url_img.append(get_attr(tags_dict['url_img'], 'src'))
                precio_actual.append(get_text(tags_dict['precio_actual']))
                precio_antes.append(get_text(tags_dict['precio_antes']))
                porcentaje_descuento.append(get_text(tags_dict['porcentaje_descuento']))
                cuotas.append(get_text(tags_dict['cuotas']))
                envio.append(get_text(tags_dict['envio']))

            except Exception as e:
                print(f"Error al procesar {recorrido}: {e}")

        self.info_scrapper = {
            'nombre_producto': nombre_producto,
            'url_img': url_img,
            'precio_actual': precio_actual,
            'precio_antes': precio_antes,
            'porcentaje_descuento': porcentaje_descuento,
            'cuotas': cuotas,
            'envio': envio,
            'url_ficha': enlace_ficha
        }

        return self.info_scrapper
