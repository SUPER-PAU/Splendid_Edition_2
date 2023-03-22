import pygame
from lib.display import display


class Enemy:
    def __init__(self):
        self.jump_cooldown = 150
        self.was_stunned = False

    def move_ai(self, slf, check_coords, close_check_coords, speed, target):
        bot_check_rect = pygame.Rect(slf.rect.centerx - (check_coords[0] * slf.rect.width * slf.flip),
                                     slf.rect.y / check_coords[1],
                                     check_coords[0] * slf.rect.width, slf.rect.height * check_coords[1])
        bot_far_check_rect = pygame.Rect(
            slf.rect.centerx - ((check_coords[0] * slf.rect.width + 300 * display.scr_w) * slf.flip),
            slf.rect.y / check_coords[1],
            check_coords[0] * slf.rect.width + 300 * display.scr_w, slf.rect.height * check_coords[1])
        # близко ли игрок
        bot_close_check_rect = pygame.Rect(slf.rect.centerx - (close_check_coords[0] * slf.rect.width * slf.flip),
                                           slf.rect.y / close_check_coords[1],
                                           slf.rect.width * close_check_coords[0],
                                           slf.rect.height * close_check_coords[1])
        # pygame.draw.rect(display.screen, (255, 255, 0), bot_check_rect)
        # pygame.draw.rect(display.screen, (255, 255, 255), bot_close_check_rect)
        GRAVITY = 2 * display.scr_h
        dx = 0
        dy = 0
        slf.sprint = False
        if not bot_far_check_rect.colliderect(target.rect):
            speed += 8.3 * display.scr_w
            slf.sprint = True
        # movement
        if bot_close_check_rect.colliderect(target.rect) and slf.flip:
            dx = speed
            slf.running = True
        elif not bot_check_rect.colliderect(target.rect) and slf.flip:
            dx = -speed
            slf.running = True
        if bot_close_check_rect.colliderect(target.rect) and not slf.flip:
            dx = -speed
            slf.running = True
        elif not bot_check_rect.colliderect(target.rect) and not slf.flip:
            dx = speed
            slf.running = True

        # apply gravity
        slf.vel_y += GRAVITY
        dy += slf.vel_y

        # ensure player stays on screen
        if slf.rect.left + dx < 0:
            dx = -slf.rect.left
        if slf.rect.right + dx > display.screen_width:
            dx = display.screen_width - slf.rect.right
        if slf.rect.bottom + dy * display.scr_h > display.screen_height - 110 * display.scr_h:
            slf.vel_y = 0
            slf.jump = False
            dy = display.screen_height - 110 * display.scr_h - slf.rect.bottom
        # update player position
        if not slf.hit:
            slf.rect.x += dx
            slf.rect.y += dy
