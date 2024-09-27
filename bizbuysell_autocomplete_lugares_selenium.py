from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import string

# Configurar Selenium para usar Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.bizbuysell.com/"

driver.get(url)

time.sleep(3)

search_input = driver.find_element(By.ID, 'mat-input-0')

# Crear combinaciones de dos letras del alfabeto (bigramas)
letters = string.ascii_lowercase
combinations = [a + b for a in letters for b in letters]

all_suggestions = []

for term in combinations:
    search_input.clear()
    search_input.send_keys(term)
    time.sleep(2)
    # Captura las sugerencias de autocompletado
    suggestions = driver.find_elements(By.CSS_SELECTOR, "mat-option")
    for suggestion in suggestions:
        suggestion_text = suggestion.text
        if suggestion_text not in all_suggestions:
            all_suggestions.append(suggestion_text)

# Cierra el navegador
driver.quit()

# Crear un DataFrame con las sugerencias únicas
df = pd.DataFrame(all_suggestions, columns=["Suggestions"])

# Mostrar las primeras dos sugerencias en consola
print(df.head(2))

# Guardar las sugerencias en un archivo Excel
df.to_excel("autocomplete_suggestions.xlsx", index=False)

print("El archivo 'autocomplete_suggestions.xlsx' ha sido creado exitosamente.")
