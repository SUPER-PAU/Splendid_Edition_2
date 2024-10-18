from random import randint

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
    pos = (0, 0)
    if display.shake_time > 0:
        display.update_shake()
        pos = (randint(int(-30 * display.scr_w), int(30 * display.scr_h)),
               randint(int(-30 * display.scr_w), int(30 * display.scr_h)))
    scaled_bg = pygame.transform.scale(bg, (display.screen_width, display.screen_height))
    display.screen.blit(scaled_bg, pos)


def draw_bg_windowed(bg, coords, size):
    scaled_bg = pygame.transform.scale(bg, size)
    display.screen.blit(scaled_bg, coords)


# Отрисовка шкалы здоровья
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(display.screen, color.white,
                     (x - 2 * display.scr_w, y - 2 * display.scr_h, 804 * display.scr_w, 34 * display.scr_h))
    if health > 100:
        ratio = (health - 100) / 100
        pygame.draw.rect(display.screen, (250, 200, 0), (x, y, 800 * display.scr_w, 30 * display.scr_h))
        pygame.draw.rect(display.screen, (195, 155, 0), (x, y + 20 * display.scr_h,
                                                         800 * display.scr_w, 10 * display.scr_h))
        pygame.draw.rect(display.screen, color.yellow, (x, y, 800 * display.scr_w, 10 * display.scr_h))

        pygame.draw.rect(display.screen, (140, 140, 140),
                         (x, y, 800 * ratio * display.scr_w, 30 * display.scr_h))
        pygame.draw.rect(display.screen, (89, 89, 89),
                         (x, y + 20 * display.scr_h, 800 * ratio * display.scr_w, 10 * display.scr_h))
        pygame.draw.rect(display.screen, (179, 179, 179),
                         (x, y, 800 * ratio * display.scr_w, 10 * display.scr_h))
    else:
        pygame.draw.rect(display.screen, color.red,
                         (x, y, 800 * display.scr_w, 30 * display.scr_h))
        pygame.draw.rect(display.screen, (100, 0, 0),
                         (x, (y + 15 * display.scr_h), 800 * display.scr_w, 15 * display.scr_h))
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


def draw_windowed_bg_instance(bg):
    if isinstance(bg, VideoReader):
        bg.draw_animated_bg_windowed((930 * display.scr_w, 98 * display.scr_h), (445 * display.scr_w,
                                                                                 469 * display.scr_h))
    else:
        draw_bg_windowed(bg, (930 * display.scr_w, 98 * display.scr_h), (445 * display.scr_w, 469 * display.scr_h))


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
        pos = (0, 0)
        if display.shake_time > 0:
            display.update_shake()
            pos = (randint(int(-30 * display.scr_w), int(30 * display.scr_h)),
                   randint(int(-30 * display.scr_w), int(30 * display.scr_h)))
        if self.tick == 0:
            self.tick = 1
            ret, img = self.cap.read()
            if ret:
                img = pygame.image.frombuffer(
                    img.tobytes(), img.shape[1::-1], "BGR")
                self.scaled_bg = pygame.transform.scale(img, (display.screen_width, display.screen_height))
                display.screen.blit(self.scaled_bg, pos)

            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            self.tick -= 1
            display.screen.blit(self.scaled_bg, pos)

    def draw_animated_bg_windowed(self, coords, size):
        if self.tick == 0:
            self.tick = 1
            ret, img = self.cap.read()
            if ret:
                img = pygame.image.frombuffer(
                    img.tobytes(), img.shape[1::-1], "BGR")
                self.scaled_bg = pygame.transform.scale(img, size)
                display.screen.blit(self.scaled_bg, coords)

            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            self.tick -= 1
            display.screen.blit(self.scaled_bg, coords)


class CutScene:
    def __init__(self, video, audio):
        self.vid, self.audio = video, audio
        self.playing = False
        self.cap = cv2.VideoCapture(self.vid)
        self.scaled_bg = None
        self.playing_music = False


    def draw(self):
        if self.playing:
            ret, img = self.cap.read()
            if ret:
                img = pygame.image.frombuffer(
                    img.tobytes(), img.shape[1::-1], "BGR")
                self.scaled_bg = pygame.transform.scale(img, (display.screen_width, display.screen_height))
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
