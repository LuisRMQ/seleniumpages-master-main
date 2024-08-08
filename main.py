from paginaclima import ClimaScraper
from paginabeis import BeisbolScraper
from paginaml import MercadoScraper
def main():
    

    # json_file_Clima = "clima.json"
    # clima_scraper = ClimaScraper(json_file_Clima)
    # clima_scraper.extract_and_export_data()

  
    json_file_Bes = "beis.json"
    beis_scrapper = BeisbolScraper(json_file_Bes)
    beis_scrapper.extract_and_export_data()

    # json_file_path = "mercado.json"
    # mercado_scraper = MercadoScraper(json_file_path)
    # mercado_scraper.extract_and_export_data()

if __name__ == "__main__":
    main()