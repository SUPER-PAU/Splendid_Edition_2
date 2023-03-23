import pygame
import cv2
import pyperclip

from lib.display import display
from constants.fonts.turok import sys as font
from lib.mixer import play_music_bg
from lib.Settings import settings
from lib.drawer import draw_text


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
VOL_PLUS = pygame.image.load(
    r'assets\images\UI\plus_volume.png').convert_alpha()
VOL_MIN = pygame.image.load(
    r'assets\images\UI\minus_volume.png').convert_alpha()
EASY_BUTTON = pygame.image.load(
    r'assets\images\UI\easy_button.png').convert_alpha()
NORMAL_BUTTON = pygame.image.load(
    r'assets\images\UI\normal_button.png').convert_alpha()
EXIT_OPTIONS = pygame.image.load(
    r'assets\images\UI\exit_options_button.png').convert_alpha()


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, size, pos, text, clicked_image=None):
        self.x, self.y = pos
        self.size = self.width, self.height = size
        self.clicked = False
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.render = None
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
        # display.screen.blit(self.surface, (self.x, self.y))
        # pygame.draw.rect(self.surface, (255, 255, 255), self.rect)

    def click(self, mouse_click):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if self.clicked_image:
                display.screen.blit(self.clicked_image, (0, 0))
            self.change_text(self.text, "Black")
            if pygame.mouse.get_pressed()[0] and mouse_click:
                self.clicked = True
        else:
            self.change_text(self.text)

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
                self.clicked = False

    def show(self, key_press):
        key = pygame.key.get_pressed()
        if self.clicked and key_press:
            if key[pygame.K_BACKSPACE] and len(self.text) > 0:
                self.text.pop()
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
            if key[pygame.K_PERIOD]:
                self.text.append('.')

            if key[pygame.K_v]:
                self.text.append(str(pyperclip.paste()))
            if key[pygame.K_c]:
                pyperclip.copy(self.get_text())
            draw_text(self.get_text() + ' |', font, (0, 0, 0), 935, 734)
        draw_text(self.get_text(), font, (0, 0, 0), 935, 734)

    def get_text(self):
        return str("".join(self.text))


class MainMenu:
    def __init__(self, scr_w, scr_h, bg, music):
        self.start_button = Button(
            (211 * scr_w, 205 * scr_h),
            (1003 * scr_w, 341 * scr_h), "", PLAY_BUTTON)
        self.exit_button = Button(
            (503 * scr_w, 28 * scr_h),
            (1416 * scr_w, 0 * scr_h), "выход")
        self.options_button = Button(
            (503 * scr_w, 28 * scr_h),
            (0 * scr_w, 0 * scr_h), "настройки")
        self.bg = bg
        self.GUI = MAIN_MENU_GUI
        self.enabled = False
        self.is_hide = False
        self.music = music
        play_music_bg(self.music)

    def show(self, mouse_click):
        if not self.is_hide:
            scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_bg, (0, 0))
            scaled_GUI = pygame.transform.scale(self.GUI, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_GUI, (0, 0))
            self.start_button.show()
            self.exit_button.show()
            self.exit_button.click(mouse_click)
            self.start_button.click(mouse_click)
            self.options_button.show()
            self.options_button.click(mouse_click)

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
        play_music_bg(self.music)

    def hide(self):
        self.is_hide = True

    def show_(self):
        self.is_hide = False


class ChooseOnlineModeMenu:
    def __init__(self, scr_w, scr_h, bg, music):
        self.connect_button = Button(
            (420 * scr_w, 330 * scr_h),
            (1406 * scr_w, 94 * scr_h), "connect")
        self.start_server = Button(
            (418 * scr_w, 333 * scr_h),
            (1406 * scr_w, 460 * scr_h), "start")
        self.exit_button = Button(
            (997 * scr_w, 173 * scr_h),
            (928 * scr_w, 860 * scr_h), "Назад", BACK_BUTTON)
        self.line_edit = LineEdit((468 * scr_w, 59 * scr_h), (928 * scr_w, 733 * scr_h))

        self.bg = bg
        self.GUI = ONLINE_MODE_GUI
        self.enabled = False
        self.is_hide = False
        self.music = music

    def show(self, mouse_click, key_press):
        if not self.is_hide:
            scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_bg, (0, 0))
            scaled_GUI = pygame.transform.scale(self.GUI, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_GUI, (0, 0))
            self.connect_button.show()
            self.exit_button.show()
            self.start_server.show()
            self.exit_button.click(mouse_click)
            self.connect_button.click(mouse_click)
            self.start_server.click(mouse_click)
            self.line_edit.show(key_press)
            self.line_edit.click(mouse_click)

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


