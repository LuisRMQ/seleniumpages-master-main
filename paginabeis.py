import json
from selenium.webdriver.common.by import By
from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from basescraper import BaseScraper

class BeisbolScraper(BaseScraper):
    def __init__(self, config_file):
        self.config_key = "beisbol"
        self.columns = ["Equipo", "Ganados", "Perdidos", "Porcentaje", "Diferencia"]
        super().__init__(config_file)

    def _scrape_data(self):
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