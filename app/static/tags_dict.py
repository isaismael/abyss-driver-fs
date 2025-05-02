class TagsDict:
    def __init__(self):

        self.fravega = {
            # esta url es la que tomo para hacer comenzar la busqueda del o los productos
            'url_search': 'https://www.fravega.com/l/?keyword=',
            # fravega tiene una ventana flotante que nos pide insertar nuestro codigo postal
            # debemos completar este campo, para poder seguir con el scraping
            'input_location': "//input[@id='header-geo-location-form-postal-number']",
            'btn_guardar': "//button[@id='button-save-postal-code']",
            # de esta tag tenemos que sacar el href para poder ingresar a la ficha del producto
            'url_ficha': "//a[@class='sc-4007e61d-0 dcODtv']",
            # generalmente en cuotas tendremos un array para recorrer
            'plan_cuotas': "//div[@class='sc-f6cfc5e5-4 gJMUXT']",
            'precio_tachado': "span.sc-66d25270-0 sc-2628e4d4-4 eiLwiO kGdyWX",
            'off': "//span[@class='sc-e2aca368-0 sc-2628e4d4-5 juwGno ehTQUi']",
            'pvp': "//span[@class='sc-1d9b1d9e-0 sc-2628e4d4-3 OZgQ jLjuuY']",
            'envio': "//p[@class='sc-477ee6eb-1 jBTwcO']",
        }

        # podemos ver que las etiquetas tiene diferente sintaxis
        # esto pasa porque a meli se lo puede scrapear con bs4
        self.mercadolibre = {
            'url_ficha': 'a.poly-component__title',
            'nombre_producto': 'h1.ui-pdp-title',
            'url_img': 'img.ui-pdp-image.ui-pdp-gallery__figure__image',
            'precio_actual': 'span.andes-money-amount.ui-pdp-price__part.andes-money-amount--cents-superscript.andes-money-amount--compact',
            'precio_antes': 's.andes-money-amount.ui-pdp-price__part.ui-pdp-price__original-value.andes-money-amount--previous.andes-money-amount--cents-superscript.andes-money-amount--compact',
            'porcentaje_descuento': 'span.andes-money-amount__discount.ui-pdp-family--REGULAR',
            'cuotas': 'p#pricing_price_subtitle',
            'envio': 'p.ui-pdp-color--BLACK.ui-pdp-family--REGULAR.ui-pdp-media__title',
        }

        self.cetrogar = {
            'ubicacion': '',
            'url_ficha': '',
            'nombre_producto': '',
            'precio_actual': '',
            'precio_antes': '',
            'porcentaje_descuento': '',
            'cuotas': '',
            'envio': '',
        }
