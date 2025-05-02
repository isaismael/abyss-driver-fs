from flask import Blueprint, render_template, url_for, request, flash, redirect
import pandas as pd
import os

from app.models import models
from app.routes.auth import login_required

from app.static.scraper import WebScraper

from app.static.scraperFravega import ScraperFravega

from app.static.tags_dict import TagsDict

home_bp = Blueprint('home', __name__)


@home_bp.route('/home')
@login_required
def home():
    return render_template('home.html')


@home_bp.route('/busqueda')
@login_required

def busqueda():
    return render_template('busqueda.html')

@home_bp.route('/scraper', methods=['GET'])
@login_required
def scraper():
    search = request.args.get('q', '')  # Para GET usamos request.args
    if search:
        url = f"https://listado.mercadolibre.com.ar/{search}#D[A:{search}]"
        scraper = WebScraper()
        info = scraper.extraer_urls(url, tags_dict)
        return render_template('busqueda.html', search=search, info=info)
    return render_template('busqueda.html')

@home_bp.route('/process_excel', methods=['POST'])
@login_required
def process_excel():
    mercadolibre = 'mercadolibre' in request.form
    fravega = 'fravega' in request.form
    
    competidores = []
    
    if fravega:
        competidores.append('Fravega')
        if 'excel' in request.files:
            excel_file = request.files['excel']
            try:
                df = pd.read_excel(excel_file)
                print(df.columns)
                
                lista = df['ID_FRABRICANTE']
                
                tags_dict_instance = TagsDict()
                tags_dict = tags_dict_instance.fravega
                url_search = tags_dict['url_search']
                
                resultados_totales = {
                    'nombre_articulo': [],
                    'costo_actual': [],
                    'utilidad': [],
                    'pvp_nuestro': [],
                    'plan_cuotas': [],
                    'precio_tachado': [],
                    'off': [],
                    'pvp': [],
                    'envio': [],
                    'id_fabricante': [] 
                }

                url_array = []
                
                if lista is not None:
                    for l in lista:
                        url_lista = f"{url_search}{l}"
                        url_array.append(url_lista)
                
                for index, url in enumerate(url_array):
                    scraper = ScraperFravega()
                    scraper_fravega = scraper.search_product_fravega(url, tags_dict)

                    # Primero cargamos los datos que vienen del Excel
                    resultados_totales['nombre_articulo'].append(df['NOMBRES_DEL_ARTICULO'].iloc[index])
                    resultados_totales['costo_actual'].append(df['COSTO ACTUAL'].iloc[index])
                    resultados_totales['utilidad'].append(df['Utilidad'].iloc[index])
                    resultados_totales['pvp_nuestro'].append(df['PVP'].iloc[index])
                    
                    resultados_totales['id_fabricante'].append(lista.iloc[index])

                    # Luego los datos que vienen del scraping
                    if scraper_fravega:
                        for campo in ['plan_cuotas', 'precio_tachado', 'off', 'pvp', 'envio']:
                            resultados_totales[campo].append(scraper_fravega.get(campo, ''))
                    else:
                        # Si no encontró nada, ponemos valores vacíos
                        for campo in ['plan_cuotas', 'precio_tachado', 'off', 'pvp', 'envio']:
                            resultados_totales[campo].append('')
                
                print(resultados_totales)
                return render_template('busqueda.html', info_masiva=resultados_totales)
            
            except Exception as e:
                print(f"Error al procesar el archivo: {str(e)}")
                return render_template('busqueda.html', error=str(e))
                
    return render_template('busqueda.html', error="No se encontró archivo para procesar", competidores=competidores)

    