import pygame
from ctypes import windll


class Display:
    def __init__(self):
        # Нативное разрешение пользователя
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)
        self.native = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        # self.screen_width = 1280
        # self.screen_height = 720
        # settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)
        # self.refresh_rate = int(getattr(settings, 'DisplayFrequency'))
        self.refresh_rate = 60
        # Разрешение экрана для pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        # Разрешение в сравнении с нативным
        self.scr_w = self.screen_width / 1920
        self.scr_h = self.screen_height / 1080

        self.shake_time = 0

        # Получение окна
        self.get_screen()
        # Заголовок окна
        self.set_caption("Великолепное Издание 2")
        # icon
        self.programIcon = pygame.image.load(r'assets\images\UI\icon.ico')
        self.set_icon(self.programIcon)

    def get_screen(self):
        return self.screen

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, icon):
        pygame.display.set_icon(icon)

    def set_fps(self, fps):
        self.refresh_rate = fps

    def shake(self, time):
        self.shake_time += time

    def update_shake(self):
        self.shake_time -= 1

    def set_online_window(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.scr_w = 1
        self.scr_h = 1
        if self.native == (self.screen_width, self.screen_height):
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def set_normal_window(self):
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)
        self.scr_w = self.screen_width / 1920
        self.scr_h = self.screen_height / 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)


display = Display()


class ServerDisplay:
    def __init__(self):
        # Нативное разрешение пользователя
        # self.screen_width = windll.user32.GetSystemMetrics(0)
        # self.screen_height = windll.user32.GetSystemMetrics(1)
        self.screen_width = 300
        self.screen_height = 200
        # settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)
        # self.refresh_rate = int(getattr(settings, 'DisplayFrequency'))
        self.refresh_rate = 10
        # Разрешение экрана для pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        # Разрешение в сравнении с нативным
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)
        self.scr_w = self.screen_width / 1920
        self.scr_h = self.screen_height / 1080

        # Получение окна
        self.get_screen()
        # Заголовок окна
        self.set_caption("Server")

    def get_screen(self):
        return self.screen

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, icon):
        pygame.display.set_icon(icon)

    def set_fps(self, fps):
        self.refresh_rate = fps
