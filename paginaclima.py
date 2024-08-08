import json
from selenium.webdriver.common.by import By
from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from basescraper import BaseScraper
class ClimaScraper(BaseScraper):
    def __init__(self, config_file):
        self.config_key = "clima"
        self.columns = ["Dia", "TempMinima", "TempMaxima", "ProbabilidadDeLluvia"]
        super().__init__(config_file)

    def _scrape_data(self):
        days = self.scraper.find_elements(By.XPATH, "//li[contains(@class, 'grid-item dia')]")
        for day in days:
            row_data = []
            for field in self.fields:
                try:
                    field_value = day.find_element(getattr(By, field["selector"]), field["selector_name"]).text
                except:
                    field_value = "No disponible"
                row_data.append(field_value)
            
            if any(value != "No disponible" for value in row_data):
                self.excel_exporter.add_row(row_data)
            else:
                print(f"Datos incompletos para un elemento: {row_data}")