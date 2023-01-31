import re
from pyt_back import game_infrastructure
game_infrastructure.main()
class game_quiz():
    num_att = 0
    list_dic = list(game_infrastructure.info_dict)
    difficulties  = {'Easy': len(list_dic) + 2, 'Medium': (len(list_dic) +1), 'Nerd': (len(list_dic) - ((len(list_dic))- 2))} 
    chosen_difficulty_input = input(' Welcome to my Quiz Game! You will be given information about a car, and you have to guess what it is! \nWhat difficulty do you want? \nEasy \nMedium \nNerd \nKeep in mind, Nerd is really tough.\n')
    chosen_difficulty = difficulties[chosen_difficulty_input]
    print('Your options are...\n',list_dic)
    game_infrastructure.car_make = game_infrastructure.car_make.replace('_', ' ')
    game_infrastructure.car_model = game_infrastructure.car_model.replace('_', ' ')
    ai_chosen_car = f'{game_infrastructure.car_make} {game_infrastructure.car_model}'
    ai_chosen_car_re = re.sub('_', ' ', ai_chosen_car)
    def game():
        chosen_info = input('What information do you wish to access? \n-->')
        if chosen_info in game_infrastructure.info_dict:
           print(game_infrastructure.info_dict.get(chosen_info))
    
    
    while chosen_difficulty > num_att:
        game()
        user_ans = input('What car do you think it is?\n')
        if user_ans.lower() == ai_chosen_car_re.lower():
            print('You have won! ')
            break
        else:
            num_att+=1
            print(f'Wrong answer... \nYou have {(chosen_difficulty - num_att)} attempts remaining... ')
            print('Your options are...\n',list_dic)
    else:
        print('You failed... Here\'s the car! ')
        print(f'{game_infrastructure.car_make} {game_infrastructure.car_model}')
        user_input = input('Do you want to see the specs for this car? \n--> ')
        if user_input[0].lower() == 'y':
            for key, item in game_infrastructure.info_dict.items():
                    print(key, '\n', item)
    




player_1 = game_quiz()