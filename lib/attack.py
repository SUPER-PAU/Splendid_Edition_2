from random import choice

import pygame

from constants.audio.effects import explosion_sounds
from constants.textures.sprites import bullet_sprites, dumplings
from lib.display import display
from lib.screen_effects import screen_shake
from lib.particle import create_green_energy, create_explosion, create_allside_particles


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, rect, rect2, target, damage, block_break=False, is_enemy=False):
        super().__init__(bullet_sprites)
        if not is_enemy:
            match player.attack_type:
                case 1 | 4 | 5 | 9 | 10 | 15 | 17 | 22:  # attack1
                    self.attack_frame = player.attack_frame[0]
                case 20 | 11 | 8 | 2 | 6 | 3 | 14 | 16 | 27 | 7:  # attack 2
                    self.attack_frame = player.attack_frame[1]
                # 3rd attack
                case 12 | 13 | 21 | 18:
                    self.attack_frame = player.attack_frame[2]
        else:
            match player.attack_type:
                case 1 | 4 | 5 | 7 | 9 | 10 | 15 | 16 | 18 | 22 | 25 | 29:  # attack1
                    self.attack_frame = player.attack_frame[0]
                # attack 2
                case 20 | 11 | 8 | 2 | 6 | 3 | 14 | 17 | 21 | 23 | 26 | 27:
                    self.attack_frame = player.attack_frame[1]
                # 3rd attack
                case 12 | 13 | 24 | 19 | 28 | 30:
                    self.attack_frame = player.attack_frame[2]
        self.attack_type = player.attack_type
        self.block_break = block_break
        self.rect, self.rect2 = rect, rect2
        self.player = player
        self.target = target
        self.damage = damage
        self.sfx_done = False
        self.hit = False
        self.is_enemy = is_enemy

    def update(self):
        if self.player.attacking and not self.hit and not self.player.hit:
            if self.attack_frame == self.player.frame_index:
                if self.attack_type == 29:
                    a = -250
                    if not self.player.flip:
                        a += 500
                    bullet_rect = pygame.Rect(self.player.rect.centerx + (a * display.scr_w),
                                              self.player.rect.bottom,
                                              150 * display.scr_w, 150 * display.scr_h)
                    bullet_data = [200, 2 * display.scr_w, (40, 40), [2, 2], self.player.flip]
                    create_green_energy(bullet_rect, bullet_data, self.target, self.damage)
                    self.hit = True
                else:
                    # pygame.draw.rect(display.screen, (255, 0, 0), self.rect)
                    if not self.sfx_done:
                        match self.attack_type:
                            case 13:
                                screen_shake(30)
                                pygame.mixer.Sound.play(choice(explosion_sounds))
                            case 16:
                                if self.is_enemy:
                                    create_allside_particles((self.rect.centerx, self.rect.top), dumplings, 2)
                                    pygame.mixer.Sound.play(choice(explosion_sounds))
                                    screen_shake(20)
                            case 1:
                                if self.player.player == 7 and not self.is_enemy:
                                    create_allside_particles((self.rect.centerx, self.rect.top), dumplings, 2)
                                    pygame.mixer.Sound.play(choice(explosion_sounds))
                                    screen_shake(20)
                            case 5:
                                if self.is_enemy and self.player.player == 7:
                                    screen_shake(10)
                            case 30:
                                screen_shake(15)
                            case 17:
                                if self.is_enemy and self.player.player == 26:
                                    screen_shake(12)

                        self.sfx_done = True
                    if self.rect.colliderect(self.target.rect) or self.rect2.colliderect(self.target.rect):
                        self.target.take_damage(self.damage, self.block_break)
                        self.hit = True
        else:
            self.kill()


class Attack2(pygame.sprite.Sprite):
    def __init__(self, player, rect, rect2, target, damage, block_break=False, is_enemy=False):
        super().__init__(bullet_sprites)
        self.attack_frame = player.attack_frame[3]
        self.block_break = block_break
        self.rect, self.rect2 = rect, rect2
        self.player = player
        self.target = target
        self.damage = damage
        self.hit = False

    def update(self):
        if self.player.attacking and not self.hit and not self.player.hit:
            self.rect = pygame.Rect(self.player.rect.centerx - (2.5 * self.player.rect.width * self.player.flip),
                                    self.player.rect.y - self.player.rect.height / 2,
                                    2.5 * self.player.rect.width, self.player.rect.height * 1.6)
            if self.attack_frame == self.player.frame_index:
                if self.player.player == 18:
                    self.player.recharged = 0
                    pygame.mixer.Sound.play(choice(explosion_sounds))
                    explosion_rect1 = pygame.Rect(self.player.rect.centerx - (400 * display.scr_w),
                                                  display.screen_height - 710 * display.scr_h,
                                                  400 * display.scr_w, 600 * display.scr_h)
                    explosion_rect2 = pygame.Rect(self.player.rect.centerx,
                                                  display.screen_height - 710 * display.scr_h,
                                                  400 * display.scr_w, 600 * display.scr_h)
                    offset = 34
                    if self.player.flip:
                        offset = 40
                    explosion_data = [127, 7.7 * display.scr_w, (offset, 10), [5], self.player.flip]
                    create_explosion(explosion_rect1, explosion_data, self.target, self.damage)
                    create_explosion(explosion_rect2, explosion_data, self.target, self.damage)
                    self.hit = True
                    screen_shake(40)
                else:
                    if self.rect.colliderect(self.target.rect) or self.rect2.colliderect(self.target.rect):
                        self.target.take_damage(self.damage, self.block_break)
                        self.hit = True
        else:
            self.kill()
