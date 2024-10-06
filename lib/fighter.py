import pygame
from random import randint, choice

from lib.mixer import play_music_bg
from constants.audio.music import the_stains_of_time, the_only_thing_i_know, a_stranger_i_remain, red_sun
from lib.attack import Attack, Attack2
from lib.display import display
from lib.particle import create_particles, create_bullet, create_dash, create_beam, create_rocket, create_bombing, \
    create_energy, create_stone, create_damage_number, create_explosion, create_grenade, OnFire
from constants.audio.effects import shield_sfx, shield_on_sfx, explosion_sounds, charge_sounds, gaubica_sounds, \
    bulat_fight, pain_sounds
from lib.Settings import settings
from constants.textures.sprites import shield_parts, dust
from lib.screen_effects import screen_shake

player_spec = [7, 8, 10, 11, 1, 15, 16, 18, 22, 25, 9, 26]
player_attack3 = [1, 15, 16, 18, 22, 9, 10, 26]
player_shield = [10, 1, 14, 16, 20, 22]
bomb_levels = [7, 15, 16, 23, 41, 45]


class FighterEnemy:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, hurt_fx, particle_sprite, partcl_type,
                 attack_frame):
        self.data = data
        self.attack_frame = attack_frame
        self.player, self.size, self.image_scale, self.offset = player, data[0], data[1], data[2]
        self.start_pos = (x, y, flip)
        self.flip = flip
        self.animation_list = self.load_images(pygame.image.load(sprite_sheet).convert_alpha(), animation_steps)
        self.rect = pygame.Rect((x, y, data[3][0], data[3][1]))
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - attack1, 4 - attack2, 5 -hit, 6 - death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.dash_x = 0
        self.stunned = 0
        self.cooldown = 55
        self.attack_type = 0
        self.attack_cooldown = 40
        self.huge_attack_cooldown = 300
        self.jump_cooldown = 100
        self.shield_cooldown = 200

        self.base_health = 100
        if self.player == 26:
            self.base_health = 200
        if self.player == 18:
            self.fire_eff = OnFire(self.size, self.image_scale, self.rect)

        self.health = self.base_health
        self.charging = False
        self.recharged = 0
        self.hurt_sfx, self.particle = hurt_fx, particle_sprite
        self.particle_type = partcl_type
        self.hit = False
        self.shield_on = False
        self.invisibility = False
        self.alive = True
        self.running = False
        self.jump = False
        self.attacking = False
        self.dashing = False
        self.was_stunned = False
        self.sec_phrase = False
        self.second_phase = False
        self.dead = False
        self.last_phase = 0

    def reset_params(self):
        x, y, self.flip = self.start_pos
        self.rect = pygame.Rect((x, y, self.data[3][0], self.data[3][1]))
        self.hit = False
        self.shield_on = False
        self.invisibility = False
        self.alive = True
        self.running = False
        self.jump = False
        self.attacking = False
        self.dashing = False
        self.was_stunned = False
        self.charging = False
        self.dead = False
        self.recharged = 0
        self.vel_y = 0
        self.stunned = 0
        self.attack_type = 0
        self.attack_cooldown = 40
        self.huge_attack_cooldown = 300
        self.jump_cooldown = 100
        self.shield_cooldown = 200
        self.health = self.base_health
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - attack1, 4 - attack2, 5 -hit, 6 - death
        self.frame_index = 0
        if self.player == 18:
            self.fire_eff = OnFire(self.size, self.image_scale, self.rect)

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

    def move(self, target, round_over, game_progress, round):
        if game_progress in bomb_levels:
            create_bombing.enable(target)
        self.running = False
        self.attack_type = 0
        # if player is stunned by beam
        # damage
        hit = 10
        SPEED = 10 * display.scr_w
        if self.stunned > 0:
            self.was_stunned = True
            self.stunned -= 1
            self.take_damage(0.2)
            self.attack_cooldown = 0
            self.vel_y = 0
        if self.player == 18:
            if self.alive:
                if self.attacking and self.recharged > 0:
                    self.move_ai((1, 1), (1, 1), 12 * display.scr_w, target)
            if round > 2:
                self.base_health = 200
                if not self.last_phase and self.health < 100 and self.alive:
                    self.last_phase = True
                    self.health = 100
                    target.heal(30)
                elif self.last_phase and self.health >= 100:
                    self.last_phase = False

        # can only perform other actions if not attacking and alive
        if not self.attacking and self.alive and not round_over:
            # matching players
            match self.player:
                # moiseev_roboboss
                case 26:
                    SPEED = 5 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.4 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3.4 * self.rect.width, self.rect.height)
                    if self.recharged > 0:
                        self.attack_type = 34
                        hit = 15
                        self.attack(target, 2.5, hit)
                    if not self.recharged > 0 and not self.charging and not self.attacking:
                        if bot_attack_check_rect.colliderect(target.rect):
                            if self.huge_attack_cooldown <= 0:
                                self.charging = True
                                self.huge_attack_cooldown = 300
                            else:
                                attack_rand = randint(1, 2)
                                if attack_rand == 1:
                                    self.attack_type = 17
                                    hit = 20
                                    self.attack(target, 1.6, hit)
                                else:
                                    self.attack_type = 18
                                    hit = 30
                                    self.attack(target, 1.6, hit)
                    self.move_ai((1.4, 1.1), (1.1, 1), SPEED, target)
                # bt25t
                case 25:
                    SPEED += 2 * display.scr_w
                    self.shield_on = False
                    # attack
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y / 1.2,
                                                        3.5 * self.rect.width, self.rect.height * 1.2)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        if self.huge_attack_cooldown <= 0:
                            self.attack_type = 9
                            hit = 25
                        else:
                            self.attack_type = 3
                            hit = 23
                        self.attack(target, 1.09, hit)
                    self.move_ai((2.3, 1.3), (1.6, 1), SPEED, target)
                # moiseev_bot
                case 24:
                    SPEED -= 1 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3.5 * self.rect.width, self.rect.height)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1:
                            self.attack_type = 1
                            hit = 18
                            self.attack(target, 1.8, hit)
                        else:
                            self.attack_type = 26
                            hit = 12
                            self.attack(target, 2.4, hit)
                    self.move_ai((1.7, 1.3), (1.6, 1), SPEED, target)
                # albinos
                case 23:
                    SPEED += 2
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3.5 * self.rect.width, self.rect.height)
                    # jump
                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -46 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 250
                        # attack
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        self.attack_type = 1
                        hit = 55
                        self.attack(target, 2, hit)
                    self.move_ai((2, 1.3), (1.6, 1), SPEED, target)
                # supertank
                case 22:
                    SPEED -= 3 * display.scr_w
                    self.shield_on = True
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (10 * self.rect.width * self.flip),
                                                        self.rect.y / 4,
                                                        10 * self.rect.width, self.rect.height * 4)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        self.attack_type = 25
                        hit = 25
                        if self.huge_attack_cooldown <= 0:
                            self.attack_type = 24
                            hit = 35
                        elif self.shield_cooldown <= 0:
                            self.attack_type = 23
                            hit = 25
                        self.attack(target, 1.05, hit)
                    self.move_ai((2.3, 2), (0.8, 1), SPEED, target)
                # aynur
                case 21:
                    SPEED -= 1
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3.5 * self.rect.width, self.rect.height)
                    # jump
                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -46 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 250
                    # attack
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1 and game_progress > 2:
                            self.attack_type = 1
                            hit = 14
                            self.attack(target, 2.9, hit)
                        else:
                            self.attack_type = 17
                            hit = 16
                            self.attack(target, 2.4, hit)
                    self.move_ai((2.3, 1.3), (1.6, 1), SPEED, target)
                # security mais
                case 19:
                    SPEED -= 1.5 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y / 1,
                                                        3.5 * self.rect.width, self.rect.height * 1.2)

                    # attack
                    if bot_attack_check_rect.colliderect(target.rect) and game_progress > 0:
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 2 and game_progress > 6:
                            self.attack_type = 3
                            hit = 20
                        else:
                            self.attack_type = 1
                            hit = 14
                        self.attack(target, 1.8, hit)

                    if game_progress > 0:
                        self.move_ai((1.6, 1.1), (1.3, 1), SPEED, target)
                # final boss
                case 18:
                    SPEED += 1 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (10 * self.rect.width * self.flip),
                                                        self.rect.y / 4,
                                                        10 * self.rect.width, self.rect.height * 4)
                    if self.jump_cooldown == 0 and not self.jump and not self.huge_attack_cooldown <= 0 and \
                            not self.charging and self.recharged <= 0:
                        self.vel_y = -46 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 70

                    if not self.second_phase and round > 1:
                        self.second_phase = True
                    if self.second_phase:
                        self.huge_attack_cooldown -= 1

                    if self.last_phase:
                        self.huge_attack_cooldown = 0
                        self.health -= abs(0.2 / settings.get_difficulty())
                    else:
                        self.heal(0.06)

                    if self.recharged > 0:
                        if not self.jump and self.attack_cooldown <= 0:
                            self.vel_y = -50 * display.scr_h
                            self.jump = True
                            self.jump_cooldown = 70
                            self.attack_type = 32
                            hit = 40 * ((self.base_health // 100 + 0.5) - self.health / 100)
                            if self.last_phase:
                                hit = 45
                            self.attack(target, 3.7, hit)

                    if not self.recharged > 0 and not self.charging and not self.attacking:
                        if bot_attack_check_rect.colliderect(target.rect):
                            attack_rand = randint(1, 2)
                            if self.huge_attack_cooldown <= 0:
                                if not self.second_phase:
                                    self.attack_type = 13
                                    hit = 40 * ((self.base_health // 100 + 0.5) - self.health / 100)
                                    self.attack(target, 3.7, hit)
                                    self.jump_cooldown = 150
                                else:
                                    if not self.jump:
                                        self.charging = True
                                        self.huge_attack_cooldown = 300
                                        if self.last_phase:
                                            choice(pain_sounds).play()
                                        else:
                                            choice(charge_sounds).play()
                            elif attack_rand == 1:
                                self.attack_type = 5
                                hit = 25 * ((self.base_health // 100 + 0.5) - self.health / 100)
                                self.attack(target, 1.5, hit)
                            else:
                                self.attack_type = 8
                                hit = 20 * ((self.base_health // 100 + 0.5) - self.health / 100)
                                self.attack(target, 1.5, hit)
                    if not self.charging and self.recharged <= 0:
                        self.move_ai((2.1, 1), (1.3, 1), SPEED, target)
                    else:
                        self.round_over_move()

                # robot_woman
                case 17:
                    SPEED += 1 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (2.3 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        2.3 * self.rect.width, self.rect.height)

                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -45 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 50

                    # attack
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1:
                            self.attack_type = 18
                            hit = 23
                            self.attack(target, 2.1, hit)
                        elif attack_rand == 2:
                            self.attack_type = 17
                            hit = 15
                            self.attack(target, 2.3, hit)
                    self.move_ai((1.7, 1.1), (1.2, 1), SPEED, target)
                # bulat
                case 16:
                    SPEED -= 2 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.4 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3.4 * self.rect.width, self.rect.height)

                    if self.jump_cooldown == 0 and not self.jump and not self.charging and not self.recharged > 0:
                        self.vel_y = -50 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 250
                    if self.recharged > 0:
                        self.attack_type = 31
                        hit = 35
                        self.attack(target, 2.5, hit)
                    if round > 1 and not self.sec_phrase and self.huge_attack_cooldown < 200:
                        bulat_fight.play()
                        self.sec_phrase = True
                    if not self.recharged > 0 and not self.charging and not self.attacking:
                        if bot_attack_check_rect.colliderect(target.rect):
                            if self.huge_attack_cooldown <= 0 and game_progress > 20:
                                if game_progress == 25:

                                    if not self.second_phase and round > 1:
                                        self.second_phase = True
                                        play_music_bg(the_only_thing_i_know)
                                        self.attack_cooldown = self.cooldown
                                        target.attack_coldown = self.cooldown
                                    elif self.second_phase:
                                        self.charging = True
                                        self.huge_attack_cooldown = 300
                                        choice(charge_sounds).play()
                                    else:
                                        self.attack_type = 19
                                        hit = 30
                                        self.attack(target, 2.5, hit)
                                else:
                                    self.attack_type = 1
                                    hit = 20
                                    self.attack(target, 1.5, hit)
                            elif self.shield_cooldown <= 0 and game_progress > 10:
                                self.attack_type = 21
                                hit = 20
                                self.attack(target, 1.05, hit)
                            else:
                                # determine attack
                                self.attack_type = 1
                                hit = 20
                                self.attack(target, 1.5, hit)
                    self.move_ai((1.4, 1.1), (1.1, 1), SPEED, target)
                # vesisa
                case 15:
                    SPEED += 1
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3.5 * self.rect.width, self.rect.height)
                    # jump
                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -50 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 350
                    # attack
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if self.huge_attack_cooldown <= 0 and not self.invisibility:
                            self.invisibility = True
                            shield_sfx.play()
                            self.heal(30)
                            create_particles((self.rect.centerx, self.rect.top), self.flip, dust, 3)
                        elif attack_rand == 1:
                            self.attack_type = 1
                            hit = 19
                            self.attack(target, 2.9, hit)
                        elif attack_rand == 2:
                            self.attack_type = 17
                            hit = 23
                            self.attack(target, 2.4, hit)
                    self.move_ai((2.3, 1.3), (1.6, 1), SPEED, target)
                # kingartema
                case 14:
                    if game_progress > 11:
                        self.cooldown = 30
                    elif round > 1 and game_progress == 11:
                        self.cooldown = 20
                        if not self.second_phase:
                            self.second_phase = True
                            play_music_bg(the_stains_of_time)
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3 * self.rect.width, self.rect.height * 2)
                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -60 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 350
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        self.attack_type = 16
                        hit = 14
                        if self.shield_cooldown <= 0:
                            self.attack_type = 3
                            hit = 20
                        self.attack(target, 1.5, hit)
                    self.move_ai((1.2, 1.3), (1.13, 1), SPEED, target)
                # egor
                case 13:
                    SPEED += 3 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip),
                                                        self.rect.y,
                                                        3 * self.rect.width, self.rect.height)
                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -40 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 250
                    # attack
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1:
                            self.attack_type = 1
                            hit = 20
                        elif attack_rand == 2:
                            self.attack_type = 2
                            hit = 18
                        self.attack(target, 1.5, hit)
                    self.move_ai((1.2, 1.3), (1.13, 1), SPEED, target)
                # tagir
                case 12:
                    SPEED -= 4 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                        self.rect.y / 1.3,
                                                        4 * self.rect.width, self.rect.height * 1.3)
                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -50 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 250
                    # attack
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1:
                            self.attack_type = 15
                            hit = 12
                            self.attack(target, 1.09, hit)
                        else:
                            self.attack_type = 27
                            hit = 12
                            self.attack(target, 1.09, hit)
                    self.move_ai((3, 1.3), (1.13, 1), SPEED, target)

                # moiseev
                case 1:
                    SPEED -= 2 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (4.5 * self.rect.width * self.flip),
                                                        self.rect.y / 1.6,
                                                        4.5 * self.rect.width, self.rect.height * 1.6)

                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -50 * display.scr_h
                        self.jump = True
                        self.jump_cooldown = 250
                    if bot_attack_check_rect.colliderect(target.rect):
                        if self.huge_attack_cooldown <= 0 and game_progress > 13:
                            self.attack_type = 12
                            hit = 35
                        elif self.shield_cooldown <= 0 and game_progress > 13:
                            self.attack_type = 11
                            hit = 29
                        else:
                            self.attack_type = 10
                            hit = 26
                        self.attack(target, 1.05, hit)
                    self.move_ai((3, 1.1), (1.7, 1), SPEED, target)

                # yacuji
                case 3:
                    SPEED -= 2 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y / 1,
                                                        3.5 * self.rect.width, self.rect.height * 1.2)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1:
                            self.attack_type = 1
                            hit = 20
                        elif attack_rand == 2:
                            self.attack_type = 2
                            hit = 18
                        self.attack(target, 1.5, hit)
                    self.move_ai((1.5, 1.1), (1.3, 1), SPEED, target)
                # soldier
                case 5:
                    SPEED -= 5.3 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.7 * self.rect.width * self.flip),
                                                        self.rect.y / 2,
                                                        3.7 * self.rect.width, self.rect.height * 2)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1 and game_progress > 16:
                            self.attack_type = 3
                            hit = 16
                        else:
                            self.attack_type = 33
                            hit = 24
                        self.attack(target, 1.5, hit)
                    self.move_ai((1.8, 1.1), (1.3, 1), SPEED, target)
                # america soldier
                case 6:
                    SPEED -= 5 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                        self.rect.y / 1,
                                                        4 * self.rect.width, self.rect.height * 1.5)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        attack_rand = randint(1, 2)
                        if attack_rand == 1:
                            self.attack_type = 3
                            hit = 16
                        elif attack_rand == 2:
                            self.attack_type = 33
                            hit = 25
                        self.attack(target, 1.5, hit)
                    self.move_ai((2, 1.3), (1.3, 1), SPEED, target)
                # negrominator
                case 7:
                    SPEED -= 4 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                        self.rect.y / 1.3,
                                                        4 * self.rect.width, self.rect.height * 1.3)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        if not self.huge_attack_cooldown == 0 and game_progress > 15:
                            self.attack_type = 3
                            hit = 20
                            self.attack(target, 1.5, hit)
                        else:
                            if self.huge_attack_cooldown == 0:
                                self.attack_type = 5
                                hit = 65
                                self.attack(target, 1.5, hit)
                    self.move_ai((2.6, 1.3), (1.13, 1), SPEED, target)
                # artestro
                case 8:
                    SPEED -= 2 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                        self.rect.y / 1.3,
                                                        4 * self.rect.width, self.rect.height * 1.3)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        if self.huge_attack_cooldown == 0:
                            self.attack_type = 7
                            hit = 55
                        else:
                            self.attack_type = 6
                            hit = 20
                        self.attack(target, 1.5, hit)
                    self.move_ai((2.6, 1.3), (1.13, 1), SPEED, target)
                # lisa boss
                case 9:
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y / 1,
                                                        3.5 * self.rect.width, self.rect.height * 1.2)
                    if self.jump_cooldown == 0 and not self.jump:
                        self.vel_y = -40 * display.scr_h
                        self.jump = True
                        if self.second_phase:
                            self.jump_cooldown = 75
                        else:
                            self.jump_cooldown = 130
                    if not self.second_phase and round > 1 and self.huge_attack_cooldown <= 50:
                        play_music_bg(a_stranger_i_remain)
                        self.second_phase = True
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        if self.huge_attack_cooldown <= 0 and self.second_phase:
                            self.attack_type = 28
                            self.attack(target, 3.7, hit)
                        else:
                            attack_rand = randint(1, 2)
                            if attack_rand == 1:
                                self.attack_type = 1
                                hit = 19
                            elif attack_rand == 2:
                                self.attack_type = 2
                                hit = 14
                            self.attack(target, 1.7, hit)
                    self.move_ai((1.5, 1.1), (1.3, 1), SPEED, target)
                # walker
                case 20:
                    SPEED -= 5 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                        self.rect.y / 1,
                                                        4 * self.rect.width, self.rect.height * 1)
                    if bot_attack_check_rect.colliderect(target.rect):
                        if self.shield_cooldown == 0 and game_progress > 15:
                            self.attack_type = 14
                            hit = 25
                            self.attack(target, 1.5, hit)
                        else:
                            self.attack_type = 22
                            hit = 25
                            self.attack(target, 1.5, hit)

                    self.move_ai((1.2, 1), (0.5, 1), SPEED, target)
                # general
                case 10:
                    if game_progress == 42 and not self.second_phase:
                        if round > 1:
                            self.second_phase = True
                            play_music_bg(red_sun)
                    if self.second_phase and round > 1:
                        SPEED += 2
                        if self.huge_attack_cooldown > 0:
                            self.huge_attack_cooldown -= 1
                    SPEED -= 8 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                        self.rect.y / 1.3,
                                                        4 * self.rect.width, self.rect.height * 1.3)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack
                        if self.huge_attack_cooldown == 0:
                            self.attack_type = 30
                            hit = 45
                            self.attack(target, 1.5, hit)
                        elif self.second_phase and round > 1:
                            self.attack_type = 29
                            hit = 15
                            self.attack(target, 1.5, hit)
                        elif self.shield_cooldown == 0 and not self.second_phase:
                            self.attack_type = 20
                            heal = 15
                            if game_progress > 42:
                                heal = 5
                            self.attack(target, heal, hit)
                    self.move_ai((1.4, 1), (0.5, 1), SPEED, target)
                # pau enemy
                case 11:
                    SPEED -= 4 * display.scr_w
                    # атаковать ли
                    bot_attack_check_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                        self.rect.y / 1,
                                                        3.5 * self.rect.width, self.rect.height * 1.2)
                    if bot_attack_check_rect.colliderect(target.rect):
                        # determine attack

                        if self.huge_attack_cooldown == 0:
                            self.attack_type = 5
                            hit = 20
                        else:
                            self.attack_type = 8
                            hit = 15
                        self.attack(target, 1.5, hit)
                    self.move_ai((1.8, 1.1), (1.3, 1), SPEED, target)
                case _:
                    SPEED -= 5.3 * display.scr_w
                    self.move_ai((1.8, 1.1), (1.3, 1), SPEED, target)
                # pygame.draw.rect(surface, (55, 255, 55), bot_attack_check_rect)
        if not self.attacking and not self.charging:
            # ensure players face each other
            if target.rect.centerx >= self.rect.centerx:
                self.flip = False
            elif target.rect.centerx < self.rect.centerx:
                self.flip = True

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.huge_attack_cooldown > 0:
            self.huge_attack_cooldown -= 1
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        if self.player in player_attack3 and self.action == 7 and self.hit:
            self.huge_attack_cooldown = 300
        elif self.player in player_spec and self.action == 3 and self.hit and \
                self.player not in player_attack3:
            self.huge_attack_cooldown = 300

    def round_over_move(self):
        dy = 0
        GRAVITY = 2 * display.scr_h
        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        if self.rect.bottom + dy * display.scr_h > display.screen_height - 110 * display.scr_h:
            self.vel_y = 0
            self.jump = False
            dy = display.screen_height - 110 * display.scr_h - self.rect.bottom
        self.rect.y += dy

    def move_ai(self, check_coords, close_check_coords, speed, target):

        bot_check_rect = pygame.Rect(self.rect.centerx - (check_coords[0] * self.rect.width * self.flip),
                                     self.rect.y / check_coords[1],
                                     check_coords[0] * self.rect.width, self.rect.height * check_coords[1])
        # близко ли игрок
        bot_close_check_rect = pygame.Rect(self.rect.centerx - (close_check_coords[0] * self.rect.width * self.flip),
                                           self.rect.y / close_check_coords[1],
                                           self.rect.width * close_check_coords[0],
                                           self.rect.height * close_check_coords[1])
        # pygame.draw.rect(display.screen, (255, 255, 0), bot_check_rect)
        # pygame.draw.rect(display.screen, (255, 255, 255), bot_close_check_rect)
        GRAVITY = 2 * display.scr_h
        if self.last_phase:
            GRAVITY = 2.2 * display.scr_h
        dx = 0
        dy = 0
        # movement
        if (self.recharged <= 0 or self.player == 18) and not self.charging:
            if bot_close_check_rect.colliderect(target.rect) and self.flip:
                dx = speed
                self.running = True
            elif not bot_check_rect.colliderect(target.rect) and self.flip:
                dx = -speed
                self.running = True
            if bot_close_check_rect.colliderect(target.rect) and not self.flip:
                dx = -speed
                self.running = True
            elif not bot_check_rect.colliderect(target.rect) and not self.flip:
                dx = speed
                self.running = True

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
        if not self.hit:
            self.rect.x += dx
            self.rect.y += dy

    # handle animation updates
    def update(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.invisibility = False
            self.update_action(6)  # death
        elif self.charging or self.recharged > 0 and not self.attacking:
            if self.player in (26, 18) and not self.last_phase:
                self.heal(0.3)
            self.update_action(8)
            self.hit = False
        elif self.hit:
            self.update_action(5)  # hit
        elif self.attacking:
            match self.attack_type:
                case 1 | 4 | 5 | 7 | 9 | 10 | 15 | 16 | 18 | 22 | 25 | 29 | 33:  # attack1
                    self.update_action(3)
                # attack 2
                case 20 | 11 | 8 | 2 | 6 | 3 | 14 | 17 | 21 | 23 | 26 | 27:
                    self.update_action(4)
                # 3rd attack
                case 12 | 13 | 24 | 19 | 28 | 30:
                    self.update_action(7)
                case 31 | 32 | 34:
                    self.update_action(9)

        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

        if self.player not in [10, 22, 18, 26]:
            animation_cooldown = 63
        elif self.player == 18:
            animation_cooldown = 63
            if self.last_phase and self.attacking:
                animation_cooldown = 68
            if self.charging:
                animation_cooldown = 30
        else:
            animation_cooldown = 83
            if self.attacking and self.attack_type == 29:
                animation_cooldown = 130
            if (self.recharged > 0 or self.charging) and self.player == 26:
                animation_cooldown = 150
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed sinse the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if the animation is finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # check if the player is dead then end animation
            if not self.alive:
                self.hit = False
                self.invisibility = False
                self.dead = True
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                if self.action == 8:
                    if self.recharged <= 0:
                        self.charging = False
                        self.recharged = 3
                self.frame_index = 0
                if self.action in [3, 4, 7, 9]:
                    self.attacking = False
                    self.dashing = False
                    if self.player in [16, 18]:
                        if self.recharged > 0:
                            if self.last_phase:
                                choice(pain_sounds).play()
                            else:
                                choice(charge_sounds).play()
                if self.action == 5:
                    if not self.was_stunned:
                        self.attack_cooldown = 40
                        self.was_stunned = False
                    self.hit = False
                    # if player was in the middle of an attack, then attack is stopped
                    self.attacking = False
                    self.dashing = False
        # update cooldown
        if self.alive:
            if self.action in [3, 4, 7, 9]:
                self.dash()
                if self.player == 22:
                    self.shield_on = False
                if self.player == 23:
                    if self.attacking and (self.frame_index == 3 or self.frame_index == 4):
                        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                                     self.rect.y,
                                                     2 * self.rect.width, self.rect.height)
                        pygame.draw.rect(display.screen, (255, 255, 0), attacking_rect)
                # куллдаун спец атаки
                if self.player in player_attack3 and self.action in [7, 9]:
                    self.huge_attack_cooldown = 300
                    self.attack_cooldown = self.cooldown
                    if self.player == 9:
                        if self.frame_index in [2, 3, 7, 8]:
                            self.rect.x += (23 - 46 * self.flip)
                elif self.action == 3 and self.player in player_spec and self.player \
                        not in player_attack3:
                    self.huge_attack_cooldown = 300
                    self.attack_cooldown = self.cooldown
                # спец аттака 2
                # щит
                elif self.action == 4 and self.player in player_shield:
                    self.shield_cooldown = 200
                    self.attack_cooldown = self.cooldown
                else:
                    self.attack_cooldown = self.cooldown
            # check if damage was taken

    def attack(self, target, hg_att, hit):
        if self.attack_cooldown == 0 and not self.hit and not self.charging:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None
            hit = int(hit * settings.get_difficulty())

            # att 1
            match self.attack_type:

                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (hg_att * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 hg_att * self.rect.width, self.rect.height)
                # att 2
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                                 2 * self.rect.width, self.rect.height * 2)
                # att 1
                case 4:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip), self.rect.y,
                                                 2.5 * self.rect.width, self.rect.height)
                # att 1 megasword
                case 5:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.6 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.4,
                                                 2.6 * self.rect.width, self.rect.height * 1.4)
                # att 2  artestro splash
                case 6:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.7 * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.6,
                                                 2.7 * self.rect.width, self.rect.height * 0.4)
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                                   self.rect.y - self.rect.height * 0.5,
                                                   2 * self.rect.width, self.rect.height * 1.5)
                # dash att 2
                case 7:
                    dash_rect = pygame.Rect(self.rect.x, self.rect.y + 50 * display.scr_h, self.rect.width,
                                            self.rect.height)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 30
                    else:
                        self.dash_x = -30
                    create_dash(dash_rect, self.flip, target, self, hit)
                # superpau web
                case 8:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.8 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.4,
                                                 2.8 * self.rect.width, self.rect.height * 1.4)
                # bt dash
                case 9:
                    dash_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                            self.rect.y + self.rect.height * 0.2,
                                            2.5 * self.rect.width, self.rect.height)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 16
                    else:
                        self.dash_x = -16
                    create_dash(dash_rect, self.flip, target, self, hit)
                # mois down
                case 10:
                    attacking_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                 self.rect.y + (self.rect.height * 0.2),
                                                 4 * self.rect.width, self.rect.height / 1.4)
                # mois up
                case 11:
                    attacking_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.7,
                                                 4 * self.rect.width, self.rect.height / 2)
                    # mois speshiaL
                case 12:
                    attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.5,
                                                 3 * self.rect.width, self.rect.height * 1.5)
                    # spau speshial
                case 13:
                    attacking_rect = pygame.Rect(self.rect.centerx - (hg_att * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.7,
                                                 hg_att * self.rect.width, self.rect.height * 2.7)
                # far attack
                case 14:
                    a = 100
                    if not self.flip:
                        a = -200
                    bullet_rect = pygame.Rect(self.rect.centerx + (a * display.scr_w),
                                              self.rect.top,
                                              100 * display.scr_w, 100 * display.scr_h)
                    bullet_data = [200, 0.6 * display.scr_w, (10, 10), [2, 2], self.flip]
                    create_rocket(bullet_rect, bullet_data, target, hit)
                # tagir dash
                case 15:
                    dash_rect = pygame.Rect(self.rect.centerx - (1 * self.rect.width * self.flip),
                                            self.rect.y + self.rect.height * 0.3,
                                            1 * self.rect.width, self.rect.height * 0.5)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 14
                    else:
                        self.dash_x = -14
                    create_dash(dash_rect, self.flip, target, self, hit)
                # hg for upd action 4
                case 17:
                    attacking_rect = pygame.Rect(self.rect.centerx - (hg_att * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 hg_att * self.rect.width, self.rect.height)
                case 18:
                    attacking_rect = pygame.Rect(self.rect.centerx - (hg_att * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.6,
                                                 hg_att * self.rect.width, self.rect.height * 0.4)
                # shield
                case 20:
                    self.shield_on = True
                    self.heal(hg_att)
                    attacking_rect = pygame.Rect(self.rect.centerx - (0.6 * self.rect.width * self.flip),
                                                 self.rect.y * 1.35,
                                                 0.6 * self.rect.width, self.rect.height)

                    shield_on_sfx.play()
                    hit = 15
                case 21:
                    attacking_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                                 self.rect.y * 1.35,
                                                 self.rect.width, self.rect.height)
                    hit = 15
                    if self.second_phase:
                        self.heal(12)
                    else:
                        self.heal(25)
                    # ranged
                # walker splash for upd action 3
                case 22:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.2 * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.6,
                                                 1.4 * self.rect.width, self.rect.height * 0.4)
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - (0.8 * self.rect.width * self.flip),
                                                   self.rect.y,
                                                   0.8 * self.rect.width, self.rect.height)
                # supertank laserbeam
                case 23:
                    choice(gaubica_sounds).play()
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y * 1.6,
                                              50 * display.scr_w, 50 * display.scr_h)
                    offset = 10
                    bullet_data = [20, 9.1 * display.scr_w, (offset, 10), [2, 2], self.flip]
                    create_beam(bullet_rect, bullet_data, target, hit)
                # supertank dash + far attack
                case 24:
                    screen_shake(40)
                    dash_rect = pygame.Rect(self.rect.centerx - (1.07 * self.rect.width * self.flip),
                                            self.rect.y,
                                            1.07 * self.rect.width, self.rect.height)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 6
                    else:
                        self.dash_x = -6
                    create_dash(dash_rect, self.flip, target, self, hit)
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y * 1.35,
                                              100 * display.scr_w, 100 * display.scr_h)
                    offset = 10
                    bullet_data = [200, 0.6 * display.scr_w, (offset, 10), [2, 2], self.flip]
                    create_rocket(bullet_rect, bullet_data, target, hit)

                case 28:
                    hit = 15
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height / 2,
                                                 2.5 * self.rect.width, self.rect.height * 1.6)
                    Attack2(self, attacking_rect, attacking_rect_2, target, hit, False, True)
                    hit = 20
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.6 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height / 2,
                                                 1.6 * self.rect.width, self.rect.height * 1.6)
                case 29:
                    attacking_rect = pygame.Rect(-1, -1, 1, 1)
                    self.heal(8)
                case 30:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.8 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.4,
                                                 1.8 * self.rect.width, self.rect.height * 1.4)
                case 3:
                    size = 25
                    bullet_data = [20, 4.55 * display.scr_w, (10, 6), [2, 2], self.flip]
                    if self.player in [7, 14, 22, 25]:
                        choice(gaubica_sounds).play()
                        size = 50
                        bullet_data = [20, 9.1 * display.scr_w, (10, 6), [2, 2], self.flip]
                    bullet_rect = pygame.Rect(self.rect.right - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.4,
                                              size * display.scr_w, size * display.scr_h)
                    create_bullet(bullet_rect, bullet_data, target, hit)
                case 25:
                    choice(gaubica_sounds).play()
                    bullet_rect = pygame.Rect(self.rect.centerx,
                                              self.rect.y * 1.8,
                                              50 * display.scr_w, 50 * display.scr_h)
                    offset = 10
                    bullet_data = [20, 9.1 * display.scr_w, (offset, 10), [2, 2], self.flip]
                    create_bullet(bullet_rect, bullet_data, target, hit)
                # energy
                case 26:
                    choice(gaubica_sounds).play()
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.35,
                                              100 * display.scr_w, 100 * display.scr_h)
                    offset = 10
                    bullet_data = [200, 0.8 * display.scr_w, (offset, 10), [2, 2], self.flip]
                    create_energy(bullet_rect, bullet_data, target, hit)
                # artestro splash for upd action 3
                case 16:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.8,
                                                 2.5 * self.rect.width, self.rect.height * 0.2)
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                                   self.rect.y,
                                                   self.rect.width, self.rect.height)
                # stone attack
                case 27:
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.35,
                                              100 * display.scr_w, 100 * display.scr_h)
                    offset = 10
                    bullet_data = [200, 0.6 * display.scr_w, (offset, 10), [2, 2], self.flip]
                    create_stone(bullet_rect, bullet_data, target, hit)
                case 19:
                    screen_shake(15)
                    pygame.mixer.Sound.play(choice(explosion_sounds))
                    explosion_rect1 = pygame.Rect(self.rect.centerx - (400 * display.scr_w),
                                                  display.screen_height - 710 * display.scr_h,
                                                  400 * display.scr_w, 600 * display.scr_h)
                    explosion_rect2 = pygame.Rect(self.rect.centerx,
                                                  display.screen_height - 710 * display.scr_h,
                                                  400 * display.scr_w, 600 * display.scr_h)
                    offset = 34
                    if self.flip:
                        offset = 40
                    explosion_data = [127, 7.7 * display.scr_w, (offset, 10), [5], self.flip]
                    create_explosion(explosion_rect1, explosion_data, target, hit)
                    create_explosion(explosion_rect2, explosion_data, target, hit)
                    # dash att 2
                case 31:
                    dash_rect = pygame.Rect(self.rect.x, self.rect.y,
                                            self.rect.width + 50 * display.scr_w,
                                            self.rect.height)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 40
                    else:
                        self.dash_x = -40
                    create_dash(dash_rect, self.flip, target, self, hit)
                    self.recharged -= 1
                    screen_shake(50)
                    pygame.mixer.Sound.play(choice(gaubica_sounds))
                case 32:
                    screen_shake(10)
                    Attack2(self, attacking_rect, attacking_rect_2, target, hit, False, True)
                case 33:
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y * 1.35,
                                              50 * display.scr_w, 50 * display.scr_h)
                    bullet_data = [150, 0.4 * display.scr_w, (10, 10), [4], self.flip]
                    create_grenade(bullet_rect, bullet_data, target, hit)
                case 34:
                    bullet_data = [200, 0.6 * display.scr_w, (10, 10), [2, 2], True]
                    bullet_data_2 = [200, 0.6 * display.scr_w, (10, 10), [2, 2], False]
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y * 1.35,
                                              100 * display.scr_w, 100 * display.scr_h)
                    create_rocket(bullet_rect, bullet_data, target, hit, 30)
                    create_rocket(bullet_rect, bullet_data_2, target, hit, 30)
                    create_rocket(bullet_rect, bullet_data, target, hit, 0)
                    pygame.mixer.Sound.play(gaubica_sounds[2])
                    self.recharged -= 1
                    screen_shake(3)
                case _:
                    attacking_rect = pygame.Rect(self.rect.centerx - (0 * self.rect.width * self.flip), self.rect.y * 0,
                                                 0 * self.rect.width, self.rect.height * 0)
            # pygame.draw.rect(display.screen, (255, 255, 0), attacking_rect)
            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect_2)
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, target, hit, False, True)

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update anim sattings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        self.draw_cooldown_stats(surface)
        if not self.invisibility:
            img = pygame.transform.flip(self.image, self.flip, False)
            # pygame.draw.rect(surface, (255, 0, 0), self.rect)
            surface.blit(img,
                         (self.rect.x - self.offset[0] * self.image_scale,
                          self.rect.y - self.offset[1] * self.image_scale))
        if self.player == 18:
            if self.alive and self.base_health == 200:
                if self.health < 100:
                    self.draw_fire(surface)

    def draw_fire(self, surface):
        img = pygame.transform.flip(self.fire_eff.get_image(), self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale,
                      self.rect.y - self.offset[1] * self.image_scale))

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
        if self.player in player_spec:
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
        if self.player in player_shield:
            pygame.draw.rect(surface, (255, 255, 255), (
                (1700 - 2) * display.scr_w, (60 - 2) * display.scr_h, (200 + 4) * display.scr_w,
                19 * display.scr_h))
            pygame.draw.rect(surface, (0, 102, 0), (
                1700 * display.scr_w, 60 * display.scr_h, 200 * display.scr_w,
                15 * display.scr_h))
            pygame.draw.rect(surface, (0, 51, 0), (
                1700 * display.scr_w, (60 + 10) * display.scr_h, 200 * display.scr_w,
                5 * display.scr_h))
            pygame.draw.rect(surface, (51, 153, 51), (
                1700 * display.scr_w, 60 * display.scr_h, 200 * display.scr_w,
                5 * display.scr_h))

            if self.shield_cooldown > 0:
                pygame.draw.rect(surface, (0, 0, 0),
                                 (1700 * display.scr_w, 60 * display.scr_h, self.shield_cooldown * display.scr_w,
                                  15 * display.scr_h))
            else:
                pygame.draw.rect(surface, (102, 255, 102), (
                    1700 * display.scr_w, 60 * display.scr_h, (200 - self.shield_cooldown) * display.scr_w,
                    15 * display.scr_h))
                pygame.draw.rect(surface, (102, 255, 153), (
                    1700 * display.scr_w, (60 + 7) * display.scr_h, (200 - self.shield_cooldown) * display.scr_w,
                    8 * display.scr_h))

    def heal(self, amount):
        if self.alive:
            if self.health + amount >= self.base_health:
                self.health = self.base_health
            else:
                self.health += amount

    def dash(self):
        if self.dashing:
            self.rect.x += self.dash_x * display.scr_w
            if self.player == 25:
                self.shield_on = True

    def stun(self):
        self.stunned = 50

    def take_damage(self, hit, block_break=False):
        if not self.shield_on:
            if not self.last_phase:
                self.health -= hit
                self.hit = True
                if self.stunned <= 0:
                    create_particles((self.rect.centerx, self.rect.top), self.flip, self.particle, self.particle_type)
                    choice(self.hurt_sfx).play()
                    create_damage_number((1750 * display.scr_w, 150 * display.scr_h),
                                         self.flip, hit)
            else:
                if self.stunned <= 0:
                    create_particles((self.rect.centerx, self.rect.top), self.flip, self.particle, self.particle_type)
        else:
            self.shield_on = False
            shield_sfx.play()
            create_particles((self.rect.centerx, self.rect.top), self.flip, shield_parts, 4)
