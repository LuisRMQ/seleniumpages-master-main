from paginaclima import ClimaScraper
from paginabeis import BeisbolScraper
from paginaml import MercadoScraper



def main():
   
    json_file_Clima = "clima.json"
    json_file_Bes = "beis.json"
    json_file_path = "mercado.json"

    clima_scraper = ClimaScraper(json_file_Clima)
    beis_scrapper = BeisbolScraper(json_file_Bes)
    mercado_scraper = MercadoScraper(json_file_path)

    clima_scraper.extract_and_export_data()
    beis_scrapper.extract_and_export_data()
    mercado_scraper.extract_and_export_data()

if __name__ == "__main__":
    main()