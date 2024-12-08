import pygame as game
import sys

screen_x = 500
screen_y = 500

zone_size = 100
screen = None

game_started = True
game.init()

field = game.image.load('field.png')
field_rect = field.get_rect(center = (screen_x // 2, screen_y / 2))


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

zones = [ ]

for i in offsets:
    zones.append(game.Rect(field_rect.centerx + i[0] - zone_size // 2, field_rect.centery + i[1] - zone_size // 2, zone_size, zone_size))


zone = game.Surface((100, 100), game.SRCALPHA)
zone.fill((0,0,0,0))




screen = game.display.set_mode((screen_x, screen_y))

while game_started:
    screen.fill((0, 154, 100))
    screen.blit(field, field_rect)

    mouse_pos = game.mouse.get_pos()
    print(mouse_pos)

    for zone in zones:
        if zone.collidepoint(mouse_pos):
            overlay = game.Surface((zone_size, zone_size), game.SRCALPHA)
            overlay.fill((0, 0, 0, 0))
            game.draw.rect(overlay, (0, 0, 0, 64), (0, 0, zone_size, zone_size), border_radius=27) 
            screen.blit(overlay, zone.topleft)
    

    

    for event in game.event.get():
        if event.type == game.QUIT:
            game_started = False
            game.quit()
            sys.exit()
        else:
            game.display.flip()
  
    
    
    