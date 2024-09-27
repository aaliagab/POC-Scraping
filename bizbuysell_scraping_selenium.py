from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

# Configura Selenium para usar Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL objetivo
url = "https://www.bizbuysell.com/virginia-established-businesses-for-sale/"

# Abre el navegador y carga la página
driver.get(url)

# Espera para que Angular cargue completamente
time.sleep(5)  # Ajusta el tiempo según sea necesario

# Obtén el contenido HTML una vez que la página haya sido renderizada completamente
html_content = driver.page_source

# Usa BeautifulSoup para parsear el HTML
soup = BeautifulSoup(html_content, "html.parser")

# Cierra el navegador
driver.quit()

# Encontrar el script que contiene el JSON con datos
script_tag = soup.find("script", {"type": "application/ld+json"})
if script_tag:
    json_data = json.loads(script_tag.string)
    listings = json_data.get("about", [])
    for listing in listings:
        item = listing.get("item", {})
        
        # Usar .get() para evitar errores si las claves no existen
        name = item.get("name", "No name available")
        offers = item.get("offers", {})
        price = offers.get("price", "No price available")
        location = offers.get("availableAtOrFrom", {}).get("address", {}).get("addressRegion", "No location available")
        description = item.get("description", "No description available")
        url = item.get("url", "#")

        print(f"Name: {name}")
        print(f"Price: {price} USD")
        print(f"Location: {location}")
        print(f"Description: {description}")
        print(f"URL: https://www.bizbuysell.com{url}")
        print("="*40)
else:
    print("No se encontró el script con tipo 'application/ld+json'")
