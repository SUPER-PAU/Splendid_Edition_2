from lib.display import display
from lib.joystick import joystick


def screen_shake(time):
    display.shake(time)
    if joystick.get_joystick():
        joystick.shake_j(time)


def shake_damage():
    if joystick.get_joystick():
        joystick.shake_j_low()
