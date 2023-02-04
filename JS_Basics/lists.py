import random
potential_lists = ['https://en.wikipedia.org/wiki/List_of_sport_utility_vehicles', 'https://en.wikipedia.org/wiki/List_of_vans', 'https://en.wikipedia.org/wiki/List_of_sports_cars', 'https://en.wikipedia.org/wiki/List_of_fastback_automobiles', 'https://en.wikipedia.org/wiki/List_of_fastest_production_cars_by_acceleration', 'https://en.wikipedia.org/wiki/List_of_production_battery_electric_vehicles', 'https://en.wikipedia.org/wiki/List_of_coup%C3%A9_convertibles' ]
list_length = len(potential_lists)
chosen_ind = random.choice(range(0, list_length))
chosen_list = potential_lists[chosen_ind]
print(chosen_list)
