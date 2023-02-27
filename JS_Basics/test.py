# import requests, random
# from bs4 import BeautifulSoup
# wiki_url1 = requests.get(f'https://en.wikipedia.org/wiki/Category:Lists_of_cars')
# soup = BeautifulSoup(wiki_url1.text, 'html.parser')
# table = soup.findAll("div",{"class":"mw-category-group"}) #finds the massive table with car makes, models
# tab = random.choice(table)
# links = soup.find_all('a')
# link = random.choice(links)
# random_link = link['href']
# wiki_url2 = requests.get(f'https://en.wikipedia.org{random_link}')
# soup = BeautifulSoup(wiki_url2.text, 'html.parser')
# tabdata = soup.findAll("b")
# print(tabdata)
# link = random.choice(tabdata)
# random_link2 = link['href']
# print(random_link2)


import requests, random
from bs4 import BeautifulSoup

a = 9
b = 5
c = 4
expression = a + b * c
print(expression)