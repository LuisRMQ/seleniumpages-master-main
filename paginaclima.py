import json
from seleniummethods import SeleniumWrapper
from excelexport import ExcelExporter
from selenium.webdriver.common.by import By

class ClimaScraper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.scraper = SeleniumWrapper()
        self.excel_exporter = ExcelExporter(self.site_config["output_file"])
        self.excel_exporter.set_columns(["Dia", "TempMinima", "TempMaxima", "ProbabilidadDeLluvia"])

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        self.site_config = config["clima"]

    def extract_and_export_data(self):
        try:
            self.scraper.open_url(self.site_config["url"])

            for element_config in self.site_config["elements"]:
                if element_config["action"] == "scroll_into_view":
                    div_element = self.scraper.find_element(getattr(By, element_config["selector"]), element_config["selector_name"])
                    self.scraper.execute_script("arguments[0].scrollIntoView(true);", div_element)

                elif element_config["action"] == "find_elements":
                    days = self.scraper.find_elements(getattr(By, element_config["selector"]), element_config["selector_name"])
                    for day in days:
                        row_data = []
                        for field in element_config["fields"]:
                            try:
                                field_value = day.find_element(getattr(By, field["selector"]), field["selector_name"]).text
                            except:
                                field_value = "No disponible"
                            row_data.append(field_value)
                        
                        if any(value != "No disponible" for value in row_data):
                            self.excel_exporter.add_row(row_data)
                        else:
                            print(f"Datos incompletos para un elemento: {row_data}")

            self.excel_exporter.export_to_excel()
        finally:
            self.scraper.close_driver()
