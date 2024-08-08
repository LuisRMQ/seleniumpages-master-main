import json
from selenium.webdriver.common.by import By
from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MercadoScraper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.scraper = SeleniumWrapper()
        self.excel_exporter = ExcelExporter(self.output_file)
        self.excel_exporter.set_columns(["Título", "Precio"])

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        site_config = config["mercado_libre"]
        self.url = site_config["url"]
        self.output_file = site_config["output_file"]
        self.search_query = site_config["search_query"]
        self.actions = site_config["actions"]
        self.fields = site_config["fields"]

    def extract_and_export_data(self):
        try:
            self.scraper.open_url(self.url)
            self._perform_actions(self.actions)
            self.excel_exporter.export_to_excel()
        finally:
            self.scraper.close_driver()

    def _perform_actions(self, actions):
        for action in actions:
            selector = action.get('selector')
            selector_name = action.get('selector_name')
            act = action.get('action')
            value = action.get('value')

            try:
                if act == 'send_keys':
                    element = WebDriverWait(self.scraper.driver, 10).until(
                        EC.presence_of_element_located((getattr(By, selector), selector_name))
                    )
                    self.scraper.send_keys(element, value)
                elif act == 'click':
                    element = WebDriverWait(self.scraper.driver, 10).until(
                        EC.element_to_be_clickable((getattr(By, selector), selector_name))
                    )
                    self.scraper.click(element)
                elif act == 'wait_for_element':
                    WebDriverWait(self.scraper.driver, 10).until(
                        EC.presence_of_element_located((getattr(By, selector), selector_name))
                    )
                else:
                    print(f"Acción '{act}' no reconocida.")
            except Exception as e:
                print(f"Error al realizar la acción '{act}': {e}")

        self._scrape_products()

    def _scrape_products(self):
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
