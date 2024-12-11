import pygame as game
import sys


game.init()


sys_font = game.font.Font('fonts/font.ttf', 32)

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

menu_overlay = game.Surface((300, 450), game.SRCALPHA) #Прозрачная поверхность
menu_overlay_rect = menu_overlay.get_rect(center = (screen_x // 2, screen_y / 2))
game.draw.rect(menu_overlay, (0, 0, 0, 64), (0, 0, 300, 450), border_radius=27)

screen = game.display.set_mode((screen_x, screen_y)) #Создание экрана
game.display.set_caption("Noughts And Crosses")

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

def reset_game():
    global zones
    global winner
    global game_status
    global Turn
    global mouse_pressed
    for id in zones:
        zone = zones.get(id)
        zone[1] = 'Null'
    winner = None
    Turn = True
    game_status = 'running'

def quit_game():
    global running
    global game_status
    game_status = 'quit'
    running = False
    game.quit()
    sys.exit()


def menu_game():
    global game_status
    global mouse_pressed
    global sys_font
    screen.blit(menu_overlay, menu_overlay_rect)

    text_title_game = sys_font.render('Крестики - Нолики', 1, (255, 255, 255))
    text_title_game_rect = text_title_game.get_rect(center=(screen_x // 2, screen_y // 2 - 150))

    text_start_game = sys_font.render('Играть', 1, (255, 255, 255))
    text_start_game_rect = text_start_game.get_rect(center=(screen_x // 2, screen_y // 2))

    text_quit_game = sys_font.render('Выход', 1, (255, 255, 255))
    text_quit_game_rect = text_quit_game.get_rect(center=(screen_x // 2, screen_y // 2 + 150))

    start_button_overlay = game.Surface((250, 100), game.SRCALPHA)
    start_button_rect = start_button_overlay.get_rect(center = (screen_x // 2, screen_y / 2))
    game.draw.rect(start_button_overlay, (152, 252, 152, 200), (0, 0, 250, 100), border_radius=27)

    quit_button_overlay = game.Surface((250, 100), game.SRCALPHA)
    quit_button_rect = quit_button_overlay.get_rect(center = (screen_x // 2, screen_y / 2 + 150))
    game.draw.rect(quit_button_overlay, (255, 86, 86, 200), (0, 0, 250, 100), border_radius=27)
    

    screen.blit(quit_button_overlay, quit_button_rect)
    screen.blit(text_quit_game, text_quit_game_rect)
    screen.blit(text_title_game, text_title_game_rect)
    screen.blit(start_button_overlay, start_button_rect)
    screen.blit(text_start_game, text_start_game_rect)
        
    if game.mouse.get_pressed()[0] == False and start_button_rect.collidepoint(mouse_pos):
        game.draw.rect(start_button_overlay, (0, 0, 0, 64), (0, 0, 250, 100), border_radius=27)
        screen.blit(start_button_overlay, start_button_rect)
    if game.mouse.get_pressed()[0] == True and start_button_rect.collidepoint(mouse_pos) and mouse_pressed == False:
        mouse_pressed = True
        game_status = 'running'

    if game.mouse.get_pressed()[0] == False and quit_button_rect.collidepoint(mouse_pos):
        game.draw.rect(quit_button_overlay, (0, 0, 0, 64), (0, 0, 250, 100), border_radius=27)
        screen.blit(quit_button_overlay, quit_button_rect)
    if game.mouse.get_pressed()[0] == True and quit_button_rect.collidepoint(mouse_pos) and mouse_pressed == False:
        quit_game()

def game_running():
    global game_status
    global mouse_pressed
    global Turn
    global sys_font
    game_status = check_win()
    turn_player = None

    turn_player_overlay = game.Surface((150, 50), game.SRCALPHA)
    turn_player_overlay_rect = turn_player_overlay.get_rect(center = (screen_x // 2, screen_y / 2 - 225))
    game.draw.rect(turn_player_overlay, (0, 0, 0, 64), (0, 0, 150, 50), border_radius=27)

    if Turn:
        turn_player = sys_font.render('Ходит x', 1, (255, 255, 255))
    if not(Turn):
        turn_player = sys_font.render('Ходит o', 1, (255, 255, 255))

    turn_player_rect = turn_player.get_rect(center=(screen_x // 2, screen_y // 2 - 225))
    screen.blit(field, field_rect) #Отрисовка игрового поля в центре экрана
    screen.blit(turn_player_overlay, turn_player_overlay_rect)
    screen.blit(turn_player, turn_player_rect)
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
            if game.mouse.get_pressed()[0] == True and mouse_pressed == False:
                if Turn:
                    zone[1] = 'X'
                else: 
                    zone[1] = 'O'
                Turn = not(Turn)

def game_end():
    global Turn
    global game_status
    global mouse_pressed
    global sys_font
    screen.blit(menu_overlay, menu_overlay_rect)

    text_end_game = sys_font.render('Игра окончена', 1, (255, 255, 255))
    text_winner = sys_font.render(winner, 1, (0, 255 ,0))
    text_restart_game = sys_font.render('Играть снова', 1, (255, 255, 255))

    text_quit_game = sys_font.render('Выход', 1, (255, 255, 255))
    text_quit_game_rect = text_quit_game.get_rect(center=(screen_x // 2, screen_y // 2 + 150))

    text_end_game_rect = text_end_game.get_rect(center=(screen_x // 2, screen_y // 2 - 150))
    text_winner_rect = text_end_game.get_rect(center=(screen_x // 2, screen_y // 2 - 100))
    text_restart_game_rect = text_restart_game.get_rect(center=(screen_x // 2, screen_y // 2))
    
    start_button_overlay = game.Surface((250, 100), game.SRCALPHA)
    start_button_rect = start_button_overlay.get_rect(center = (screen_x // 2 , screen_y // 2))
    game.draw.rect(start_button_overlay, (152, 255, 152, 200), (0, 0, 250, 100), border_radius=27)

    quit_button_overlay = game.Surface((250, 100), game.SRCALPHA)
    quit_button_rect = quit_button_overlay.get_rect(center = (screen_x // 2, screen_y // 2 + 150))
    game.draw.rect(quit_button_overlay, (255, 86, 86, 200), (0, 0, 250, 100), border_radius=27)

    screen.blit(quit_button_overlay, quit_button_rect)
    screen.blit(start_button_overlay, start_button_rect)

    screen.blit(text_end_game, text_end_game_rect)
    screen.blit(text_quit_game, text_quit_game_rect)
    screen.blit(text_winner, text_winner_rect)
    screen.blit(text_restart_game, text_restart_game_rect)
    if game.mouse.get_pressed()[0] == False and start_button_rect.collidepoint(mouse_pos):
        game.draw.rect(start_button_overlay, (0, 0, 0, 64), (0, 0, 250, 100), border_radius=27)
        screen.blit(start_button_overlay, start_button_rect)

    if game.mouse.get_pressed()[0] == True and start_button_rect.collidepoint(mouse_pos) and mouse_pressed == False:
        reset_game()

    if game.mouse.get_pressed()[0] == False and quit_button_rect.collidepoint(mouse_pos):
        game.draw.rect(quit_button_overlay, (0, 0, 0, 64), (0, 0, 250, 100), border_radius=27)
        screen.blit(quit_button_overlay, quit_button_rect)
    if game.mouse.get_pressed()[0] == True and quit_button_rect.collidepoint(mouse_pos) and mouse_pressed == False:
        quit_game()
    

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
            winner = 'Победа: Крестики'
            return 'end_game'
        if all([j in posO for j in i]):
            winner = 'Победа: Нолики'
            return 'end_game'
    if counter == 9:
        winner = 'Ничья'
        return 'end_game'
    return 'running'

while running:
    mouse_pos = game.mouse.get_pos() #Координаты мыши
    screen.fill((0, 154, 100)) #Заполнение экрана цветом


    if game_status == 'menu':
        menu_game()
        
    if game_status == 'running':
        game_running()

    if game_status == 'end_game':
        game_end()

    
    if game.mouse.get_pressed()[0] == True and mouse_pressed == False:
            mouse_pressed = True
    if game.mouse.get_pressed()[0] == False and mouse_pressed == True:
            mouse_pressed = False
    print(game_status)
    
    
    for event in game.event.get():
        if event.type == game.QUIT:
            quit_game()
            
    game.display.update()

