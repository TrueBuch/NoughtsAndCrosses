import random



def check_field(game_field, row, player): #проверка на свободное поле+регаем ход
    if game_field[row] == "":
        game_field[row] == player
        print(game_field)
        check_win(game_field, player)
        return True
    return False


def check_win(game_field, player): #проверка на победу
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for i in wins:
        count = 0
        for j in i:
            if game_field[j] == player:
                count += 1
        if count == 3:
            if player == "x":
                return "Победа игрока 2"
            else:
                return "Победа игрока 1"
    else:
        return check_draw(game_field)

def check_draw(game_field): #проверка на ничью
    count = 0
    for i in game_field:
        if i != "":
            count += 1
    if count == 9:
        return "Ничья"
    else:
        return "Игра продолжается"
        

game_field = ["x","","x","o","o","x","x","x","o"]
player = "x"
print(check_win(game_field, player))








# def main():
#     game_field = ["" for _ in range(9)]
#     turn = random.randint(0,1)
#     playero = "o"
#     playerx = "x"
#     if turn:
#         print("Player x")
#         check_field(game_field, int(input()), playerx)
#     else:
#         print("Player o")
#         check_field(game_field, int(input()), playero)
# main()