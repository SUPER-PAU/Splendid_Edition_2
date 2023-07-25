import pygame


pygame.joystick.init()

supported_controllers = ['DualSense Wireless Controller', 'PS4 Controller']


class Joystick:
    def __init__(self):
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.main_joystick = None
        self.layout = "mouse"
        if joysticks:
            self.main_joystick = joysticks[0]
            print(self.main_joystick.get_name())
            if self.main_joystick.get_name() not in supported_controllers:
                self.main_joystick = None

    def change_layout(self, x):
        self.layout = x

    def get_layout(self):
        return self.layout

    def locate_joystick(self):

        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.main_joystick = None
        if joysticks:
            self.main_joystick = joysticks[0]
            # print(self.main_joystick.get_name())
            if self.main_joystick.get_name() not in supported_controllers:
                self.main_joystick = None

    def get_joystick(self):
        return self.main_joystick


joystick = Joystick()


def get_j(*args):
    return False



