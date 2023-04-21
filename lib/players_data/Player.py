from random import choice

import pygame

from constants.audio.effects import human_sound, woman_sound
from constants.colors import black, red
from constants.textures.sprites import blood
from lib.display import display
from lib.drawer import draw_health_bar, draw_text
from lib.players_data.particles_online import create_damage_number, create_particles

player_spec = [1, 2, 4]
player_attack3 = [1, 2]
player_shield = [3, 2]


class PLAYER:

    def __init__(self, player, x, y, flip, data, attack_frame):

        self.data = data
        self.player, self.size, self.image_scale, self.offset = player, data[0], data[1], data[2]
        self.attack_frame = attack_frame
        self.start_pos = x, y, flip
        self.flip = flip
        self.rect = pygame.Rect((x, y, data[3][0], data[3][1]))
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - attack1, 4 - attack2, 5 -hit, 6 - death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.hit_cooldown = 0
        self.running = False
        self.dashing = False
        self.jump = False
        self.attacking = False
        self.blocking = False
        self.was_attacking = None
        self.last_damage_number = 0
        self.attack_type = 0
        self.attack_cooldown = 0
        self.same_attack_count = 0
        self.temp_attack = 100
        self.huge_attack_cooldown = 300
        self.shield_cooldown = 200
        self.health = 100
        self.emoji_cooldown = 0
        self.dash_x = 0
        self.stunned = 0
        self.hit = False
        self.shield_on = False
        self.alive = True
        self.ready = False
        self.playing_emoji = False
        self.grabing = False
        self.in_grab = False
        self.sprint = False
        self.invisible = False
        self.is_tank = False
        self.knifes = 0
        self.side = 1
        self.sex = 1
        self.prev_hit = 0
        self.hit_timer = 6
        self.fire_cooldown = 0

    def set_side(self, player):
        self.side = player
        if player == 1:
            self.start_pos = 400, 540, False
        else:
            self.start_pos = 1400, 540, True
        self.reset_pos()

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite_sheets
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def reset_pos(self):
        x, y, self.flip = self.start_pos
        self.rect = pygame.Rect((x, y, self.data[3][0], self.data[3][1]))
        self.hit = False
        self.shield_on = False
        self.dashing = False
        self.alive = True
        self.grabing = False
        self.in_grab = False
        self.knifes = 0
        self.invisible = False
        self.blocking = False
        self.running = False
        self.jump = False
        self.attacking = False
        self.was_attacking = None
        self.playing_emoji = False
        self.same_attack_count = 0
        self.vel_y = 0
        self.dash_x = 0
        self.attack_type = 0
        self.attack_cooldown = 0
        self.prev_hit = 0
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - attack1, 4 - attack2, 5 -hit, 6 - death
        self.frame_index = 0
        self.ready = False
        self.hit_timer = 6
        self.fire_cooldown = 0

    def reset_params(self):
        x, y, self.flip = self.start_pos
        self.rect = pygame.Rect((x, y, self.data[3][0], self.data[3][1]))
        self.hit = False
        self.shield_on = False
        self.dashing = False
        self.alive = True
        self.grabing = False
        self.in_grab = False
        self.invisible = False
        self.blocking = False
        self.running = False
        self.jump = False
        self.attacking = False
        self.was_attacking = None
        self.playing_emoji = False
        self.is_tank = False
        self.same_attack_count = 0
        self.fire_cooldown = 0
        self.stunned = 0
        self.prev_hit = 0
        self.vel_y = 0
        self.dash_x = 0
        self.attack_type = 0
        self.attack_cooldown = 0
        self.huge_attack_cooldown = 300
        self.shield_cooldown = 200
        self.health = 100
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - attack1, 4 - attack2, 5 -hit, 6 - death
        self.frame_index = 0
        self.ready = False
        self.hit_timer = 6

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update anim settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def ready_for_fight(self):
        self.ready = True

    def is_ready(self):
        return self.ready

    def draw_round_statistic(self, name, font):
        if self.side == 1:
            draw_text(f"{name}   {round(self.health)}/100", font, black, 7,
                      83)
            draw_text(f"{name}   {round(self.health)}/100", font, red, 10,
                      80)
        else:
            draw_text(f"{name}   {round(self.health)}/100", font, black, 1087,
                      83)
            draw_text(f"{name}   {round(self.health)}/100", font, red, 1090,
                      80)

    def draw_hp(self):
        self.draw_cooldown_stats(display.screen)
        if self.side == 1:
            draw_health_bar(self.health, 20, 20)
        else:
            draw_health_bar(self.health, 1100, 20)

    def get_attack_stats(self):
        temp = self.was_attacking
        self.was_attacking = False
        return temp

    def clear_attack_stats(self):
        self.was_attacking = None

    def get_animation_params(self):
        return self.action, self.frame_index

    def draw(self, surface, img):
        img = pygame.transform.flip(img, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))

    def draw_cooldown_stats(self, surface):
        if self.side == 1:
            # draw huge attack cooldown
            if self.player in player_spec:
                pygame.draw.rect(surface, (255, 255, 255), ((520 - 2), (60 - 2), (300 + 4),  19))
                pygame.draw.rect(surface, (0, 0, 0), (520, 60, 300, 15))
                if self.huge_attack_cooldown > 0:
                    pygame.draw.rect(surface, (70, 70, 195), (520, 60, (300 - self.huge_attack_cooldown), 15))
                    pygame.draw.rect(surface, (0, 0, 90), (520, (60 + 10), (300 - self.huge_attack_cooldown), 5))
                    pygame.draw.rect(surface, (120, 120, 255), (520, 60, (300 - self.huge_attack_cooldown), 5))
                else:
                    pygame.draw.rect(surface, (204, 255, 255), (520, 60, (300 - self.huge_attack_cooldown), 15))
                    pygame.draw.rect(surface, (0, 255, 255), (520, (60 + 7), (300 - self.huge_attack_cooldown), 8))

            if self.player in player_shield:
                pygame.draw.rect(surface, (255, 255, 255), ((20 - 2), (60 - 2), (200 + 4), 19))
                pygame.draw.rect(surface, (0, 0, 0), (20, 60, 200, 15))

                if self.shield_cooldown > 0:
                    pygame.draw.rect(surface, (0, 102, 0), (20, 60, (200 - self.shield_cooldown), 15))
                    pygame.draw.rect(surface, (0, 51, 0), (20, (60 + 10), (200 - self.shield_cooldown), 5))
                    pygame.draw.rect(surface, (51, 153, 51), (20, 60, (200 - self.shield_cooldown), 5))
                else:
                    pygame.draw.rect(surface, (102, 255, 102), (20, 60, (200 - self.shield_cooldown), 15))
                    pygame.draw.rect(surface, (102, 255, 153), (20, (60 + 7), (200 - self.shield_cooldown), 8))
        else:
            # draw huge attack cooldown
            if self.player in player_spec:
                pygame.draw.rect(surface, (255, 255, 255), (1098, 58, 304, 19))
                pygame.draw.rect(surface, (70, 70, 195), (1100, 60, 300, 15))
                pygame.draw.rect(surface, (0, 0, 90), (1100, 70, 300, 5))
                pygame.draw.rect(surface, (120, 120, 255), (1100, 60, 300, 5))
                if self.huge_attack_cooldown > 0:
                    pygame.draw.rect(surface, (0, 0, 0), (1100, 60, self.huge_attack_cooldown, 15))
                else:
                    pygame.draw.rect(surface, (204, 255, 255), (1100, 60, 300, 15))
                    pygame.draw.rect(surface, (0, 255, 255), (1100, 67, 300, 8))
            if self.player in player_shield:
                pygame.draw.rect(surface, (255, 255, 255), (1698, 58, 204, 19))
                pygame.draw.rect(surface, (0, 102, 0), (1700, 60, 200, 15))
                pygame.draw.rect(surface, (0, 51, 0), (1700, 70, 200, 5))
                pygame.draw.rect(surface, (51, 153, 51), (1700, 60, 200, 5))

                if self.shield_cooldown > 0:
                    pygame.draw.rect(surface, (0, 0, 0), (1700, 60, self.shield_cooldown, 15))
                else:
                    pygame.draw.rect(surface, (102, 255, 102), (1700, 60, (200 - self.shield_cooldown), 15))
                    pygame.draw.rect(surface, (102, 255, 153), (1700, 67, (200 - self.shield_cooldown), 8))

    def heal(self, amount):
        if self.alive:
            if self.health + amount >= 100:
                self.health = 100
            else:
                self.health += amount

    def update_huge_attack_cd(self, amount):
        if self.alive:
            if self.huge_attack_cooldown - amount <= 0:
                self.huge_attack_cooldown = 0
            else:
                self.huge_attack_cooldown -= amount

    def dash(self):
        if self.dashing and self.attacking:
            self.rect.x += self.dash_x
            if self.player == 4:
                self.shield_on = True

    def stun(self):
        self.stunned = 45

    def take_damage(self, hit, block_break=False, sender=2):
        hit = round(hit)
        if not (hit == self.prev_hit and self.hit) and self.hit_timer <= 0:
            if block_break or self.jump or self.stunned > 0 or self.sprint or self.attacking:
                if sender == 2:
                    self.hit_timer = 6
                    self.prev_hit = hit
                    self.health -= hit
                    self.hit = True
                    self.update_huge_attack_cd(100)
                create_particles((self.rect.centerx, self.rect.top), self.flip, blood)
                if self.sex == 1:
                    choice(human_sound).play()
                elif self.sex == 2:
                    choice(woman_sound).play()
            else:
                hit = round(hit * 0.2)
                if sender == 2:
                    self.hit_timer = 6
                    self.prev_hit = hit
                    self.health -= hit
                    self.blocking = True
                    self.update_huge_attack_cd(60)
            if sender == 2:
                if self.side == 1:
                    create_damage_number((50, 150),
                                         self.flip, hit)
                else:
                    create_damage_number((1750, 150),
                                         self.flip, hit)

    def set_on_fire(self):
        self.fire_cooldown = 250

    def burn(self, img):
        img = pygame.transform.flip(img, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        display.screen.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))
        self.fire_cooldown -= 1
        self.health -= 0.1
