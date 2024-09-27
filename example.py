import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
# My API key de ScraperAPI
api_key = os.getenv('API_KEY_SCRAPERAPI')
print(f"API_KEY_SCRAPERAPI: {api_key}")
# URL de "Books to Scrape"
url = "http://books.toscrape.com/"

params = {
    "api_key": api_key,
    "url": url,
    "autoparse": "true",
    "keep_headers": "true"
}

try:
    print("Starting Scraping...")
    response = requests.get("http://api.scraperapi.com/", params=params)
    response.raise_for_status()
    html_content = response.content

    with open("books_page.html", "wb") as file:
        file.write(html_content)

    print("HTML was saved in books_page.html")

    # Procesar el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Encontrar todos los libros listados en la página
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        # Extraer título, precio y disponibilidad
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Availability: {availability}")
        print("="*40)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
