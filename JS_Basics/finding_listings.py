
from bs4 import BeautifulSoup
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
Options = Options()
Options.headless = True
class Finding_listing():   
    BAT_url = requests.get('https://bringatrailer.com/models/')
    response = BAT_url.text
    BAT_soup = BeautifulSoup(response, 'html.parser')
    car_makes_html = BAT_soup.find_all("a", 'previous-listing-image-link', href = True)
    chosen_url = random.choice(car_makes_html)
    chosen_url = chosen_url['href']
    browser = webdriver.Chrome(options=Options)
    browser.get(chosen_url)
    car_soup = BeautifulSoup(browser.page_source, 'html.parser')
    text = car_soup.find_all('a', {'data-bind' : "attr: { href: url }"})
    chosen_car = random.choice(text)
    chosen_listing = chosen_car['href']
    car_info = {}
    browser.get(chosen_listing)
    listing_soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    car_name = listing_soup.find('h1', {'class': 'post-title listing-post-title'}).text
    car_info['car_name'] = car_name
    car_price = listing_soup.find('span', {'class': 'info-value noborder-tiny'}).text
    car_info['car_price'] = car_price
    car_pic1 = listing_soup.find('div', {'class': 'column column-post-image'}).findChild('img')
    carpic1_src = car_pic1['src']
    car_info['carpic1_src'] = carpic1_src
    carpic2 = listing_soup.find('img', {'class': 'alignnone size-large'})
    carpic2_src = carpic2['src']
    car_info['carpic2_src'] = carpic2_src
    print(chosen_listing)
    car_items = listing_soup.find('div', {'class': 'item'}).text
    car_info['car_items'] = car_items
    car_intro = listing_soup.find ('div', {'class':'post-excerpt'}).findChild().text
    car_info['car_intro'] = car_intro
    print(car_info)
    browser.quit()
   