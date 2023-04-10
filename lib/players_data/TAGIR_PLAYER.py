from constants.textures.sprites import attack_group
from lib.players_data.particles_online import create_stone
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame

from lib.display import display


class TagirPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(3, x, y, flip, data, attack_frame)
        self.sex = 1
        self.name = "tagir"

    def move(self, surface, target, round_over, mouse_click, key_press):
        SPEED = 8 * display.scr_w
        GRAVITY = 2 * display.scr_h
        dx = 0
        dy = 0
        self.running = False
        self.sprint = False
        self.attack_type = 0
        # key presses
        key = pygame.key.get_pressed()
        mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()

        if key[pygame.K_LSHIFT] and not self.jump:
            SPEED += 8.3 * display.scr_w
            self.sprint = True

        # play emoji
        if key[pygame.K_1] and self.emoji_cooldown <= 0:
            self.play_emoji()
            self.emoji_cooldown = 160

        # can only perform other actions if not attacking
        if not self.attacking and self.alive and not round_over and not self.blocking and not self.hit:
            # jump
            if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                self.vel_y = -46 * display.scr_h
                self.jump = True
            # attack
            if (key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_e]) and \
                    (mouse_click or key_press):
                if self.attack_cooldown <= 0:
                    # determine attack
                    if key[pygame.K_r] or mouse_left:
                        self.attack_type = 1
                        self.attack(target, attack_group)
                    elif key[pygame.K_t] or mouse_right and self.shield_cooldown <= 0:
                        self.attack_type = 2
                        self.attack(target, attack_group)
                    elif key[pygame.K_e]:
                        self.attack_type = 4
                        self.attack(target, attack_group)
            # movement
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
            if key[pygame.K_d]:
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
            if self.rect.bottom + dy * display.scr_h > display.screen_height - 110 * display.scr_h:
                self.vel_y = 0
                self.jump = False
                dy = display.screen_height - 110 * display.scr_h - self.rect.bottom
            # update player position
            self.rect.x += dx
            self.rect.y += dy
        # apply attack cooldown
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.emoji_cooldown > 0:
            self.emoji_cooldown -= 1

    def attack(self, target, group):
        if not self.hit:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None
            block_break = False
            hit = 0
            # att 1
            match self.attack_type:
                # superpau web
                case 1:
                    dash_rect = pygame.Rect(self.rect.centerx - (1 * self.rect.width * self.flip),
                                            self.rect.y + self.rect.height * 0.3,
                                            1 * self.rect.width, self.rect.height * 0.5)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 14
                    else:
                        self.dash_x = -14
                    hit = 12
                    create_dash_online(dash_rect, self.flip, target, self, hit, group)
                # att 1
                case 2:
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.35,
                                              100 * display.scr_w, 100 * display.scr_h)
                    bullet_data = [200, 0.6 * display.scr_w, (10, 10), [2, 2], self.flip]
                    hit = 20
                    create_stone(bullet_rect, bullet_data, target, hit)
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
        self.rect = pygame.Rect(self.player.rect.centerx - (1 * self.player.rect.width * self.flip),
                                self.player.rect.y + self.player.rect.height * 0.3,
                                1 * self.player.rect.width, self.player.rect.height * 0.5)
        self.rect.x += self.player.dash_x * display.scr_w
        self.rect.y = self.rect.y
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