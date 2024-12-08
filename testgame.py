import pygame as game
import sys


game.init()

#Размеры окна
screen_x = 500
screen_y = 500

zone_size = 100 #Размер зоны для крестика/нолика

screen = None
game_started = True #состояние игры

#Загрузка изображений
field = game.image.load('field.png')
Nought = game.image.load('Nought.png')
Cross = game.image.load('Cross.png')

overlay = game.Surface((zone_size, zone_size), game.SRCALPHA) #Прозрачная поверхность для зон с размером 100


screen = game.display.set_mode((screen_x, screen_y)) #Создание экрана

field_rect = field.get_rect(center = (screen_x // 2, screen_y / 2)) #Получение объекта класса Rect, с местоположением в центре экрана
game.draw.rect(overlay, (0, 0, 0, 64), (0, 0, zone_size, zone_size), border_radius=27) #Полупрозрачаня поверхность с закругленными краями

# !!!
# !!!
#[БУДЕТ ИЗМЕНЕНО] Очередь хода
# True = X 
# False = O
# !!!
# !!!
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

#Заполнение zones с необходимыми параметрами, отступом и состоянием
for id, offset in enumerate(offsets):
    zones[id] = [(game.Rect(field_rect.centerx + offset[0] - zone_size // 2, field_rect.centery + offset[1] - zone_size // 2, zone_size, zone_size)), "Null"]


while game_started:
    
    screen.fill((0, 154, 100)) #Заполнение экрана цветов

    screen.blit(field, field_rect) #Отрисовка игрового поля в центре экрана

    mouse_pos = game.mouse.get_pos() #Координаты мыши
    # print(mouse_pos)


    for id in zones:
        zone = zones.get(id)

        # Отрисовка крестиков и ноликов, если они имеются на поле
        if zone[1] == 'X':
            screen.blit(Cross, zone[0].topleft)
        if zone[1] == 'O':
            screen.blit(Nought, zone[0].topleft)

        #Обработка наведения мыши на зону, куда можно поставить крестик/нолик
        if zone[0].collidepoint(mouse_pos) and zone[1] == 'Null':
            screen.blit(overlay, zone[0].topleft)
            #!!!
            #!!!
            #[БУДЕТ ИЗМЕНЕНО] Обработка нажатия кнопки на зону, установка крестика или нолика
            #!!!
            #!!!
            if game.mouse.get_pressed()[0] == True:
                if Turn:
                    zone[1] = 'X'
                else: 
                    zone[1] = 'O'
                Turn = not(Turn)
        # else:
        #     if game.mouse.get_pressed()[2] == True:
        #         zone[1] = 'Null'


            

    #Обработка события закрытия игры
    for event in game.event.get():
        if event.type == game.QUIT:
            game_started = False
            game.quit()
            sys.exit()

    game.display.update() #[БУДЕТ ИЗМЕНЕНО] Обновление экрана
    

  
    
    
    