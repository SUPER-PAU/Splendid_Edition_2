import pygame
from lib.display import display

pygame.font.init()

# Определение шрифта turok и его размера
count = pygame.font.Font(r'assets\fonts\turok.ttf', int(150 * display.scr_w))
score = pygame.font.Font(r'assets\fonts\turok.ttf', int(80 * display.scr_w))
victory_text = pygame.font.Font(r'assets\fonts\turok.ttf', int(200 * display.scr_w))

# Системный шрифт для диалогов
sys = pygame.font.SysFont('Times New Roman', int(40 * display.scr_w))
bigger_sys = pygame.font.SysFont('Times New Roman', int(80 * display.scr_w))
