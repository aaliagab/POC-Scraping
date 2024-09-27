from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import pandas as pd

# Config Selenium to use Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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

# Lista para almacenar los datos
data = []

# Encontrar el script que contiene el JSON con datos
script_tag = soup.find("script", {"type": "application/ld+json"})
if script_tag:
    json_data = json.loads(script_tag.string)
    listings = json_data.get("about", [])
    for listing in listings:
        item = listing.get("item", {})        
        name = item.get("name", "No name available")
        offers = item.get("offers", {})
        price = offers.get("price", "No price available")
        location = offers.get("availableAtOrFrom", {}).get("address", {}).get("addressRegion", "No location available")
        description = item.get("description", "No description available")
        url = item.get("url", "#")

        # Almacenar los datos en el diccionario
        data.append({
            "Name": name,
            "Price": price,
            "Location": location,
            "Description": description,
            "URL": f"https://www.bizbuysell.com{url}"
        })

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    # Mostrar los dos primeros registros en la consola
    print(df.head(2))

    # Guardar el DataFrame en un archivo Excel
    df.to_excel("bizbuysell_listings.xlsx", index=False)

    print("El archivo Excel 'bizbuysell_listings.xlsx' ha sido creado exitosamente.")
else:
    print("No se encontró el script con tipo 'application/ld+json'")
