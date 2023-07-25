import pygame
from lib.display import display

# Иконки интерфейса
round_count_empt = pygame.image.load(r"assets\images\UI\round_count.png").convert_alpha()
round_count_vin = pygame.image.load(r"assets\images\UI\round_vin.png").convert_alpha()

button_X = pygame.image.load(r"assets\images\UI\x_button.png").convert_alpha()
button_Triangle = pygame.image.load(r"assets\images\UI\triangle_button.png").convert_alpha()
button_Square = pygame.image.load(r"assets\images\UI\square_button.png").convert_alpha()
button_O = pygame.image.load(r"assets\images\UI\o_button.png").convert_alpha()
Left_Click = pygame.image.load(r"assets\images\UI\left_click.png").convert_alpha()
Richt_Click = pygame.image.load(r"assets\images\UI\right_click.png").convert_alpha()
Mid_Click = pygame.image.load(r"assets\images\UI\mid_click.png").convert_alpha()

button_X = pygame.transform.scale(button_X, (60 * display.scr_w, 60 * display.scr_h))
button_Triangle = pygame.transform.scale(button_Triangle, (60 * display.scr_w, 60 * display.scr_h))
button_Square = pygame.transform.scale(button_Square, (60 * display.scr_w, 60 * display.scr_h))
button_O = pygame.transform.scale(button_O, (60 * display.scr_w, 60 * display.scr_h))
Left_Click = pygame.transform.scale(Left_Click, (60 * display.scr_w, 60 * display.scr_h))
Richt_Click = pygame.transform.scale(Richt_Click, (60 * display.scr_w, 60 * display.scr_h))
Mid_Click = pygame.transform.scale(Mid_Click, (60 * display.scr_w, 60 * display.scr_h))