class ChooseModeMenu:
    def __init__(self, scr_w, scr_h, bg, music):
        self.campain_button = Button(
            (450 * scr_w, 699 * scr_h),
            (928 * scr_w, 95 * scr_h), "История", STORY_MODE_BUTTON)
        self.online_button = Button(
            (450 * scr_w, 699 * scr_h),
            (1406 * scr_w, 95 * scr_h), "PVP", SURVIVAL_MODE_BUTTON)
        self.exit_button = Button(
            (997 * scr_w, 173 * scr_h),
            (928 * scr_w, 860 * scr_h), "Назад", BACK_BUTTON)

        self.vid = bg
        self.cap = cv2.VideoCapture(self.vid)
        self.ret, img = self.cap.read()
        img = cv2.transpose(img)
        self.surface = pygame.surface.Surface((img.shape[0], img.shape[1]))

        self.GUI = GAME_MODE_GUI
        self.enabled = False
        self.is_hide = False
        self.music = music

    def show(self, mouse_click):
        if not self.is_hide:
            ret, img = self.cap.read()
            if ret:
                img = cv2.transpose(img)
                pygame.surfarray.blit_array(self.surface, img)
                display.screen.blit(self.surface, (0, 0))
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            scaled_GUI = pygame.transform.scale(self.GUI, (display.screen_width, display.screen_height))
            display.screen.blit(scaled_GUI, (0, 0))
            self.campain_button.show()
            self.exit_button.show()
            self.online_button.show()
            self.exit_button.click(mouse_click)
            self.campain_button.click(mouse_click)
            self.online_button.click(mouse_click)

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
            (1550 * scr_w, 950 * scr_h), "Назад", EXIT_OPTIONS)
        self.volume_button_plus = Button((100 * scr_w, 100 * scr_h),
                                         (1100 * scr_w, 220 * scr_h), "     +", VOL_PLUS)
        self.volume_button_minus = Button((100 * scr_w, 100 * scr_h),
                                          (900 * scr_w, 220 * scr_h), "     -", VOL_MIN)
        self.easy_mode = Button((500 * scr_w, 100 * scr_h),
                                         (600 * scr_w, 800 * scr_h), "БОТИК", EASY_BUTTON)
        self.normal_mode = Button((500 * scr_w, 100 * scr_h),
                                          (1200 * scr_w, 800 * scr_h), "NORMAL", NORMAL_BUTTON)

        self.bg = bg
        self.enabled = False

    def show(self, mouse_click):
        scaled_bg = pygame.transform.scale(self.bg, (display.screen_width, display.screen_height))
        display.screen.blit(scaled_bg, (0, 0))
        self.exit_button.show()
        self.volume_button_plus.show()
        self.volume_button_minus.show()
        self.easy_mode.show()
        self.normal_mode.show()
        self.volume_button_plus.click(mouse_click)
        if settings.get_music_volume() > 0:
            self.volume_button_minus.click(mouse_click)
        if settings.get_difficulty() == 0.5:
            self.normal_mode.click(mouse_click)
        else:
            self.normal_mode.change_text("NORMAL")
        if settings.get_difficulty() == 1:
            self.easy_mode.click(mouse_click)
        else:
            self.easy_mode.change_text("БОТИК")
        self.exit_button.click(mouse_click)
        draw_text(str(round(settings.get_music_volume(), 2)), font, (255, 255, 255), 1025 * display.scr_w,
                  245 * display.scr_h)

    def is_enabled(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
