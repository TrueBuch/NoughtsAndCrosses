def check_field(game_field, row, player, running):  # Проверка на свободное поле + регистрация хода
    if game_field[row] == "":
        game_field[row] = player  # Используем присваивание
        result = check_win(game_field, player)
        if result != "Игра продолжается":
            running[0] = False  # Завершаем игру, если есть победитель или ничья
        return True
    print("Поле занято, попробуйте снова.")
    return False

def check_win(game_field, player):  # Проверка на победу
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for i in wins:
        if all(game_field[j] == player for j in i):
            return f"Победа игрока {'1' if player == 'x' else '2'}"
    return check_draw(game_field)

def check_draw(game_field):  # Проверка на ничью
    if all(i != "" for i in game_field):
        return "Ничья"
    return "Игра продолжается"

def main():  # Основная функция
    game_field = [""] * 9
    turn = True
    players = ["x", "o"]
    running = [True]  # Используем список для передачи по ссылке

    while running[0]:
        current_player = players[turn]
        print(f"Ход игрока {current_player}:")
        while True:
            try:
                move = int(input("Введите номер ячейки (0-8): "))
                if 0 <= move < 9 and check_field(game_field, move, current_player, running):
                    break
            except ValueError:
                print("Пожалуйста, введите число от 0 до 8.")
        
        turn = 1 - turn  # Смена игрока

    # Выводим результат после завершения игры
    print("Игровое поле:")
    for i in range(0, 9, 3):
        print(game_field[i:i+3])  # Отображение игрового поля

    # Проверяем, кто выиграл
    result = check_win(game_field, players[0])  # Проверяем для первого игрока
    if result == "Игра продолжается":
        result = check_win(game_field, players[1])  # Проверяем для второго игрока
    print(result)

if __name__ == "__main__":
    main()







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