import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd


driver = webdriver.Chrome()
url = 'https://www.julis-bw.de/beschlusssammlung/'
driver.get(url)

links = []
pagination_start = 2
time.sleep(10)

data_entries = []

while True:
    # Verwende CSS-Selektor, um Elemente mit mehreren Klassen zu finden
    content_elements = driver.find_elements(By.CSS_SELECTOR, '.elementor-column.elementor-col-100.elementor-top-column.elementor-element.elementor-element-a66c805')
    for element in content_elements:
        # Verwende .get_attribute('href'), um den href-Wert zu erhalten
        links.append(element.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    
    try:
        next_page_button = driver.find_element(By.XPATH, f'//div[@class="jet-filters-pagination__item" and @data-value="{pagination_start}"]')
        pagination_start += 1
        next_page_button.click()

        time.sleep(2)
    except Exception as e:
        print("Keine weitere Seite gefunden oder Fehler aufgetreten:", e)
        for link in links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('div', class_='elementor-element elementor-element-3d156863 elementor-widget elementor-widget-heading').text
            content = soup.find('div', class_='elementor-element elementor-element-5aabca2 elementor-widget elementor-widget-theme-post-content').text
            data_entries.append({'title': title, 'content': content, 'link': link})
        break

# Denken Sie daran, den Driver am Ende zu schließen
driver.quit()

df = pd.DataFrame(data_entries)
df.to_csv('julis_bw_beschluesse.csv', index=False)
df.to_excel('julis_bw_beschluesse.xlsx', index=False)