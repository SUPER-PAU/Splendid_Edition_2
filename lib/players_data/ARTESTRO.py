from constants.audio.effects import shield_sfx
from constants.textures.sprites import attack_group, dust, knife
from lib.players_data.particles_online import create_knife, create_particles
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame

from lib.display import display

knife_img = pygame.transform.scale(knife, (60, 60))


class ArtestroPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(2, x, y, flip, data, attack_frame)
        self.sex = 1
        self.knifes = 0
        self.name = "artestro"

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
            if (key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f] or mouse_middle or
               key[pygame.K_e]) and (mouse_click or key_press):
                if self.attack_cooldown <= 0:
                    # determine attack
                    if key[pygame.K_r] or mouse_left:
                        if self.knifes > 0:
                            self.attack_type = 3
                            self.attack(target, attack_group)
                        else:
                            self.attack_type = 1
                            self.attack(target, attack_group)
                    elif key[pygame.K_f] or mouse_middle:
                        if self.huge_attack_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                            self.knifes += 5
                            self.huge_attack_cooldown = 300
                            shield_sfx.play()
                            create_particles((self.rect.centerx, self.rect.top), self.flip, dust)
                    elif key[pygame.K_t] or mouse_right:
                        if self.knifes > 0:
                            if self.knifes == 1:
                                self.attack_type = 3
                                self.attack(target, attack_group)
                            else:
                                if not self.hit:
                                    self.attacking = True
                                    self.attack_type = 3
                                    hit = 8 * self.knifes
                                    bullet_data = [200, 0.6, (5, 3), [2, 2], self.flip]
                                    for i in range(self.knifes):
                                        bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                                                  self.rect.y + self.rect.height * (0.1 + i * 0.15),
                                                                  50, 50)
                                        create_knife(bullet_rect, bullet_data, target, hit)
                                    self.knifes = 0
                        else:
                            if self.shield_cooldown <= 0:
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
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1
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
                case 1:
                    hit = 10
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.7 * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.6,
                                                 2.7 * self.rect.width, self.rect.height * 0.4)
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                                   self.rect.y - self.rect.height * 0.5,
                                                   2 * self.rect.width, self.rect.height * 1.5)
                # att 1
                case 2:
                    self.shield_cooldown = 200
                    hit = 20
                    dash_rect = pygame.Rect(self.rect.x, self.rect.y + 50, self.rect.width,
                                            self.rect.height - 50)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 30
                    else:
                        self.dash_x = -30
                    create_dash_online(dash_rect, self.flip, target, self, hit, attack_group)
                case 3:
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.35,
                                              50, 50)
                    bullet_data = [200, 0.6, (5, 3), [2, 2], self.flip]
                    hit = 10
                    create_knife(bullet_rect, bullet_data, target, hit)
                    self.knifes -= 1
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

    def draw(self, surface, img):
        img = pygame.transform.flip(img, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))
        for i in range(self.knifes):
            if not self.flip:
                imeg = pygame.transform.flip(knife_img, self.flip, False)
                display.screen.blit(imeg,
                                    ((self.rect.left - 60) + 60 * i,
                                     self.rect.y + self.rect.height * 0.35))
            else:
                imeg = pygame.transform.flip(knife_img, self.flip, False)
                display.screen.blit(imeg,
                                    (self.rect.right - 60 * i,
                                     self.rect.y + self.rect.height * 0.35))


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
        if n == 1:
            self.move()
        self.attack(enemy, n)
        if not self.player.attacking:
            self.kill()

    def move(self):
        self.rect.x += self.player.dash_x
        # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)

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
