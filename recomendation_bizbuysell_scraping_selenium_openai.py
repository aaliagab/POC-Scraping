from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# Config Selenium para usar Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.bizbuysell.com/virginia-established-businesses-for-sale/"

# Abro el navegador y carga la página
driver.get(url)

# Espera para que Angular cargue completamente
time.sleep(5)

# Contenido HTML una vez que la página haya sido renderizada completamente
html_content = driver.page_source

# BeautifulSoup para parsear el HTML
soup = BeautifulSoup(html_content, "html.parser")

# Cierra el navegador
driver.quit()

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

        data.append({
            "Name": name,
            "Price": price,
            "Location": location,
            "Description": description,
            "URL": f"https://www.bizbuysell.com{url}"
        })

    df = pd.DataFrame(data)

    print(df.head(2))

    df.to_excel("bizbuysell_listings.xlsx", index=False)

    print("El archivo Excel 'bizbuysell_listings.xlsx' ha sido creado exitosamente.")
else:
    print("No se encontró el script con tipo 'application/ld+json'")

def obtener_recomendaciones(descripcion_usuario):
    mensajes = [
        {"role": "system", "content": "Eres un asistente que recomienda negocios según la descripción del usuario."},
        {"role": "user", "content": f"Busco recomendaciones basadas en: {descripcion_usuario}. Aquí están los negocios: {data}"}
    ]
    
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensajes,
        temperature=0.2,
        top_p=0.9,      
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return respuesta.choices[0].message.content

descripcion_usuario = "Busco un restaurante familiar en Virginia con buenas reseñas."
recomendaciones = obtener_recomendaciones(descripcion_usuario)

print("Recomendaciones de negocios:")
print(recomendaciones)
