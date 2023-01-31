import random
from types import NoneType
import requests
import re
import string
from bs4 import BeautifulSoup
import json
class game_infrastructure():
    def __init__(self, chosen_letter, kbb_url, wiki_link, car_model, car_make, info_dict, car_data_table, image) -> None: # for every run of the game, initialize these variables.
            self.chosen_letter = chosen_letter
            self.kbb_url = kbb_url
            self.wiki_link = wiki_link
            self.car_model = car_model
            self.car_make = car_make
            self.info_dict = info_dict
            self.car_data_table = car_data_table
            self.image = image
    @classmethod
    def list_of_letters(self):
        list_of_letters_lowercase = list(string.ascii_lowercase)
        self.chosen_letter = random.choice(list_of_letters_lowercase)
        return self.chosen_letter #the Kelley Blue Book reference uses an A-Z setup to find cars, so it chooses a random letter
    @classmethod
    def kbb_search(self):
        self.kbb_url = requests.get(f'https://www.kbb.com/car-make-model-list/used/{self.chosen_letter}/model/')
        soup = BeautifulSoup(self.kbb_url.text, 'html.parser')
        table = soup.find("tbody",{"class":"css-ap66tw ee33uo34"}) #finds the massive table with car makes, models
        tab = table.findAll('tr')
        link = random.choice(tab) # chooses a random row
        car_model_html = link.find('div', {"class":"css-z687n ee33uo36"})
        self.car_model = car_model_html.text
        car_make_html = car_model_html.find_next() #car makes are displayed following the model.
        self.car_make = car_make_html.text
        self.car_model = self.car_model.replace(' ',  '_')
        self.car_model = self.car_model.replace('-',  '_')
        self.car_make = self.car_make.replace(' ', '_')
        if len(self.car_make) > 3:
            self.car_make = string.capwords(self.car_make, sep='_') #meant to exclude abbreviation makes like BMW, AMG
        if len(self.car_model) > 3: 
            self.car_model = string.capwords(self.car_model, sep='_') # same with model names like X5M
        else:
            return self.car_make, self.car_model
    
    @classmethod
    def wiki_search(self):
        self.target_car = f'{self.car_make} {self.car_model}'
        print(self.target_car)
        self.target_car2 = re.sub(r'([a-z])([A-Z])', r'\1 \2', self.target_car)  #This is the car name that the program has selected.
        self.info_dict = {} # the dictionary where all of the car info goes
        self.wiki_link = requests.get(f'https://en.wikipedia.org/wiki/{self.car_make}_{self.car_model}')
        game_infrastructure.soup1 = BeautifulSoup(self.wiki_link.text, 'html.parser')
        game_infrastructure.car_data_table = game_infrastructure.soup1.find("table", {'class': 'infobox hproduct'})

    @classmethod
    def image_search(self):
        self.image_link = requests.get(f'https://www.google.com/search?q={self.car_make}+{self.car_model}&sxsrf=ALeKk03xBalIZi7BAzyIRw8R4_KrIEYONg:1620885765119&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjv44CC_sXwAhUZyjgGHSgdAQ8Q_AUoAXoECAEQAw&cshid=1620885828054361')
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
            game_infrastructure.list_of_letters()
            game_infrastructure.kbb_search()
            game_infrastructure.wiki_search()
            game_infrastructure.data_gathering()
            game_infrastructure.image_search()
            while 'This article needs additional citations for verification' in game_infrastructure.car_data_table.text or 'Wikipedia does not have an article with this exact name' in game_infrastructure.car_data_table.text:
                game_infrastructure.kbb_search() # keep rerunning the program until it lands on a good car
                game_infrastructure.wiki_search()
                game_infrastructure.data_gathering()
                game_infrastructure.image_search()
        except TypeError or AttributeError:
            game_infrastructure.main()
player_1 = game_infrastructure.main()