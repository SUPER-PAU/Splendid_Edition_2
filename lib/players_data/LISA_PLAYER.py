from random import choice

from constants.audio.effects import woman_sound, human_sound
from lib.display import display
from lib.particle import create_damage_number, create_particles
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer
from constants.textures.sprites import bullet_sprites, blood
import pygame


class LisaPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(1, x, y, flip, data, attack_frame)

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
            self.rect.x -= (8 - 16 * self.flip) * display.scr_w
        elif self.blocking:
            self.update_action(3)  # block
            self.rect.x -= (4 - 8 * self.flip) * display.scr_w
        elif self.attacking:
            match self.attack_type:
                case 1:
                    self.update_action(6)  # attack1
                case 2:
                    self.update_action(7)  # attack 2
                case 3:
                    self.update_action(8)  # 3rd attack
        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

    def update(self, animation_list):
        animation_cooldown = 70
        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if the animation is finished
        if self.frame_index >= len(animation_list[self.action]):
            # check if the player is dead then end animation
            if not self.alive:
                self.hit = False
                self.blocking = False
                self.frame_index = len(animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if attack is executed
                if self.action in [6, 7, 8]:
                    self.attacking = False
                    self.attack_cooldown = 20
                    self.dashing = False
                # check if damage was taken
                if self.action == 4:
                    self.hit = False
                    # if player was in the middle of an attack, then attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20
                    self.dashing = False
                # check block
                if self.action == 3:
                    self.blocking = False
                    self.attack_cooldown = 20
                    self.hit = False

        if self.alive:
            if self.action in [6, 7, 8]:
                self.attack_cooldown = 30
                if self.action == 8:
                    self.huge_attack_cooldown = 300
                    if self.frame_index in [2, 3, 7, 8]:
                        self.rect.x += (23 - 46 * self.flip) * display.scr_w
                self.dash()

        # if player is stunned by beam
        if self.stunned > 0:
            self.stunned -= 1
            self.take_damage(0.2)
            self.vel_y = 0

    def attack(self, surface, target, hg_att, hit):
        if self.attack_cooldown == 0 and not self.hit:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None
            block_break = False
            # att 1
            match self.attack_type:
                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.3 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 1.3 * self.rect.width, self.rect.height)
                    # att 2
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                                 2 * self.rect.width, self.rect.height)
                # speshal
                case 3:
                    hit = 15
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height / 2,
                                                 2.5 * self.rect.width, self.rect.height * 1.6)
                    Attack(self, 4, attacking_rect, attacking_rect_2, target, hit, block_break)
                    hit = 20
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.6 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height / 2,
                                                 1.6 * self.rect.width, self.rect.height * 1.6)
                    block_break = True

            if self.attack_type == self.temp_attack:
                self.same_attack_count += 1
            else:
                self.same_attack_count = 0
            self.temp_attack = self.attack_type
            # take damage
            if attacking_rect:
                Attack(self, self.attack_type, attacking_rect, attacking_rect_2, target, hit, block_break)
            # punish player for spamming same attacks)))) heheheha!
            if self.same_attack_count == 3 and target.player != 10:
                target.hit = False
                target.attack_cooldown = 8
                self.same_attack_count = 0

    def take_damage(self, hit, block_break=False):
        if not self.shield_on:
            if block_break or self.jump or self.stunned > 0 or self.sprint or self.attacking:
                self.health -= hit
                self.hit = True
                choice(woman_sound).play()
                create_particles((self.rect.centerx, self.rect.top), self.flip, blood)
                # create_particles((self.rect.centerx, self.rect.top), self.flip, self.particle)
                # choice(self.hurt_sfx).play()
            else:
                hit = round(hit * 0.2)
                self.health -= hit
                self.blocking = True
            self.last_damage_number = hit
            create_damage_number((1750 * display.scr_w, 150 * display.scr_h),
                                 self.flip, hit)
        else:
            self.shield_on = False

    def draw_cooldown_stats(self, surface):
        # draw atk cooldown
        pygame.draw.rect(surface, (255, 255, 255),
                         ((1450 - 2) * display.scr_w, (1020 - 2) * display.scr_h, (440 + 4) * display.scr_w,
                          19 * display.scr_h))
        pygame.draw.rect(surface, (204, 51, 0),
                         (1450 * display.scr_w, 1020 * display.scr_h, 440 * display.scr_w, 15 * display.scr_h))
        pygame.draw.rect(surface, (0, 0, 0),
                         (
                             1450 * display.scr_w, 1020 * display.scr_h, self.attack_cooldown * 8 * display.scr_w,
                             15 * display.scr_h))

        # draw huge attack cooldown
        pygame.draw.rect(surface, (255, 255, 255),
                         ((1100 - 2) * display.scr_w, (60 - 2) * display.scr_h, (300 + 4) * display.scr_w,
                          19 * display.scr_h))
        pygame.draw.rect(surface, (70, 70, 195), (
            1100 * display.scr_w, 60 * display.scr_h, 300 * display.scr_w,
            15 * display.scr_h))
        pygame.draw.rect(surface, (0, 0, 90), (
            1100 * display.scr_w, (60 + 10) * display.scr_h, 300 * display.scr_w,
            5 * display.scr_h))
        pygame.draw.rect(surface, (120, 120, 255), (
            1100 * display.scr_w, 60 * display.scr_h, 300 * display.scr_w,
            5 * display.scr_h))
        if self.huge_attack_cooldown > 0:
            pygame.draw.rect(surface, (0, 0, 0),
                             (1100 * display.scr_w, 60 * display.scr_h, self.huge_attack_cooldown * display.scr_w,
                              15 * display.scr_h))
        else:
            pygame.draw.rect(surface, (204, 255, 255), (
                1100 * display.scr_w, 60 * display.scr_h, 300 * display.scr_w,
                15 * display.scr_h))
            pygame.draw.rect(surface, (0, 255, 255), (
                1100 * display.scr_w, (60 + 7) * display.scr_h, 300 * display.scr_w,
                8 * display.scr_h))


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, attack_type, rect, rect2, target, damage, block_break=False):
        super().__init__(bullet_sprites)
        match attack_type:
            case 1:  # attack1
                self.attack_frame = player.attack_frame[0]
            case 2:  # attack 2
                self.attack_frame = player.attack_frame[1]
            # 3rd attack
            case 3:
                self.attack_frame = player.attack_frame[2]
            case 4:
                self.attack_frame = 8
        self.block_break = block_break
        self.rect, self.rect2 = rect, rect2
        self.player = player
        self.target = target
        self.damage = damage
        self.hit = False

    def update(self):
        if self.player.attacking and not self.hit and not self.player.hit:
            if self.attack_frame == self.player.frame_index:
                attacking_rect = pygame.Rect(
                    self.player.rect.centerx - (1.3 * self.player.rect.width * self.player.flip),
                    self.rect.y,
                    self.rect.width, self.rect.height)
                # pygame.draw.rect(display.screen, (255, 255, 0), attacking_rect)
                if attacking_rect.colliderect(self.target.rect) or self.rect2.colliderect(self.target.rect):
                    self.target.take_damage(self.damage, self.block_break)
                    self.hit = True
                    create_damage_number((50 * display.scr_w, 150 * display.scr_h),
                                         self.target.flip, self.target.last_damage_number)
                    if not self.target.blocking:
                        create_particles((self.target.rect.centerx, self.target.rect.top), self.target.flip, blood)
                        choice(human_sound).play()
        else:
            self.kill()

