import json
from selenium.webdriver.common.by import By
from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from basescraper import BaseScraper

class MercadoScraper(BaseScraper):
    def __init__(self, config_file):
        self.config_key = "mercado_libre"
        self.columns = ["Título", "Precio"]
        super().__init__(config_file)

    def _scrape_data(self):
        product_cards = self.scraper.find_elements(By.CLASS_NAME, "andes-card")
        for card in product_cards:
            try:
                title = card.find_element(By.CLASS_NAME, self.fields['title_selector']).text
            except:
                title = "No disponible"

            try:
                price = card.find_element(By.CLASS_NAME, self.fields['price_selector']).text
            except:
                price = "No disponible"

            if title != "No disponible" and price != "No disponible":
                self.excel_exporter.add_row([title, price])