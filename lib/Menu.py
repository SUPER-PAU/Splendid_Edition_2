import pygame
import cv2

import lib.players_data.online_players as player
from constants.textures.backgrounds import bulat_boss

from lib.display import display
from constants.fonts.turok import sys as font
from lib.joystick import joystick, get_j
from lib.mixer import play_music_bg
from lib.Settings import settings
from lib.drawer import draw_text, draw_windowed_bg_instance
import constants.textures.player_card_sprites as card
from lib.Database import save_name
import constants.textures.icons as layout
from constants.progress import pg
from constants.audio.effects import shield_sfx as button_sound_eff


# from constants.fonts.turok import bigger_sys as big_font

MAIN_MENU_GUI = pygame.image.load(
    r"assets\images\UI\menu_GUI.png").convert_alpha()
GAME_MODE_GUI = pygame.image.load(
    r"assets\images\UI\game_menu_GUI.png").convert_alpha()
ONLINE_MODE_GUI = pygame.image.load(
    r"assets\images\UI\game_online_menu_GUI.png").convert_alpha()
STORY_MODE_BUTTON = pygame.image.load(
    r"assets\images\UI\story_button_GUI.png").convert_alpha()
SURVIVAL_MODE_BUTTON = pygame.image.load(
    r"assets\images\UI\survival_button_GUI.png").convert_alpha()
BACK_BUTTON = pygame.image.load(
    r"assets\images\UI\back_menu_GUI.png").convert_alpha()
PLAY_BUTTON = pygame.image.load(
    r"assets\images\UI\menu_Button_Play_GUI.png").convert_alpha()
EASY_BUTTON = pygame.image.load(
    r'assets\images\UI\easy_button.png').convert_alpha()
NORMAL_BUTTON = pygame.image.load(
    r'assets\images\UI\normal_button.png').convert_alpha()
HARD_BUTTON = pygame.image.load(
    r'assets\images\UI\hard_button.png').convert_alpha()
EXIT_OPTIONS = pygame.image.load(
    r'assets\images\UI\exit_options_button.png').convert_alpha()
BATTLE_MENU_FOUND = pygame.image.load(
    r'assets\images\UI\Battle_menu_found.png').convert_alpha()
ONLINE_MODE_BACK = pygame.image.load(
    r'assets\images\UI\game_online_menu_back.png').convert_alpha()
ONLINE_MODE_START = pygame.image.load(
    r'assets\images\UI\game_online_menu_start.png').convert_alpha()
