import random
from types import NoneType
import requests
import re
import string
from bs4 import BeautifulSoup
import json
from lists import chosen_list
class game_infrastructure():
    def __init__(self, wiki_link, info_dict, car_data_table, image, a_list, chosen_data, result) -> None: # for every run of the game, initialize these variables.
           
            self.result = result
            self.wiki_link = wiki_link
            self.info_dict = info_dict
            self.car_data_table = car_data_table
            self.image = image
            self.a_list = a_list
            self.chosen_data = chosen_data
    
    @classmethod
    def find_car(self):
        self.a_list = []
        exclusions = ['Category', 'ISBN', 'Template', 'Special', 'Wikipedia', 'http', 'foundation', 'Help', 'File']
        url = requests.get(chosen_list).text
        soup = BeautifulSoup(url, "html.parser")
        if soup.findAll("tr"):
            tabledata = soup.findAll("tr")
            for table in tabledata:
                a_tag = table.find_all("a")
                if a_tag:   
                    for link in a_tag:
                        if 'href' in link.attrs:
                            href = link['href']
                            if '/wiki' in href and not any(excl in href for excl in exclusions):
                                self.a_list.append(href) 
                            else:
                                continue
                        
          
        else:
            tabledata = soup.findAll("li")
            for list in tabledata:
                a_tag = list.find_all("a")
                if a_tag:   
                    for link in a_tag:
                        if 'href' in link.attrs:
                            href = link['href']
                            if '/wiki' in href and not any(excl in href for excl in exclusions):
                                self.a_list.append(href) 
                            else:
                                continue
            
 
        self.chosen_data = random.choice(self.a_list)
        return self.chosen_data




    @classmethod
    def verify_model(self):
        self.result = game_infrastructure.find_car()
        url2 = requests.get(f'https://en.wikipedia.org{self.result}').text
        soup2 = BeautifulSoup(url2, 'html.parser')
        
        try:
            infobox = soup2.find("table", {'class': 'infobox hproduct'})
            for table in infobox:
                        rows = table.findChildren(['th', 'tr'])
                        for row in rows:
                            titles = row.findChildren('th')
                            while 'Products' in titles or 'Product type' in titles:
                                 game_infrastructure.verify_model()
            self.target_car = soup2.find("th", {'infobox-above fn'}).text
            print(self.target_car)
            print(self.result)
            return self.target_car

        except TypeError:
             game_infrastructure.verify_model()
        return self.target_car, self.result     
    @classmethod
    def wiki_search(self):
        self.info_dict = {} # the dictionary where all of the car info goes
        self.wiki_link = requests.get(f'https://en.wikipedia.org{self.result}')
        game_infrastructure.soup1 = BeautifulSoup(self.wiki_link.text, 'html.parser')
        game_infrastructure.car_data_table = game_infrastructure.soup1.find("table", {'class': 'infobox hproduct'})

    @classmethod
    def image_search(self):
        self.image_link = requests.get(f'https://www.google.com/search?q={self.target_car}&sxsrf=ALeKk03xBalIZi7BAzyIRw8R4_KrIEYONg:1620885765119&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjv44CC_sXwAhUZyjgGHSgdAQ8Q_AUoAXoECAEQAw&cshid=1620885828054361')
        game_infrastructure.soup2 = BeautifulSoup(self.image_link.content, 'html.parser')
        self.image = game_infrastructure.soup2.find("img", {"class" : "yWs4tf"}).get('src')
        game_infrastructure.info_dict['image'] = game_infrastructure.image
        print(game_infrastructure.info_dict)
    
    @classmethod
    def data_gathering(self):
        for table in game_infrastructure.car_data_table:
            rows = table.findChildren(['th', 'tr'])
            for row in rows:
                titles = row.findChildren('th')
                cells = row.findChildren('td')
                for cell in cells: # trying to filter out as much extraneous HTML or poor formatting that gets accidentally caught by the scraper.
                    cell_re = re.sub(r'\xa0', '', cell.text)
                    cell_re2 = re.sub(r'\[\d\]', '', cell_re)
                    cell_re3 = re.sub(r'$ | ^', '\n', cell_re2)
                    cell_re4 = cell_re3.replace('\\u', ' ')
                    cell_re5 = re.sub(r'([a-z])([0-9])', r'\1, \2', cell_re4) #
                    cell_re6 = re.sub(r'([a-z])([A-Z])', r'\1, \2', cell_re5) # lowercase following uppercase
                    cell_re7 = re.sub(r'(\))([A-Z])', r'\1, \2', cell_re6) #paren w/uppercase
                    cell_re8 = re.sub(r'(\))([a-z])', r'\1, \2', cell_re7) # paren w letter
                    cell_re9 = re.sub(r'(\))([0-9])', r'\1, \2 ', cell_re8) # paren w num
                    cell_re10 = re.sub(r'(\d{4})(\d{4})',  r'\1,  \2' , cell_re9) # 4 digit number
                    cell_re11 = cell_re10
                    cell_re12 = re.sub(r'([0-9])([A-Z])', r'\1, \2', cell_re11)
                    cell_re13 = re.sub(r'(\d{4})(\d)',  r'\1, \2' , cell_re12)
                    for title in titles:
                        title_re = re.sub(r'\xa0', ' ', title.text)
                        game_infrastructure.info_dict[title_re] = cell_re13
        return game_infrastructure.car_data_table
    
    def main():
        try:
            game_infrastructure.verify_model()
            game_infrastructure.wiki_search()
            game_infrastructure.data_gathering()
            game_infrastructure.image_search()
            #while 'This article needs additional citations for verification' in game_infrastructure.car_data_table.text or 'Wikipedia does not have an article with this exact name' in game_infrastructure.car_data_table.text:
               
        except  AttributeError:
            game_infrastructure.main()
player_1 = game_infrastructure.main()