import pygame as game
import sys


game.init()


sys_font = game.font.SysFont('arial', 64)

#Размеры окна
screen_x = 500
screen_y = 500

zone_size = 100 #Размер зоны для крестика/нолика

screen = None
running = True
game_status = 'menu'
winner = None
mouse_pressed = False

#Загрузка спрайтов
field = game.image.load('sprites/field.png')
Nought = game.image.load('sprites/Nought.png')
Cross = game.image.load('sprites/Cross.png')

zone_overlay = game.Surface((zone_size, zone_size), game.SRCALPHA) #Прозрачная поверхность для зон с размером 100
game.draw.rect(zone_overlay, (0, 0, 0, 64), (0, 0, zone_size, zone_size), border_radius=27) #Полупрозрачаня поверхность с закругленными краями

start_button_overlay = game.Surface((300, 450), game.SRCALPHA) #Прозрачная поверхность
start_button_overlay_rect = start_button_overlay.get_rect(center = (screen_x // 2, screen_y / 2))
game.draw.rect(start_button_overlay, (0, 0, 0, 64), (0, 0, 300, 450), border_radius=27)

screen = game.display.set_mode((screen_x, screen_y)) #Создание экрана

field_rect = field.get_rect(center = (screen_x // 2, screen_y / 2)) #Получение объекта класса Rect, с местоположением в центре экрана


#Ход игрока
#True = X
#False = O
Turn = True



#Список отступов от центра экрана для отрисовки зон
offsets = [
    (-138, -138),  # 0
    (0, -138),     # 1
    (138, -138),   # 2
    (-138, 0),     # 3
    (0, 0),        # 4
    (138, 0),      # 5
    (-138, 138),   # 6
    (0, 138),      # 7
    (138, 138),    # 8
]

zones = {} #Словарь зон где id: [Rect, Состояние(Null, X, O)]
wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

#Заполнение zones с необходимыми параметрами, отступом и состоянием
for id, offset in enumerate(offsets):
    zones[id] = [(game.Rect(field_rect.centerx + offset[0] - zone_size // 2, field_rect.centery + offset[1] - zone_size // 2, zone_size, zone_size)), 'Null']

def check_win():  # Проверка на победу
    global zones
    global wins
    global winner
    posX = []
    posO = []
    counter = 0
    
    
    for id in zones:
        zone = zones.get(id)
        if zone[1] == 'X':
            posX.append(id)
        if zone[1] == 'O':
            posO.append(id)
        if zone[1] != 'Null':
            counter += 1
    for i in wins:
        if all([j in posX for j in i]):
            winner = 'Победа X'
            return 'end_game'
        if all([j in posO for j in i]):
            winner = 'Победа O'
            return 'end_game'
    if counter == 9:
        winner = 'Ничья'
        return 'end_game'
    return 'running'

# def main():  # Основная функция
#     game_field = [""] * 9
#     turn = True
#     players = ["x", "o"]
#     running = [True]  # Используем список для передачи по ссылке

#     while running[0]:
#         current_player = players[turn]
#         print(f"Ход игрока {current_player}:")
#         while True:
#             try:
#                 move = int(input("Введите номер ячейки (0-8): "))
#                 if 0 <= move < 9 and check_field(game_field, move, current_player, running):
#                     break
#             except ValueError:
#                 print("Пожалуйста, введите число от 0 до 8.")
        
#         turn = 1 - turn  # Смена игрока

#     # Выводим результат после завершения игры
#     print("Игровое поле:")
#     for i in range(0, 9, 3):
#         print(game_field[i:i+3])  # Отображение игрового поля

#     # Проверяем, кто выиграл
#     result = check_win(game_field, players[0])  # Проверяем для первого игрока
#     if result == "Игра продолжается":
#         result = check_win(game_field, players[1])  # Проверяем для второго игрока
#     print(result)

# if __name__ == "__main__":
#     main()







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

while running:
    print(game_status)
    mouse_pos = game.mouse.get_pos() #Координаты мыши
    # print(mouse_pos)

    screen.fill((0, 154, 100)) #Заполнение экрана цветов


    if game_status == 'menu':
        
        
        screen.blit(start_button_overlay, start_button_overlay_rect)
        
        if game.mouse.get_pressed()[0] == True and start_button_overlay_rect.collidepoint(mouse_pos):
            game_status = 'running'
            mouse_pressed = True
        

    if game_status == 'running':
        game_status = check_win()
        screen.blit(field, field_rect) #Отрисовка игрового поля в центре экрана
        for id in zones:
            zone = zones.get(id)

            # Отрисовка крестиков и ноликов, если они имеются на поле
            if zone[1] == 'X':
                screen.blit(Cross, zone[0].topleft)
            if zone[1] == 'O':
                screen.blit(Nought, zone[0].topleft)

            #Обработка наведения мыши на зону, куда можно поставить крестик/нолик
            if zone[0].collidepoint(mouse_pos) and zone[1] == 'Null':
                screen.blit(zone_overlay, zone[0].topleft)
                #!!!
                #!!!
                #[БУДЕТ ИЗМЕНЕНО] Обработка нажатия кнопки на зону, установка крестика или нолика
                #!!!
                #!!!
                if game.mouse.get_pressed()[0] == True and mouse_pressed == False:
                    if Turn:
                        zone[1] = 'X'
                    else: 
                        zone[1] = 'O'
                    Turn = not(Turn)
                    mouse_pressed = True
            
            if game.mouse.get_pressed()[2] == True:
                Turn = True
                zone[1] = 'Null'

    
    if game_status == 'end_game':
        screen.blit(start_button_overlay, start_button_overlay_rect)
        sys_text = sys_font.render(winner, 1, (255, 0, 0))
        sys_text_rect = sys_text.get_rect(center=(screen_x // 2, screen_y // 2 - 150))
        screen.blit(sys_text, sys_text_rect)
        if game.mouse.get_pressed()[0] == True and start_button_overlay_rect.collidepoint(mouse_pos) and mouse_pressed == False:
            for id in zones:
                zone = zones.get(id)
                zone[1] = 'Null'
            Turn = True
            game_status = 'running'
            mouse_pressed = True
    
    if game.mouse.get_pressed()[0] == False:
            mouse_pressed = False
        
    #Обработка события закрытия игры
    for event in game.event.get():
        if event.type == game.QUIT:
            game_started = False
            game.quit()
            sys.exit()

    game.display.update() #[БУДЕТ ИЗМЕНЕНО] Обновление экрана

