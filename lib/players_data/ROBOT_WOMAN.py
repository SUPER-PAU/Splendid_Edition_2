from constants.textures.sprites import attack_group
from lib.joystick import get_j, joystick
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame

from lib.display import display


class RobotFemalePlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame, sprite):
        super().__init__(1, x, y, flip, data, attack_frame, sprite)
        self.sex = 2
        self.name = "robot_woman"
        self.tpd = False

    def move(self, surface, target, round_over, mouse_click, key_press, joypress):
        SPEED = 8
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.sprint = False
        self.attack_type = 0
        # key presses
        key = pygame.key.get_pressed()
        mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
        if joystick.get_joystick():
            joybutton = joystick.main_joystick.get_button
        else:
            joybutton = get_j

        if (key[pygame.K_LSHIFT] or joybutton(10)) and not self.jump:
            SPEED += 8.3
            self.sprint = True

        # play emoji
        if key[pygame.K_1] and self.emoji_cooldown <= 0:
            self.play_emoji()
            self.emoji_cooldown = 160

        if self.action == 8:
            if self.frame_index == 3 and not self.tpd:
                if target.rect.centerx >= self.rect.centerx:
                    self.rect.centerx = target.rect.right
                    self.flip = True
                elif target.rect.centerx < self.rect.centerx:
                    self.rect.centerx = target.rect.left
                    self.flip = False

                self.tpd = True

        # can only perform other actions if not attacking
        if not self.attacking and self.alive and not round_over and not self.blocking and not self.hit:
            # jump
            if (key[pygame.K_w] or key[pygame.K_SPACE] or joybutton(11)) and self.jump is False:
                self.vel_y = -46
                self.jump = True
            # attack
            if (key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f] or mouse_middle or
               key[pygame.K_e] or joybutton(2) or joybutton(0) or joybutton(1) or joybutton(3))\
                    and (mouse_click or key_press or joypress):
                if self.attack_cooldown <= 0:
                    # determine attack
                    if key[pygame.K_r] or mouse_left or joybutton(0):
                        self.attack_type = 1
                        self.attack(target, attack_group)
                    elif key[pygame.K_f] or mouse_middle or joybutton(3):
                        if self.huge_attack_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                            self.attack_type = 3
                            self.huge_attack_cooldown = 300
                            self.attack(target, attack_group)
                    elif key[pygame.K_t] or mouse_right or joybutton(2):
                        self.attack_type = 2
                        self.attack(target, attack_group)
                    elif key[pygame.K_e] or joybutton(1):
                        self.attack_type = 4
                        self.attack(target, attack_group)
            # movement
            if key[pygame.K_a] or joybutton(13):
                dx = -SPEED
                self.running = True
            if key[pygame.K_d] or joybutton(14):
                dx = SPEED
                self.running = True

            # ensure players face each other
            if target.rect.centerx >= self.rect.centerx and not self.attacking:
                self.flip = False
            elif target.rect.centerx < self.rect.centerx and not self.attacking:
                self.flip = True

        if not self.hit and not self.attacking and not self.blocking:
            # apply gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            # ensure player stays on screen
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > display.screen_width:
                dx = display.screen_width - self.rect.right
            if self.rect.bottom + dy > display.screen_height - 110:
                self.vel_y = 0
                self.jump = False
                dy = display.screen_height - 110 - self.rect.bottom
            # update player position
            self.rect.x += dx
            self.rect.y += dy
        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.emoji_cooldown > 0:
            self.emoji_cooldown -= 1
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def attack(self, target, group):
        if not self.hit:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None
            block_break = False
            hit = 0
            match self.attack_type:
                # att 1
                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.1 * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.6,
                                                 2.1 * self.rect.width, self.rect.height * 0.4)
                    hit = 16
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.3 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 2.3 * self.rect.width, self.rect.height)
                    hit = 12
                case 3:
                    self.tpd = False
                    block_break = True
                    attacking_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.4,
                                                 self.rect.width, self.rect.height * 0.2)
                    hit = 40
                # grab
                case 4:
                    block_break = True
                    attacking_rect = pygame.Rect(self.rect.centerx - (0.7 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 0.7 * self.rect.width, self.rect.height)
                    hit = 15
            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect)
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, self.attack_type, target, hit, group, block_break)