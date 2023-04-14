from constants.textures.sprites import attack_group
from lib.players_data.particles_online import create_bullet
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame

from lib.display import display


class AksenovPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(5, x, y, flip, data, attack_frame)
        self.sex = 2
        self.name = "aksenov"

    def move(self, surface, target, round_over, mouse_click, key_press):
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

        if key[pygame.K_LSHIFT] and not self.jump:
            SPEED += 8.3
            self.sprint = True

        # play emoji
        if key[pygame.K_1] and self.emoji_cooldown <= 0:
            self.play_emoji()
            self.emoji_cooldown = 160

        # can only perform other actions if not attacking
        if not self.attacking and self.alive and not round_over and not self.blocking and not self.hit:
            # jump
            if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                self.vel_y = -46
                self.jump = True
            # attack
            if (key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or
               key[pygame.K_e]) and (mouse_click or key_press):
                if self.attack_cooldown <= 0:
                    # determine attack
                    if key[pygame.K_r] or mouse_left:
                        self.attack_type = 1
                        self.attack(target, attack_group)
                    elif key[pygame.K_t] or mouse_right:
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
            # att 1
            match self.attack_type:
                # superpau web
                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.09 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 1.09 * self.rect.width, self.rect.height)
                    hit = 30
                case 2:
                    size = 25
                    bullet_data = [20, 4.55, (10, 6), [2, 2], self.flip]
                    bullet_rect = pygame.Rect(self.rect.right * 0.9 - (self.rect.width * 0.2 * self.flip),
                                              self.rect.y + self.rect.height * 0.4,
                                              size, size)
                    hit = 8
                    create_bullet(bullet_rect, bullet_data, target, hit)
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
