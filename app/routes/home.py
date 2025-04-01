from flask import Blueprint, render_template, url_for, request, flash, redirect
import pandas as pd
import os

from app.models import models

from app.static.scraper import WebScraper
from app.static.scraperMasivo import WebScraperMasivo

home_bp = Blueprint('home', __name__)

tags_dict = {
    'url_ficha': "//a[@class='poly-component__title']",
    'nombre_producto': "//h1[@class='ui-pdp-title']",
    'url_img': "//img[@class='ui-pdp-image ui-pdp-gallery__figure__image']",
    'precio_actual': "//span[@class='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact']",
    'precio_antes': "//s[@class='andes-money-amount ui-pdp-price__part ui-pdp-price__original-value andes-money-amount--previous andes-money-amount--cents-superscript andes-money-amount--compact']",
    'porcentaje_descuento': "//span[@class='andes-money-amount__discount ui-pdp-family--REGULAR']",
    'cuotas': "//p[@id='pricing_price_subtitle']",
    'envio': "//p[@class='ui-pdp-color--BLACK ui-pdp-family--REGULAR ui-pdp-media__title']",
}

@home_bp.route('/home')
def home():
    return render_template('home.html')

@home_bp.route('/busqueda')
def busqueda():
    return render_template('busqueda.html')

@home_bp.route('/scraper', methods=['GET'])
def scraper():
    search = request.args.get('q', '')  # Para GET usamos request.args
    if search:
        url = f"https://listado.mercadolibre.com.ar/{search}#D[A:{search}]"
        scraper = WebScraper()
        info = scraper.extraer_urls(url, tags_dict)
        return render_template('busqueda.html', search=search, info=info)
    return render_template('busqueda.html')

@home_bp.route('/process_excel', methods=['POST'])
def process_excel():
    if 'excel' in request.files:
        excel_file = request.files['excel']
        
        # Leer el archivo Excel
        try:
            df = pd.read_excel(excel_file, header=None)
            # Obtener la primera columna (asumiendo que es la columna 0)
            lista = df.iloc[:, 0]
            
            url = []
            resultados_totales = {
                'nombre_producto': [],
                'url_img': [],
                'precio_actual': [],
                'precio_antes': [],
                'porcentaje_descuento': [],
                'cuotas': [],
                'envio': [],
                'url_ficha': []
            }

            if lista is not None:
                for l in lista:
                    url_lista = f"https://listado.mercadolibre.com.ar/{l}#D[A:{l}]"
                    url.append(url_lista)
            
            for u in url:
                scraper_masivo = WebScraperMasivo()
                info_masiva = scraper_masivo.search_product(u, tags_dict)
                
                # Combinar los resultados de cada búsqueda
                if info_masiva:
                    for key in resultados_totales:
                        resultados_totales[key].extend(info_masiva[key][:5])  # Solo los primeros 5 de cada búsqueda
            
            return render_template('busqueda.html', info_masiva=resultados_totales)
            
        except Exception as e:
            print(f"Error al procesar el archivo: {str(e)}")
            return render_template('busqueda.html', error=str(e))
    
    return render_template('busqueda.html', error="No se encontró archivo para procesar")