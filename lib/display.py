import pygame
from ctypes import windll


class Display:
    def __init__(self):
        # Нативное разрешение пользователя
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)
        # self.screen_width = 640
        # self.screen_height = 360
        # settings = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1)
        # self.refresh_rate = int(getattr(settings, 'DisplayFrequency'))
        self.refresh_rate = 60
        # Разрешение экрана для pygame
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        # Разрешение в сравнении с нативным
        self.scr_w = self.screen_width / 1920
        self.scr_h = self.screen_height / 1080

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
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RES)
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
