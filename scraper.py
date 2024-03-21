import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.julis-bw.de/beschlusssammlung/'

response = requests.get(url)

links = []

if response.status_code == 200:
    html_content = response.text
else:
    print(f"Fehler beim Abrufen der Webseite: Statuscode {response.status_code}")

soup = BeautifulSoup(html_content, 'html.parser')

paragraphs = soup.find_all('div', class_='elementor-column elementor-col-100 elementor-top-column elementor-element elementor-element-a66c805')

for paragraph in paragraphs:
    links.append(paragraph.find('a', href=True).get('href'))

for link in links:
    print(link)