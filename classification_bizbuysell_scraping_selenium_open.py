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

# Load the API key from the environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# Config Selenium to use Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.bizbuysell.com/virginia-established-businesses-for-sale/"

# Open the browser and load the page
driver.get(url)

# Wait for Angular to fully load
time.sleep(5)

# Get HTML content once the page has been rendered completely
html_content = driver.page_source

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Close the browser
driver.quit()

data = []

# Find the script that contains the JSON with data
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

        # Append data to the list
        data.append({
            "Name": name,
            "Price": price,
            "Location": location,
            "Description": description,
            "URL": f"https://www.bizbuysell.com{url}"
        })

    # Create a DataFrame with the data
    df = pd.DataFrame(data)

    print(df.head(2))

    df.to_excel("bizbuysell_listings.xlsx", index=False)

    print("The Excel file 'bizbuysell_listings.xlsx' has been created successfully.")
else:
    print("No script with type 'application/ld+json' was found.")

# Function to classify multiple businesses based on names and descriptions
def classify_businesses(businesses):
    messages = [
        {"role": "system", "content": "You are a classification assistant that categorizes businesses based on their names and descriptions."},
        {"role": "user", "content": f"Classify the following businesses: {businesses}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].message.content.strip()

businesses_to_classify = "\n".join([f"Name: {row['Name']}, Description: {row['Description']}" for _, row in df.iterrows()])

classification_results = classify_businesses(businesses_to_classify)

categories = classification_results.split('\n')

if len(categories) < len(df):
    categories += ["Unknown"] * (len(df) - len(categories))

df['Category'] = categories[:len(df)]

print("Business categories have been classified:")
print(df[['Name', 'Category']].head(10))

unique_categories = df['Category'].unique()
print("\nUnique categories found:")
for category in unique_categories:
    print(category)