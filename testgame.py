import pygame as game
import sys

screen_length = 500
screen_width = 500
screen = None

game_started = True
game.init()

screen = game.display.set_mode((screen_length, screen_width))
screen.fill((0, 154, 100))
while game_started:

    game.display.update()

    for event in game.event.get():
        if event.type == game.QUIT:
            game_started = False
            game.quit()

    