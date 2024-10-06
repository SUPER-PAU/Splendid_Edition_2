import pygame
from pygame import mixer
from lib.clock import Clock
from lib.display import display
from lib.gamemodes import Game
from lib.joystick import joystick


# Инициализация
pygame.init()
mixer.init()

game = Game()
# Загрузка клока
clocks = Clock()
# загрузить бойцов
# reset_players()

# определить клики
mouse_click = False
keyboard_click = False
joy_click = False
new_frame = True
# Луп игры
while game.aplication_run:
    # Хэндлер
    joystick.locate_joystick()
    mouse_click = False
    joy_click = False
    keyboard_click = False
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game.aplication_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            joystick.change_layout("mouse")
        if event.type == pygame.KEYDOWN:
            keyboard_click = True
            joystick.change_layout("mouse")
        if event.type == pygame.JOYBUTTONDOWN:
            joy_click = True
            joystick.change_layout("controller")
    game.game_navigation(keyboard_click, mouse_click, joy_click)
    pygame.display.flip()
    # Обновление кадра дисплея
    pygame.display.update()
    clocks.clock.tick(display.refresh_rate)

pygame.quit()
