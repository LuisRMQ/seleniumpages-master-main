import json
from selenium.webdriver.common.by import By
from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BeisbolScraper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.scraper = SeleniumWrapper()
        self.excel_exporter = ExcelExporter(self.output_file)
        self.excel_exporter.set_columns(["Equipo", "Ganados", "Perdidos", "Porcentaje", "Diferencia"])

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        site_config = config["beisbol"]
        self.url = site_config["url"]
        self.output_file = site_config["output_file"]
        self.actions = site_config["actions"]
        self.table_config = site_config["table"]

    def extract_and_export_data(self):
        try:
            self.scraper.open_url(self.url)
            time.sleep(10)  # Consider replacing this with WebDriverWait for better stability

            for action in self.actions:
                self._perform_action(action)

            self._scrape_table()
            self.excel_exporter.export_to_excel()
        finally:
            self.scraper.close_driver()

    def _perform_action(self, action):
        selector = action.get('selector')
        selector_name = action.get('selector_name')
        act = action.get('action')
        optional = action.get('optional', False)

        try:
            if act == 'click':
                element = WebDriverWait(self.scraper.driver, 10).until(
                    EC.element_to_be_clickable((getattr(By, selector), selector_name))
                )
                self.scraper.click(element)
            elif act == 'scroll_into_view':
                element = WebDriverWait(self.scraper.driver, 10).until(
                    EC.presence_of_element_located((getattr(By, selector), selector_name))
                )
                self.scraper.execute_script("arguments[0].scrollIntoView(true);", element)
            elif act == 'guardarDatos':
                self._scrape_table()
            else:
                print(f"Acción '{act}' no reconocida.")
        except Exception as e:
            if not optional:
                print(f"Error al realizar la acción '{act}': {e}")

    def _scrape_table(self):
        table_config = self.table_config
        tbody = self.scraper.find_element(getattr(By, table_config["tbody_selector"]), table_config["tbody_name"])
        rows = tbody.find_elements(getattr(By, table_config["row_selector"]), table_config["row_name"])

        for row in rows:
            row_data = []
            for col in table_config["columns"]:
                data_col = col["data_col"]
                try:
                    cell = row.find_element(By.XPATH, f".//td[@data-col='{data_col}']").text
                except:
                    cell = "No disponible"
                row_data.append(cell)
            self.excel_exporter.add_row(row_data)
