import json
from selenium.webdriver.common.by import By
from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseScraper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.scraper = SeleniumWrapper()
        self.excel_exporter = ExcelExporter(self.output_file)

        if hasattr(self, 'columns'):
            self.excel_exporter.set_columns(self.columns)
        elif hasattr(self, 'fields'):
            self.excel_exporter.set_fields(self.fields)

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        site_config = config[self.config_key]
        self.url = site_config["url"]
        self.output_file = site_config["output_file"]
        self.actions = site_config["actions"]

        if 'table' in site_config:
            self.table_config = site_config["table"]
            self.columns = [col.get('name') for col in self.table_config.get("columns", [])]
        else:
            self.fields = site_config.get("fields", {})


    def extract_and_export_data(self):
        try:
            self.scraper.open_url(self.url)
            self._perform_actions(self.actions)
            self._scrape_data()
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
                elif act == 'scroll_into_view':
                    element = self.scraper.find_element(getattr(By, selector), selector_name)
                    self.scraper.execute_script("arguments[0].scrollIntoView(true);", element)
                elif act == 'guardarDatos':
                    self._scrape_data()
                else:
                    print(f"Acción '{act}' no reconocida.")
            except Exception as e:
                print(f"Error al realizar la acción '{act}': {e}")

    def _scrape_data(self):
        raise NotImplementedError("Subclasses must implement _scrape_data method.")