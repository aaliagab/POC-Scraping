import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

try:
    print("Starting Scraping...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.content

    with open("books_page_no_scraperapi.html", "wb") as file:
        file.write(html_content)

    print("HTML was saved in books_page.html")

    soup = BeautifulSoup(html_content, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Availability: {availability}")
        print("="*40)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
