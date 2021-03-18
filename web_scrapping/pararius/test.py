#from web_scrapping.pararius import utils_pararius
from urllib.parse import \
    urlsplit, urlunsplit
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    # content = requests.get("https://www.pararius.nl/appartement-te-huur/eindhoven/712f63d5/boutenslaan")
    # soup = BeautifulSoup(content.text, 'html.parser')

    url = 'https://www.pararius.nl/appartement-te-huur/mijdrecht/653f535c/malachiet'
    driver = webdriver.Chrome('C:\\Users\\baghba\\chromedriver.exe')
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    #time.sleep(1)
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".stock-quote")))
    page_source = driver.page_source
    driver.close()

    # HTML parsing part
    soup = BeautifulSoup(page_source, 'html.parser')
    for tag in soup.find_all('main'):
        if tag.has_attr("class"):
            if any("listing-features__description--for_rent_price" in s for s in tag['class']):
                print("pause")
    print(url)
    print(utils_pararius.get_rent_price(soup))

    print("The End!")