HERO_PICK_BACK = pygame.image.load(
    r'assets\images\UI\hero_pick_back_button.png').convert_alpha()


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, size, pos, text, clicked_image=None, button_layout=None, button=None):
        self.x, self.y = pos
        self.size = self.width, self.height = size
        self.clicked = False
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.render = None
        self.button = button
        self.button_image = button_layout
        self.change_text(text)
        self.clicked_image = clicked_image
        if clicked_image:
            self.clicked_image = pygame.transform.scale(self.clicked_image,
                                                        (display.screen_width, display.screen_height))

    def change_text(self, text, color='White'):
        self.render = font.render(text, 1, pygame.Color(color))
        display.screen.blit(self.render, (int(self.rect.centerx - 60 * display.scr_w),
                                          int(self.y + self.height // 2 - 30 * display.scr_h)))

    def show(self):
        self.clicked = False
        if joystick.get_layout() != "mouse" and self.button_image:
            click_rect = pygame.rect.Rect((self.rect.centerx - 25 * display.scr_w,
                                           self.rect.bottom - 30 * display.scr_h,
                                           50 * display.scr_w, 50 * display.scr_h))
            display.screen.blit(self.button_image, (click_rect.x, click_rect.y))
        # display.screen.blit(self.surface, (self.x, self.y))
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

    def click(self, mouse_click, joy_click):
        if joystick.get_joystick():
            joybutton = joystick.main_joystick.get_button
        else:
            joybutton = get_j

        if joystick.get_layout() != "mouse" and self.button_image:
            if joybutton(self.button):
                if self.clicked_image:
                    display.screen.blit(self.clicked_image, (0, 0))
                self.change_text(self.text, "Black")
                if joybutton(self.button) and joy_click:
                    self.clicked = True
                    button_sound_eff.play()
            else:
                self.change_text(self.text)

        else:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                if self.clicked_image:
                    display.screen.blit(self.clicked_image, (0, 0))
                self.change_text(self.text, "Black")
                if pygame.mouse.get_pressed()[0] and mouse_click:
                    self.clicked = True
                    button_sound_eff.play()
            else:
                self.change_text(self.text)

    def is_clicked(self):
        return self.clicked


class ButtonVisual:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, font, size, pos):
        self.x, self.y = pos
        self.size = self.width, self.height = size
        self.font = font
        self.text = text
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.change_text(text)
        # self.bought = False
        self.render = None
        self.color = (122, 124, 255)

    def change_text(self, text, bg=(122, 124, 255)):
        self.render = self.font.render(text, 1, (255, 255, 255))
        self.surface.fill(bg)
        self.surface.blit(self.render, (self.width // 2 - 70, self.height // 2 - 30))

    def show(self):
        self.clicked = False
        display.screen.blit(self.surface, (self.x, self.y))
        self.change_text(self.text, self.color)
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

    def click(self, mouse_click):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.color = (0, 4, 255)
            if mouse_click:
                self.clicked = True
        else:
            self.color = (122, 124, 255)

    def is_clicked(self):
        return self.clicked


class CardButtonEnemy:
    def __init__(self, player, pos):
        self.x, self.y = pos
        self.size = self.width, self.height = 150 * display.scr_w, 200 * display.scr_h
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.render = None
        self.player = player
        self.clicked_image = card.clicked
        self.picked = False

    def get_p(self):
        return self.player

    def set_picked(self):
        self.picked = True

    def show(self):
        img = pygame.transform.scale(card.card_by_name[f"{self.player.name}"], self.size)
        display.screen.blit(img, (self.x, self.y))
        if not self.player.alive:
            img = pygame.transform.scale(card.dead, self.size)
            display.screen.blit(img, (self.x, self.y))
            self.picked = False
        if self.picked:
            img = pygame.transform.scale(card.picked, self.size)
            display.screen.blit(img, (self.x, self.y))
        # display.screen.blit(self.surface, (self.x, self.y))
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

    def is_clicked(self):
        return self.clicked


class CardButton:
    def __init__(self, pos, picked, button_image=None, text=None, button=None):
        self.pos = pos
        self.x, self.y = pos

        self.picked_pos = (self.x - 38 * display.scr_w, self.y - 50 * display.scr_h)
        self.text = text
        self.normal_size = self.width, self.height = 150 * display.scr_w, 200 * display.scr_h
        self.picked_size = 225 * display.scr_w, 300 * display.scr_h
        self.size = self.normal_size

        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.render = None
        self.player = player
        self.clicked_image = card.clicked
        self.picked = picked
        self.button_image = button_image
        self.button = button

    def get_p(self):
        return self.player

    def set_picked(self):
        self.picked = True

    def set_unpicked(self):
        self.picked = False

    def show(self):

        img = pygame.transform.scale(self.button_image, self.size)
        display.screen.blit(img, (self.x, self.y))
        if self.picked:
            self.size = self.picked_size
            self.x, self.y = self.picked_pos
            img = pygame.transform.scale(card.picked, self.size)
            display.screen.blit(img, (self.x, self.y))
        else:
            self.x, self.y = self.pos
            self.size = self.normal_size
            if joystick.get_layout() != "mouse" and self.button_image:
                click_rect = pygame.rect.Rect((self.rect.centerx - 25 * display.scr_w,
                                               self.rect.bottom - 30 * display.scr_h,
                                               50 * display.scr_w, 50 * display.scr_h))
                display.screen.blit(self.button_image, (click_rect.x, click_rect.y))
        # display.screen.blit(self.surface, (self.x, self.y))
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

    def show_locked(self):
        img = pygame.transform.scale(card.card_lock, self.size)
        display.screen.blit(img, (self.x, self.y))
        draw_text(self.text, font, "white", self.rect.left - (60 * display.scr_w),
                  self.rect.bottom + (20 * display.scr_h))

    def show_locked_2_line(self):
        img = pygame.transform.scale(card.card_lock, self.size)
        display.screen.blit(img, (self.x, self.y))
        draw_text(self.text[0], font, "white", self.rect.left - (60 * display.scr_w),
                  self.rect.bottom + (10 * display.scr_h))
        draw_text(self.text[1], font, "white", self.rect.left - (60 * display.scr_w),
                  self.rect.bottom + (50 * display.scr_h))

    def click(self, mouse_click, joy_click):
        self.clicked = False
        if not self.picked:
            if joystick.get_joystick():
                joybutton = joystick.main_joystick.get_button
            else:
                joybutton = get_j
            if joystick.get_layout() != "mouse" and self.button_image:
                if joybutton(self.button) and joy_click:
                    self.clicked = True
            else:
                x, y = pygame.mouse.get_pos()
                if self.rect.collidepoint(x, y):
                    img = pygame.transform.scale(self.clicked_image, self.size)
                    display.screen.blit(img, (self.x, self.y))
                    if pygame.mouse.get_pressed()[0] and mouse_click:
                        self.clicked = True

    def is_clicked(self):
        return self.clicked


class LineEdit:
    def __init__(self, size, pos):
        self.x, self.y = pos
        self.size = self.width, self.height = size
        self.clicked = False
        self.text = []
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.render = None

    def click(self, mouse_click):
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and mouse_click:
            if self.rect.collidepoint(x, y):
                self.clicked = True
            else:
                if self.clicked:
                    save_name(self.get_raw_text())
                self.clicked = False

    def set_text(self, text):
        self.text.append(str(text))

    def show(self, key_press):
        key = pygame.key.get_pressed()
        if self.clicked and key_press:
            if key[pygame.K_BACKSPACE] and len(self.text) > 0:
                self.text.pop()
            if len(self.text) < 20:
                if key[pygame.K_SPACE]:
                    self.text.append(' ')
                if key[pygame.K_1]:
                    self.text.append('1')
                if key[pygame.K_2]:
                    self.text.append('2')
                if key[pygame.K_3]:
                    self.text.append('3')
                if key[pygame.K_4]:
                    self.text.append('4')
                if key[pygame.K_5]:
                    self.text.append('5')
                if key[pygame.K_6]:
                    self.text.append('6')
                if key[pygame.K_7]:
                    self.text.append('7')
                if key[pygame.K_8]:
                    self.text.append('8')
                if key[pygame.K_9]:
                    self.text.append('9')
                if key[pygame.K_0]:
                    self.text.append('0')
                if key[pygame.K_v]:
                    self.text.append('V')
                if key[pygame.K_c]:
                    self.text.append('C')
                if key[pygame.K_q]:
                    self.text.append('Q')
                if key[pygame.K_w]:
                    self.text.append('W')
                if key[pygame.K_e]:
                    self.text.append('E')
                if key[pygame.K_r]:
                    self.text.append('R')
                if key[pygame.K_t]:
                    self.text.append('T')
                if key[pygame.K_y]:
                    self.text.append('Y')
                if key[pygame.K_u]:
                    self.text.append('U')
                if key[pygame.K_i]:
                    self.text.append('I')
                if key[pygame.K_o]:
                    self.text.append('O')
                if key[pygame.K_p]:
                    self.text.append('P')
                if key[pygame.K_a]:
                    self.text.append('A')
                if key[pygame.K_s]:
                    self.text.append('S')
                if key[pygame.K_d]:
                    self.text.append('D')
                if key[pygame.K_f]:
                    self.text.append('F')
                if key[pygame.K_g]:
                    self.text.append('G')
                if key[pygame.K_h]:
                    self.text.append('H')
                if key[pygame.K_j]:
                    self.text.append('J')
                if key[pygame.K_k]:
                    self.text.append('K')
                if key[pygame.K_l]:
                    self.text.append('L')
                if key[pygame.K_z]:
                    self.text.append('Z')
                if key[pygame.K_x]:
                    self.text.append('X')
                if key[pygame.K_b]:
                    self.text.append('B')
                if key[pygame.K_n]:
                    self.text.append('N')
                if key[pygame.K_m]:
                    self.text.append('M')

            draw_text(self.get_text() + ' |', font, (0, 0, 0), self.x + 1 * display.scr_w, self.y + 2 * display.scr_w)
        draw_text(self.get_text(), font, (0, 0, 0), self.x + 2 * display.scr_w, self.y + 2 * display.scr_h)

    def get_text(self):
        return f" {str(''.join(self.text))}"

    def get_raw_text(self):
        return str(''.join(self.text))


class MainMenu:
    def __init__(self, scr_w, scr_h, bg):
        self.start_button = Button(
            (211 * scr_w, 205 * scr_h),
            (1003 * scr_w, 341 * scr_h), "", PLAY_BUTTON, layout.button_X, 0)
        self.exit_button = Button(
            (503 * scr_w, 28 * scr_h),
            (1416 * scr_w, 0 * scr_h), "выход", None, layout.button_O, 1)
        self.options_button = Button(
            (503 * scr_w, 28 * scr_h),
            (0 * scr_w, 0 * scr_h), "настройки", None, layout.button_Triangle, 3)
        self.bg = bg
        self.GUI = MAIN_MENU_GUI
        self.enabled = False
        self.is_hide = False

    def show(self, mouse_click, joy_click):
        if not self.is_hide:
            scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_bg, (0, 0))
            scaled_GUI = pygame.transform.scale(self.GUI, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_GUI, (0, 0))
            self.start_button.show()
            self.exit_button.show()
            self.exit_button.click(mouse_click, joy_click)
            self.start_button.click(mouse_click, joy_click)
            self.options_button.show()
            self.options_button.click(mouse_click, joy_click)

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def hide(self):
        self.is_hide = True

    def show_(self):
        self.is_hide = False


# class OnlineBattle:
#     def __init__(self, bg, player_heroes, player_name=None):
#         self.bg = bg
#         self.enabled = False
#         self.is_hide = False
#         self.player_heroes = player_heroes
#         self.player_name = player_name
#         self.cansel_button = ButtonVisual("отменить", font, (500, 100), (710, 900))
#         # self.enemy_heroes = enemy_heroes
#         self.player_hero_1 = CardButton(player_heroes[0], (100 * display.scr_w, 500 * display.scr_h),
#                                         layout.button_Square, 2)
#         self.player_hero_2 = CardButton(player_heroes[1], (350 * display.scr_w, 500 * display.scr_h),
#                                         layout.button_X, 0)
#         self.player_hero_3 = CardButton(player_heroes[2], (600 * display.scr_w, 500 * display.scr_h),
#                                         layout.button_O, 1)
#
#     def show(self, mouse_click, chosen, enemy_pick, enemy_name, joy_click):
#         scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
#         display.screen.blit(scaled_bg, (0, 0))
#
#         if enemy_name:
#             scaled_found = pygame.transform.scale(BATTLE_MENU_FOUND, (display.screen_width, display.screen_height))
#             display.screen.blit(scaled_found, (0, 0))
#             self.player_hero_1.show()
#             self.player_hero_2.show()
#             self.player_hero_3.show()
#             draw_text(self.player_name, font, (255, 255, 255), 100, 300)
#             if not chosen:
#                 self.player_hero_1.click(mouse_click, joy_click)
#                 self.player_hero_2.click(mouse_click, joy_click)
#                 self.player_hero_3.click(mouse_click, joy_click)
#             if enemy_pick:
#                 enemy_hero_1 = CardButtonEnemy(enemy_pick[0],
#                                          (display.screen_width - 250, 500))
#                 enemy_hero_2 = CardButtonEnemy(enemy_pick[1],
#                                          (display.screen_width - 500, 500))
#                 enemy_hero_3 = CardButtonEnemy(enemy_pick[2],
#                                          (display.screen_width - 750, 500))
#                 enemy_hero_1.show()
#                 enemy_hero_2.show()
#                 enemy_hero_3.show()
#             draw_text(enemy_name, font, (255, 255, 255), 1170, 300)
#         else:
#             self.cansel_button.show()
#             self.cansel_button.click(mouse_click)
#
#     def is_enabled(self):
#         return self.enabled
#
#     def disable(self):
#         self.enabled = False
#
#     def enable(self):
#         self.enabled = True
#
#     def hide(self):
#         self.is_hide = True
#
#     def show_(self):
#         self.is_hide = False


class ChooseHeroMenu:
    def __init__(self, bg):
        self.exit_button = Button(
            (60, 60),
            (1845, 7), "", HERO_PICK_BACK, layout.button_O, 1)
        self.super_pau_v1 = CardButton((100 * display.scr_w, 100 * display.scr_h), True, card.pau)
        self.super_pau_v2 = CardButton((500 * display.scr_w, 100 * display.scr_h), False, card.pau_v2,
                                      ("Пройди BOSS RUSH,", "сложность ТЕРПИ"))

        self.vesisa_v1 = CardButton((100 * display.scr_w, 450 * display.scr_h), True, card.vesisa)
        self.vesisa_v2 = CardButton((500 * display.scr_w, 450 * display.scr_h), False, card.vesisa_v2, "Пройди историю")

        self.lisa_v1 = CardButton((100 * display.scr_w, 800 * display.scr_h), True, card.lisa)
        self.lisa_v2 = CardButton((500 * display.scr_w, 800 * display.scr_h), False, card.lisa_v2)

        self.bg = bg
        self.enabled = False
        self.is_hide = False
        self.player_picking = 0

    def show(self, mouse_click, joy_click):
        if not self.is_hide:
            scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_bg, (0, 0))
            self.exit_button.show()
            self.exit_button.click(mouse_click, joy_click)
            self.super_pau_v1.show()
            self.super_pau_v1.click(mouse_click, joy_click)
            self.vesisa_v1.show()
            self.vesisa_v1.click(mouse_click, joy_click)
            self.super_pau_v2.show()
            self.super_pau_v2.click(mouse_click, joy_click)
            self.vesisa_v2.show()
            self.vesisa_v2.click(mouse_click, joy_click)
            self.lisa_v1.show()
            self.lisa_v1.click(mouse_click, joy_click)
            self.lisa_v2.show()
            self.lisa_v2.click(mouse_click, joy_click)
            # p.draw_hero_pick_menu()

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def get_pick(self):
        return self.player_picking

    def hide(self):
        self.is_hide = True

    def show_(self):
        self.is_hide = False


class ChooseOnlineModeMenu:
    def __init__(self, bg, music):
        self.connect_button = Button(
            (496, 108),
            (710, 911), "START", ONLINE_MODE_START, layout.button_X, 0)
        self.exit_button = Button(
            (60, 60),
            (21, 19), "", ONLINE_MODE_BACK, layout.button_O, 1)

        self.bg = bg
        self.GUI = ONLINE_MODE_GUI
        self.enabled = False
        self.is_hide = False
        self.music = music

    def show(self, mouse_click, team, joy_click):
        if not self.is_hide:
            scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_bg, (0, 0))
            scaled_GUI = pygame.transform.scale(self.GUI, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_GUI, (0, 0))
            self.connect_button.show()
            self.exit_button.show()
            # self.start_server.show()
            self.exit_button.click(mouse_click, joy_click)
            self.connect_button.click(mouse_click, joy_click)
            # self.start_server.click(mouse_click)

            team[0].draw_menu((400 * display.scr_w, 420 * display.scr_h))
            team[1].draw_menu((1520 * display.scr_w, 420 * display.scr_h))

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self, enable_music=True):
        if enable_music:
            play_music_bg(self.music)
        self.enabled = True

    def hide(self):
        self.is_hide = True

    def show_(self):
        self.is_hide = False


