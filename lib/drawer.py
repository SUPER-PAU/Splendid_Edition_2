import pygame
from lib.display import display
import constants.colors as color
import cv2
from lib.mixer import play_music


# Отрисовка текста
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    display.screen.blit(img, (x, y))


# Отрисовка фона
def draw_bg(bg):
    scaled_bg = pygame.transform.scale(bg, (display.screen_width, display.screen_height))
    display.screen.blit(scaled_bg, (0, 0))


# Отрисовка шкалы здоровья
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(display.screen, color.white,
                     (x - 2 * display.scr_w, y - 2 * display.scr_h, 804 * display.scr_w, 34 * display.scr_h))
    pygame.draw.rect(display.screen, color.red,
                     (x, y, 800 * display.scr_w, 30 * display.scr_h))
    pygame.draw.rect(display.screen, (100, 0, 0),
                     (x, (y + 15) * display.scr_w, 800 * display.scr_w, 15 * display.scr_h))
    pygame.draw.rect(display.screen, (250, 200, 0),
                     (x, y, 800 * ratio * display.scr_w, 30 * display.scr_h))
    pygame.draw.rect(display.screen, (195, 155, 0),
                     (x, y + 20 * display.scr_h, 800 * ratio * display.scr_w, 10 * display.scr_h))
    pygame.draw.rect(display.screen, color.yellow,
                     (x, y, 800 * ratio * display.scr_w, 10 * display.scr_h))


def check_bg_instance(bg):
    if isinstance(bg, VideoReader):
        bg.draw_animated_bg()
    else:
        draw_bg(bg)


class VideoReader:
    def __init__(self, bg):
        self.tick = 0
        self.vid = bg
        self.cap = cv2.VideoCapture(self.vid)
        self.ret, img = self.cap.read()
        img = cv2.transpose(img)
        self.surface = pygame.surface.Surface((img.shape[0], img.shape[1]))
        self.scaled_bg = None

    def draw_animated_bg(self):
        if self.tick == 0:
            self.tick = 4
            ret, img = self.cap.read()
            if ret:
                img = cv2.transpose(img)
                pygame.surfarray.blit_array(self.surface, img)
                self.scaled_bg = pygame.transform.scale(self.surface, (display.screen_width, display.screen_height))
                display.screen.blit(self.scaled_bg, (0, 0))

            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            self.tick -= 1
            display.screen.blit(self.scaled_bg, (0, 0))


class CutScene:
    def __init__(self, video, audio):
        self.vid, self.audio = video, audio
        self.playing = False
        self.cap = cv2.VideoCapture(self.vid)
        self.ret, img = self.cap.read()
        img = cv2.transpose(img)
        self.surface = pygame.surface.Surface((img.shape[0], img.shape[1]))
        self.scaled_bg = None
        self.playing_music = False

    def draw(self):
        if self.playing:
            ret, img = self.cap.read()
            if ret:
                img = cv2.transpose(img)
                pygame.surfarray.blit_array(self.surface, img)
                self.scaled_bg = pygame.transform.scale(self.surface, (display.screen_width, display.screen_height))
                display.screen.blit(self.scaled_bg, (0, 0))
                if not self.playing_music:
                    play_music(self.audio)
                    self.playing_music = True
            else:
                self.stop()

    def stop(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.playing = False
        self.playing_music = False

    def play(self):
        self.playing = True
        # da

    def is_playing(self):
        return self.playing
