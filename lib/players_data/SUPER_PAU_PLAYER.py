from random import choice

import pygame

from constants.colors import black, red
from lib.display import display
from lib.drawer import draw_health_bar, draw_text
from lib.particle import create_particles, create_damage_number, create_emoji
from constants.audio.effects import human_sound, woman_sound
from constants.textures.sprites import attack_group, blood
from lib.players_data.Player import PLAYER


class SuperPauPlayer(PLAYER):
    def __init__(self, player, x, y, flip, data, attack_frame):
        super().__init__(player, x, y, flip, data, attack_frame)
        self.sprint = False
        self.emoji_name = "pau"

    def draw_round_statistic(self, name, rounds, font):
        draw_text(f"{name}: {rounds} / {3}", font, black, 17 * display.scr_w,
                  83 * display.scr_h)
        draw_text(f"{name}: {rounds} / {3}", font, red, 20 * display.scr_w,
                  80 * display.scr_h)

    def draw_hp(self):
        draw_health_bar(self.health, 20 * display.scr_w, 20 * display.scr_h)

    def play_emoji(self):
        if self.emoji_name == "lisa":
            emoji_rect = pygame.Rect(
                1470 * display.scr_w, 150 * display.scr_h, 250 * display.scr_w, 250 * display.scr_h)
            emoji_data = [500, 0.5 * display.scr_w, (0, 0), [3], True]
            create_emoji(emoji_rect, emoji_data, self.emoji_name, self)
        else:
            emoji_rect = pygame.Rect(
                250 * display.scr_w, 150 * display.scr_h, 250 * display.scr_w, 250 * display.scr_h)
            emoji_data = [500, 0.5 * display.scr_w, (0, 0), [3], False]
            create_emoji(emoji_rect, emoji_data, self.emoji_name, self)

    def move(self, surface, target, round_over, new_frame):
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

        # heal player aboba os ability sprint
        self.heal(0.017)
        # can only perform other actions if not attacking
        if not self.attacking and self.alive and not round_over and not self.blocking and not self.hit:
            # jump
            if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                self.vel_y = -46 * display.scr_h
                self.jump = True
            # attack
            if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f] \
                    or mouse_middle or key[pygame.K_e]:
                # determine attack
                if key[pygame.K_r] or mouse_left:
                    self.attack_type = 1
                    hit = 12
                    self.attack(surface, target, 1.3, hit)
                elif key[pygame.K_f] or mouse_middle:
                    if self.huge_attack_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                        self.attack_type = 3
                        hit = 35
                        self.huge_attack_cooldown = 300
                        self.attack(surface, target, 1.3, hit)
                elif key[pygame.K_t] or mouse_right:
                    self.attack_type = 2
                    hit = 14
                    self.attack(surface, target, 2.5, hit)
                elif key[pygame.K_e]:
                    print(1)
                    self.attack_type = 4
                    hit = 15
                    self.attack(surface, target, 2.5, hit)
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
        if self.attack_cooldown > 0 and new_frame:
            self.attack_cooldown -= 1
        if self.emoji_cooldown > 0:
            self.emoji_cooldown -= 1

    def check_action(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.hit = False
            self.attacking = False
            self.update_action(5)  # death
        elif self.grabing:
            self.update_action(10)
            self.attacking = True
        elif self.in_grab:
            self.update_action(11)
            self.hit = True
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
                case 4:
                    self.update_action(9)  # grab
        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

    def update(self, animation_list):
        animation_cooldown = 70
        if self.action in [10, 11]:
            animation_cooldown = 100

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
                if self.action in [6, 7, 8, 9]:
                    self.attacking = False
                    self.attack_cooldown = 20
                    self.dashing = False
                if self.action == 10:
                    self.attacking = False
                    self.grabing = False
                    self.attack_cooldown = 20
                    self.dashing = False
                # check if damage was taken
                if self.action == 11:
                    self.hit = False
                    self.in_grab = False
                    # if player was in the middle of an attack, then attack is stopped
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
            if self.action == 11:
                if self.frame_index in [2, 3]:
                    self.rect.x -= (23 - 46 * self.flip) * display.scr_w
            if self.action in [6, 7, 8, 9, 10]:
                self.attack_cooldown = 30
                if self.action == 8:
                    self.huge_attack_cooldown = 300
                self.dash()

    def attack(self, surface, target, hg_att, hit):
        if self.attack_cooldown == 0 and not self.hit:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None
            block_break = False
            # att 1
            match self.attack_type:
                # att 1
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip), self.rect.y,
                                                 2.5 * self.rect.width, self.rect.height)
                # superpau web
                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.4,
                                                 3 * self.rect.width, self.rect.height * 1.4)
                # spau speshal
                case 3:
                    block_break = True
                    attacking_rect = pygame.Rect(self.rect.centerx - (3.7 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.7,
                                                 3.7 * self.rect.width, self.rect.height * 1.7)
                # grab
                case 4:
                    block_break = True
                    attacking_rect = pygame.Rect(self.rect.centerx - (0.7 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 0.7 * self.rect.width, self.rect.height)
            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect)
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, self.attack_type, target, hit, block_break)

    def take_damage(self, hit, block_break=False):
        if block_break or self.jump or self.stunned > 0 or self.sprint or self.attacking:
            self.health -= hit
            self.hit = True
            create_particles((self.rect.centerx, self.rect.top), self.flip, blood)
            choice(human_sound).play()
            self.update_huge_attack_cd(100)
        else:
            hit = round(hit * 0.2)
            self.health -= hit
            self.blocking = True
            self.update_huge_attack_cd(60)
        create_damage_number((50 * display.scr_w, 150 * display.scr_h),
                             self.flip, hit)
        self.last_damage_number = hit


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, rect, rect2, attack_type, target, damage, block_break=False):
        super().__init__(attack_group)
        match player.attack_type:
            case 1:  # attack1
                self.attack_frame = player.attack_frame[0]
            case 2:  # attack 2
                self.attack_frame = player.attack_frame[1]
            # 3rd attack
            case 3:
                self.attack_frame = player.attack_frame[2]
            case 4:
                self.attack_frame = player.attack_frame[3]
        self.attack_type = attack_type
        self.block_break = block_break
        self.rect, self.rect2 = rect, rect2
        self.player = player
        self.target = target
        self.damage = damage
        self.hit = False

    def update(self, target):
        if self.player.attacking and not self.hit and not self.player.hit:
            if self.attack_frame == self.player.frame_index:

                # pygame.draw.rect(display.screen, (255, 255, 0), self.rect)

                if self.rect.colliderect(target.rect) or self.rect2.colliderect(target.rect):
                    self.player.was_attacking = (self.damage, self.block_break)
                    if self.attack_type == 4:
                        if not target.jump or not target.attacking:
                            self.player.update_huge_attack_cd(50)
                            create_particles((target.rect.centerx, target.rect.top), target.flip, blood)
                            choice(woman_sound).play()
                            self.player.grabing = True
                            create_damage_number((1750 * display.scr_w, 150 * display.scr_h),
                                                 target.flip, round(self.damage))
                            self.hit = True
                    else:
                        # target.take_damage(self.damage, self.block_break)
                        ratio = 0.2
                        if self.block_break or target.jump or target.sprint or target.attacking:
                            ratio = 1
                            self.player.update_huge_attack_cd(50)
                            create_particles((target.rect.centerx, target.rect.top), target.flip, blood)
                            choice(woman_sound).play()
                        else:
                            self.player.update_huge_attack_cd(30)
                        create_damage_number((1750 * display.scr_w, 150 * display.scr_h),
                                             target.flip, round(self.damage * ratio))
                        self.hit = True

        else:
            self.kill()
