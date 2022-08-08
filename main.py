import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pprint import pprint

driver_path = "C:/Users/nicol/Documents/Development/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

GOOGLE_SHEET_LINK = "https://forms.gle/n8PiQ1ZQ9Sthqx138"
LISTING_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

# Write your code below this line 👇
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept-Language": "en-US",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br"
}

response = requests.get(url=LISTING_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

addresses = [address.getText() for address in soup.find_all(name="address", attrs={"data-test": "property-card-addr"})]
prices = [price.getText() for price in soup.find_all(name="span", attrs={"data-test": "property-card-price"})]
links = [listing.get("href").replace("/b/", "https://www.zillow.com/b/") for listing in
         soup.find_all(name="a", class_="property-card-link")]

print(len(addresses))
print(len(prices))
print(len(links[::2]))

driver.get(GOOGLE_SHEET_LINK)

for i in range(len(links)):
    inputs = driver.find_elements(By.CSS_SELECTOR,
                                  '.whsOnd')
    time.sleep(2)
    inputs[0].send_keys(addresses[i])
    inputs[1].send_keys(prices[i])
    inputs[2].send_keys(links[i])
    submit = driver.find_element(By.CLASS_NAME, "uArJ5e")
    submit.click()
    time.sleep(2)
    try:
        next = driver.find_element(By.CSS_SELECTOR, ".c2gzEf a")
        next.click()
    except:
        pass
    time.sleep(2)