class ChooseModeMenu:
    def __init__(self, scr_w, scr_h, bg):
        self.campain_button = Button((450 * scr_w, 137 * scr_h), (928 * scr_w, 654 * scr_h), "История",
                                     STORY_MODE_BUTTON, layout.button_X, 0)
        self.online_button = Button(
            (450 * scr_w, 699 * scr_h),
            (1406 * scr_w, 95 * scr_h), "PVP", SURVIVAL_MODE_BUTTON, layout.button_Triangle, 3)
        self.exit_button = Button(
            (997 * scr_w, 173 * scr_h),
            (928 * scr_w, 860 * scr_h), "Назад", BACK_BUTTON, layout.button_O, 1)
        self.boss_rush_button = Button(
            (300 * scr_w, 200 * scr_h),
            (50 * scr_w, 850 * scr_h), "BOSS RUSH", None, layout.button_Square, 2)

        self.skins_button = Button(
            (300 * scr_w, 200 * scr_h),
            (400 * scr_w, 850 * scr_h), "SKINS", None)
        self.gp_button_plus = Button((58 * scr_w, 79 * scr_h),
                                     (1317 * scr_w, 571 * scr_h), "     >", None, layout.none_layout, 14)
        self.gp_button_minus = Button((58 * scr_w, 79 * scr_h),
                                     (929 * scr_w, 571 * scr_h), "     <", None, layout.none_layout, 13)

        self.vid = bg
        self.cap = cv2.VideoCapture(self.vid)
        self.scaled_bg = None

        self.GUI = GAME_MODE_GUI
        self.enabled = False
        self.is_hide = False

    def show(self, mouse_click, joy_click, game_progress, game_completed):
        if not self.is_hide:
            ret, img = self.cap.read()
            if ret:
                img = pygame.image.frombuffer(
                    img.tobytes(), img.shape[1::-1], "BGR")
                self.scaled_bg = pygame.transform.scale(img, (display.screen_width, display.screen_height))
                display.screen.blit(self.scaled_bg, (0, 0))
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                display.screen.blit(self.scaled_bg, (0, 0))
            scaled_gui = pygame.transform.scale(self.GUI, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_gui, (0, 0))
            self.campain_button.show()
            self.exit_button.show()
            self.online_button.show()
            self.skins_button.show()
            self.exit_button.click(mouse_click, joy_click)
            self.campain_button.click(mouse_click, joy_click)
            self.online_button.click(mouse_click, joy_click)
            self.skins_button.click(mouse_click, joy_click)
            if game_completed == 1:
                self.gp_button_plus.show()
                if not game_progress >= 54:
                    self.gp_button_plus.click(mouse_click, joy_click)
                self.gp_button_minus.show()
                if game_progress > 0:
                    self.gp_button_minus.click(mouse_click, joy_click)
                self.boss_rush_button.show()
                self.boss_rush_button.click(mouse_click, joy_click)
            level = pg[game_progress][0]
            if game_progress == 25:
                level = bulat_boss
            draw_windowed_bg_instance(level)
            draw_text(str(game_progress), font, (255, 255, 255), 1136 * display.scr_w,
                      585 * display.scr_h)

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def hide(self):
        self.is_hide = True

    def show_(self):
        self.is_hide = False


