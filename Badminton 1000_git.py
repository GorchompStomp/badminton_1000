#Byron Jones   bjone079@uottawa.ca
#This program is for organising badminton games
#There is a ELO rating system, and a group rating system.
#The ELO needs to be calibrated through play, while the group system is plug and play.
#The badminton club I will use it for is doubles play, with 4 available courts.
import random

class Player:

    def __init__(self, name = 'Guest', group = 2, games = 0, rating = 1500):        #rating currently not in use

        self.name = name

        self.group = group

        self.games = games
        
        self.rating = rating
    
    def __repr__(self):
        
        return str(self.name)# + ":" + str(self.group) + ":" + str(self.games)

    def __eq__(self, o):
        
        return self.name == o.name and self.group == o.group
    
##    def game(self, oppo, sa): 
##        '''
##objects --> (none)
##with input of player, opponent and win/tie/lose, update the rating of both players
##'''
##        if (sa == 1):
##            sb = 0
##
##        elif (sa == .5):
##            sb = .5
##
##        elif (sa == 0):
##            sb = 1
##            
##        ea = 1 / (1 + 10 ** ((oppo.rating - self.rating) / 400))
##        eb = 1 / (1 + 10 ** ((self.rating - oppo.rating) / 400))
##        self.rating = self.rating + 32 * (sa - ea)
##        oppo.rating = oppo.rating + 32 * (sb - eb)
def games_played(total):
    total += 1
    return total

def new_game(player_list):
    
    random.shuffle(player_list)                         #shuffle list to randomise play
    
    player_list.sort(key=lambda x: x.games)             #sort from fewest games played to most
    
    orgfield = []                                       #temp list for new game
    total = 0
    print(games_played(total))
    
    print('\n Games played = '+ str(games_played))
    
    i = 0
    while i < 16:
        
        player_list[i].games = player_list[i].games + 1     #Increase the games played by those playing next round by 1
        orgfield.append(player_list[i])                     #Add those players to temp list for new game
        i += 1

    
    orgfield.sort(key=lambda x: x.group)                #sort temp list by skill group

    b=0                                                 #index for courts
    print('')
    
    for i in orgfield:                                  #go through temp list of players and print names and court placement

        print(i)
        b=b+1

        if (b % 4) == 0:                                #Court number
            
            print('COURT: ' + str(b // 4))
            print('')
            
    orgfield = []                                       #clear temp list
    

def remove(player_list, player):
    
    if player in player_list:
        player_list.remove(player)
        print(str(player) + ' has been removed from player_list.')

    else: print("player not in list")


def add(player_list, player):
    
    try:
        player.games = player_list[len(player_list) // 2].games
        player_list.append(player)
        print(str(player) + ' has been successfully added to the list!')
        
    except Exception:
        print('Player is not in program, please check name,\n or assign to dropin')
        player = input('Re-enter name or select a drop in: ')
        
    return


def skip(player):
    
    player.games = player_list[len(player_list)-1].games + .1
    print(str(player) + ' has been set to skip next game.')


def find(player_list, player):  #use a for loop, okay I guess
    
    try:
        player in player_list
        return True
    
    except NameError:
        print("name not found")


def help():
    
    print('\nWelcome to Badminton 1000!\n')

    print('I count the number of games people play, and suggest courts based \non peoples skill rating.\n')

    print('I can do some stuff:\n\nStart a new game by inputting \'new_game(player_list)\'\n')
    
    print('You can add players who are in the main program,  by using: \nadd(player_list, player) where player is the variable name of the player\nI throw errors but don\'t worry it\'s normal(ish).\n')

    print('Remove players by writing \'remove(player_list, player)\' \nwhere player = name of player with underscore and captials\nfor example: Byron_Jones\n')

    print('if you want to see if someone is in the player list\nType: find(player_list, player) where player is as above\n')

    print('if you want to see the entire list of players type: print(player_list)\n\n')

    print('Go ahead, write: new_game(player_list)\n\n')

    print('If you want to see this again type: help()\n')
    
        
"-------------------------------------------------------------------------------------------------------------------------"
#This area is for creating the player list. If a player is not going to attend, comment out the player_list.append() function


player_list = []

Telson_Neuvella = Player('Telson Neuvella', 3)
#player_list.append(Telson_Neuvella)

Steve_Harvey = Player('Steve Harvey', 1)
#player_list.append(Steve_Harvey)

drop_in_1 = Player('drop_in_1', 1)
#player_list.append(drop_in_1)

drop_in_2 = Player('drop_in_2', 1)
#player_list.append(drop_in_2)

drop_in_3 = Player('drop_in_3', 2)
#player_list.append(drop_in_3)

drop_in_4 = Player('drop_in_4', 2)
#player_list.append(drop_in_4)

drop_in_5 = Player('drop_in_5', 3)
#player_list.append(drop_in_5)

drop_in_6 = Player('drop_in_6', 3)
#player_list.append(drop_in_6)


"--------------------------------------------------------------------------------------------------------------------------"

#User display instructions

print('\nWelcome to Badminton 1000!\n')

print('I count the number of games people play, and suggest courts based \non peoples skill rating.\n')

print('I can do some stuff:\n\nStart a new game by inputting \'new_game(player_list)\'.\n')

print('You can add players who are in the main program,  by using: \n\'add(player_list, player)\' where player is the variable name of the player.\nI throw errors but don\'t worry it\'s normal(ish).\n')

print('Remove players by writing \'remove(player_list, player)\' \nwhere player = name of player with underscore and captials\nfor example: Byron_Jones\n')

print('If you want to see if someone is in the player list\ntype: \'find(player_list, player)\' where player is as above\n')

print('If you want to see the entire list of players type: \'print(player_list)\'\n\n')

print('Go ahead, write: new_game(player_list)\n\n')

print('If you want to see this again type: help()\n')
