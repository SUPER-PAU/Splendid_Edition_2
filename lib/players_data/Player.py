import pygame
from lib.display import display
from lib.particle import create_damage_number

player_spec = [1, 9, 12]
player_attack3 = [1, 9]
player_shield = [9]


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

    def reset_params(self):
        x, y, self.flip = self.start_pos
        self.rect = pygame.Rect((x, y, self.data[3][0], self.data[3][1]))
        self.hit = False
        self.shield_on = False
        self.dashing = False
        self.alive = True
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
        self.huge_attack_cooldown = 300
        self.shield_cooldown = 200
        self.health = 100
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - attack1, 4 - attack2, 5 -hit, 6 - death
        self.frame_index = 0
        self.ready = False

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
        self.draw_cooldown_stats(surface)

    def draw_cooldown_stats(self, surface):
        # draw atk cooldown
        pygame.draw.rect(surface, (255, 255, 255),
                         ((30 - 2) * display.scr_w, (1020 - 2) * display.scr_h, (440 + 4) * display.scr_w,
                          19 * display.scr_h))
        pygame.draw.rect(surface, (0, 0, 0),
                         (30 * display.scr_w, 1020 * display.scr_h, 440 * display.scr_w, 15 * display.scr_h))
        pygame.draw.rect(surface, (204, 51, 0),
                         (
                             30 * display.scr_w, 1020 * display.scr_h, (440 - self.attack_cooldown * 8) * display.scr_w,
                             15 * display.scr_h))
        # draw huge attack cooldown
        if self.player in player_spec:

            pygame.draw.rect(surface, (255, 255, 255),
                             ((520 - 2) * display.scr_w, (60 - 2) * display.scr_h, (300 + 4) * display.scr_w,
                              19 * display.scr_h * display.scr_h))
            pygame.draw.rect(surface, (0, 0, 0),
                             (520 * display.scr_w, 60 * display.scr_h, 300 * display.scr_w, 15 * display.scr_h))
            if self.huge_attack_cooldown > 0:
                pygame.draw.rect(surface, (70, 70, 195), (
                    520 * display.scr_w, 60 * display.scr_h, (300 - self.huge_attack_cooldown) * display.scr_w,
                    15 * display.scr_h))
                pygame.draw.rect(surface, (0, 0, 90), (
                    520 * display.scr_w, (60 + 10) * display.scr_h, (300 - self.huge_attack_cooldown) * display.scr_w,
                    5 * display.scr_h))
                pygame.draw.rect(surface, (120, 120, 255), (
                    520 * display.scr_w, 60 * display.scr_h, (300 - self.huge_attack_cooldown) * display.scr_w,
                    5 * display.scr_h))
            else:
                pygame.draw.rect(surface, (204, 255, 255), (
                    520 * display.scr_w, 60 * display.scr_h, (300 - self.huge_attack_cooldown) * display.scr_w,
                    15 * display.scr_h))
                pygame.draw.rect(surface, (0, 255, 255), (
                    520 * display.scr_w, (60 + 7) * display.scr_h, (300 - self.huge_attack_cooldown) * display.scr_w,
                    8 * display.scr_h))

        if self.player in player_shield:
            pygame.draw.rect(surface, (255, 255, 255), (
                (20 - 2) * display.scr_w, (60 - 2) * display.scr_h, (200 + 4) * display.scr_w,
                19 * display.scr_h))
            pygame.draw.rect(surface, (0, 0, 0),
                             (20 * display.scr_w, 60 * display.scr_h, 200 * display.scr_w, 15 * display.scr_h))
            if self.shield_cooldown > 0:
                pygame.draw.rect(surface, (0, 102, 0), (
                    20 * display.scr_w, 60 * display.scr_h, (200 - self.shield_cooldown) * display.scr_w,
                    15 * display.scr_h))
                pygame.draw.rect(surface, (0, 51, 0), (
                    20 * display.scr_w, (60 + 10) * display.scr_h, (200 - self.shield_cooldown) * display.scr_w,
                    5 * display.scr_h))
                pygame.draw.rect(surface, (51, 153, 51), (
                    20 * display.scr_w, 60 * display.scr_h, (200 - self.shield_cooldown) * display.scr_w,
                    5 * display.scr_h))
            else:
                pygame.draw.rect(surface, (102, 255, 102), (
                    20 * display.scr_w, 60 * display.scr_h, (200 - self.shield_cooldown) * display.scr_w,
                    15 * display.scr_h))
                pygame.draw.rect(surface, (102, 255, 153), (
                    20 * display.scr_w, (60 + 7) * display.scr_h, (200 - self.shield_cooldown) * display.scr_w,
                    8 * display.scr_h))

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
        if self.dashing:
            self.rect.x += self.dash_x * display.scr_w
            if self.player == 4:
                self.shield_on = True

    def stun(self):
        self.stunned = 45

    def take_damage(self, hit, block_break=False):
        if not self.shield_on:
            self.health -= hit
            self.hit = True
            if not self.stunned:
                create_damage_number((50 * display.scr_w, 150 * display.scr_h),
                                     self.flip, hit)
                # create_particles((self.rect.centerx, self.rect.top), self.flip, self.particle)
                # choice(self.hurt_sfx).play()
        else:
            self.shield_on = False
            # shield_sfx.play()
            # create_particles((self.rect.centerx, self.rect.top), self.flip, shield_parts)
