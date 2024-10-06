from random import choice

from constants.audio.effects import bt_sound
from constants.textures.sprites import attack_group
from lib.joystick import get_j, joystick
from lib.players_data.particles_online import create_tank_bullet, create_damage_number, create_beam
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame

from lib.display import display


class Bt25T(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame, sprite):
        super().__init__(2, x, y, flip, data, attack_frame, sprite)
        self.sex = 3
        self.name = "bt25t"
        self.is_tank = True

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
        # can only perform other actions if not attacking
        if not self.attacking and self.alive and not round_over and not self.blocking and not self.hit:
            # attack
            if (key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f] or mouse_middle
                or joybutton(2) or joybutton(0) or joybutton(3)) \
                    and (mouse_click or key_press or joypress):
                if self.attack_cooldown <= 0:
                    # determine attack
                    if (key[pygame.K_r] or mouse_left or joybutton(0)) and self.shield_cooldown <= 0:
                        self.attack_type = 1
                        self.shield_cooldown = 200
                        self.attack(target, attack_group)
                    elif key[pygame.K_f] or mouse_middle or joybutton(3):
                        if self.huge_attack_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                            self.attack_type = 3
                            self.huge_attack_cooldown = 300
                            self.attack(target, attack_group)
                    elif (key[pygame.K_t] or mouse_right or joybutton(2)) and self.shield_cooldown <= 0:
                        self.attack_type = 2
                        self.shield_cooldown = 200
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
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1
        if self.emoji_cooldown > 0:
            self.emoji_cooldown -= 1
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def check_action(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.hit = False
            self.attacking = False
            self.update_action(5)  # death
        elif self.hit:
            self.update_action(4)  # hit
            self.dashing = False
        elif self.blocking:
            self.update_action(4)  # block
            self.dashing = False
        elif self.attacking:
            match self.attack_type:
                case 1:
                    self.update_action(6)  # attack1
                case 2:
                    self.update_action(7)  # attack 2
                case 3:
                    self.update_action(7)  # attack 2
        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

    def attack(self, target, group):
        if not self.hit:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None
            block_break = False
            hit = 0
            # att 1
            match self.attack_type:
                case 1:
                    dash_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                            self.rect.y + self.rect.height * 0.2,
                                            2.5 * self.rect.width, self.rect.height)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 16
                    else:
                        self.dash_x = -16
                    hit = 20
                    create_dash_online(dash_rect, self.flip, target, self, hit, attack_group)
                case 2:
                    size = 50
                    bullet_data = [20, 9.1, (10, 6), [2, 2], self.flip]
                    bullet_rect = pygame.Rect(self.rect.right * 0.9 - (self.rect.width * 0.2 * self.flip),
                                              self.rect.y + self.rect.height * 0.4,
                                              size, size)
                    hit = 20
                    create_tank_bullet(bullet_rect, bullet_data, target, hit)
                case 3:
                    size = 50
                    bullet_data = [20, 9.1, (10, 6), [2, 2], self.flip]
                    bullet_rect = pygame.Rect(self.rect.right * 0.9 - (self.rect.width * 0.2 * self.flip),
                                              self.rect.y + self.rect.height * 0.4,
                                              size, size)
                    hit = 20
                    create_beam(bullet_rect, bullet_data, target, hit)
            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect)
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, self.attack_type, target, hit, group, block_break)

    def take_damage(self, hit, block_break=False, sender=2):
        if not (hit == self.prev_hit and self.hit) and self.hit_timer <= 0:
            hit = round(hit * 0.5)
            choice(bt_sound).play()
            if sender == 2:
                self.hit_timer = 6
                self.prev_hit = hit
                self.health -= hit
                self.hit = True
                self.update_huge_attack_cd(60)
                if self.side == 1:
                    create_damage_number((50, 150),
                                         self.flip, hit)
                else:
                    create_damage_number((1750, 150),
                                         self.flip, hit)


def create_dash_online(rect, flip, target, player, damage, group):
    Dash(rect, flip, target, player, damage, group)


class Dash(pygame.sprite.Sprite):
    def __init__(self, rect, flip, target, player, damage, sprite_group):
        super().__init__(sprite_group)
        self.rect = rect.copy()
        self.action = 0  # 0 - idle
        self.frame_index = 0
        self.flip = flip
        self.hit = False
        self.target = target
        self.damage = damage
        self.player = player
        self.update_time = pygame.time.get_ticks()

    def update(self, enemy, player, n=1):
        self.player = player
        self.target = enemy
        self.move(enemy, n)
        if not self.player.attacking:
            self.kill()

    def move(self, target, n):
        self.rect.x += self.player.dash_x
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)
        self.attack(target, n)

    def attack(self, target, n):
        if self.hit and (target.hit or target.blocking):
            self.kill()
        else:
            if n == 1 and self.hit:
                pass
            else:
                if self.rect.colliderect(target.rect):
                    self.hit = True
                    target.take_damage(self.damage, True, n)
