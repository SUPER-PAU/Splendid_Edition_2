import pygame
from lib.display import display


class Clock:
    def __init__(self):
        # Клок с фпс лимитом
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Кулдаун для диалогов
        self.keypress_cooldown = 50

        # Тики
        self.ticks = pygame.time.get_ticks()

    def cutscene_fps(self):
        self.fps = 24

    def normal_fps(self):
        self.fps = 60