class OptionsMenu:
    def __init__(self, scr_w, scr_h, bg):
        self.exit_button = Button(
            (200 * scr_w, 100 * scr_h),
            (1550 * scr_w, 950 * scr_h), "Назад", EXIT_OPTIONS, layout.button_O, 1)
        self.volume_button_minus = ButtonVisual("       -", font, (100, 100), (900 * scr_w, 220 * scr_h))
        self.volume_button_plus = ButtonVisual("      +", font, (100, 100), (1120 * scr_w, 220 * scr_h))
        self.sound_button_minus = ButtonVisual("       -", font, (100, 100), (900 * scr_w, 350 * scr_h))
        self.sound_button_plus = ButtonVisual("      +", font, (100, 100), (1120 * scr_w, 350 * scr_h))
        self.easy_mode = Button((500 * scr_w, 100 * scr_h),
                                (600 * scr_w, 800 * scr_h), "СЛАБОСТЬ", EASY_BUTTON, layout.button_X, 0)
        self.normal_mode = Button((500 * scr_w, 100 * scr_h),
                                  (1200 * scr_w, 800 * scr_h), "NORMAL", NORMAL_BUTTON, layout.button_Square, 2)
        self.hard_mode = Button((500 * scr_w, 100 * scr_h),
                                (600 * scr_w, 950 * scr_h), "ТЕРПИ", HARD_BUTTON, layout.button_Triangle, 3)
        self.bg = bg
        self.enabled = False

    def show(self, mouse_click, joy_click):
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        self.exit_button.show()
        self.volume_button_plus.show()
        self.volume_button_minus.show()
        self.sound_button_plus.show()
        self.sound_button_minus.show()
        self.easy_mode.show()
        self.normal_mode.show()
        self.hard_mode.show()
        self.volume_button_plus.click(mouse_click)
        if settings.get_music_volume() > 0.01:
            self.volume_button_minus.click(mouse_click)
        self.sound_button_plus.click(mouse_click)
        if settings.get_sound_volume() > 0.01:
            self.sound_button_minus.click(mouse_click)
        if settings.get_difficulty() == 0.5:
            self.normal_mode.click(mouse_click, joy_click)
            self.hard_mode.click(mouse_click, joy_click)
        else:
            self.normal_mode.change_text("NORMAL")
            self.hard_mode.change_text("ТЕРПИ")
        if settings.get_difficulty() == 1:
            self.easy_mode.click(mouse_click, joy_click)
            self.hard_mode.click(mouse_click, joy_click)
        else:
            self.easy_mode.change_text("СЛАБОСТЬ")
            self.hard_mode.change_text("ТЕРПИ")
        if settings.get_difficulty() == 1.5:
            self.easy_mode.click(mouse_click, joy_click)
            self.normal_mode.click(mouse_click, joy_click)
        else:
            self.easy_mode.change_text("СЛАБОСТЬ")
            self.normal_mode.change_text("NORMAL")

        self.exit_button.click(mouse_click, joy_click)
        draw_text(str(round(settings.get_music_volume(), 2)), font, (255, 255, 255), 1025 * display.scr_w,
                  245 * display.scr_h)
        draw_text(str(round(settings.get_sound_volume(), 2)), font, (255, 255, 255), 1025 * display.scr_w,
                  365 * display.scr_h)

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
