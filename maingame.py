import random

game_field = ["","","","","","","","",""]
playerx =
playero =
turn = random.randint(0,1)

def check_field(game_field, row, player):
    if game_field[row] == "":
        game_field[row] == player
        return True
    return False