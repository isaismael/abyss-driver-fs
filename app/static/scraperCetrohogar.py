import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class scraperFravega:
    def __init__(self):
        '''Configuracion de Selenium.'''
        options = Options()
        options.add_argument("--no-sandbox")  # Desactiva el sandboxing
        options.add_argument("--headless")    # Ejecuta en modo headless
        options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memoria
        options.add_argument("--disable-gpu")  # Desactiva la GPU
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        #
        self.driver = webdriver.Chrome(options=options)
        #
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

    def search_product_cetrogar(self, url, tags_dict):
        self.driver.get(url)