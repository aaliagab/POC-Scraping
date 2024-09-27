import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os

load_dotenv()
# My API key de ScraperAPI
api_key = os.getenv('API_KEY_SCRAPERAPI')
print(f"API_KEY_SCRAPERAPI: {api_key}")

url = "https://www.bizbuysell.com/virginia-established-businesses-for-sale/"

# Parámetros para la solicitud de ScraperAPI
params = {
    "api_key": api_key,
    "url": url
}

try:
    print("Starting Scraping...")
    response = requests.get("https://api.scraperapi.com/", params=params)
    response.raise_for_status()
    html_content = response.content

    with open("bizbuysell_page.html", "wb") as file:
        file.write(html_content)

    print("HTML was saved in bizbuysell_page.html")

    # Procesar el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Encontrar el script que contiene el JSON con datos
    script_tag = soup.find("script", {"type": "application/ld+json"})
    if script_tag:
        json_data = json.loads(script_tag.string)
        listings = json_data.get("about", [])
        for listing in listings:
            item = listing["item"]
            name = item["name"]
            price = item["offers"]["price"]
            location = item["offers"]["availableAtOrFrom"]["address"]["addressRegion"]
            description = item["description"]
            url = item["url"]
            
            print(f"Name: {name}")
            print(f"Price: {price} USD")
            print(f"Location: {location}")
            print(f"Description: {description}")
            print(f"URL: https://www.bizbuysell.com{url}")
            print("="*40)
    else:
        print("No se encontró el script con tipo 'application/ld+json'")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
