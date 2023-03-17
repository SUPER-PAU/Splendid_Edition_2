from random import choice

import pygame
from lib.display import display
from lib.particle import create_particles, create_bullet, create_dash, create_rocket, create_stone, \
    create_damage_number, create_beam, create_explosion
from constants.audio.effects import shield_sfx, explosion_sounds
from constants.textures.sprites import shield_parts
from lib.attack import Attack

player_spec = [1, 9, 12]
player_attack3 = [1, 9]
player_shield = [9]


class FighterPLAYER:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, hurt_fx, particle_sprite, attack_frame):
        self.data = data
        self.player, self.size, self.image_scale, self.offset = player, data[0], data[1], data[2]
        self.attack_frame = attack_frame
        self.start_pos = x, y, flip
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.rect = pygame.Rect((x, y, data[3][0], data[3][1]))
        self.action = 0  # 0 - idle, 1 - run, 2 - jump, 3 - attack1, 4 - attack2, 5 -hit, 6 - death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.running = False
        self.dashing = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.same_attack_count = 0
        self.temp_attack = 100
        self.huge_attack_cooldown = 300
        self.shield_cooldown = 200
        self.health = 100
        self.dash_x = 0
        self.stunned = 0
        self.hurt_sfx, self.particle = hurt_fx, particle_sprite
        self.hit = False
        self.shield_on = False
        self.alive = True

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
        self.running = False
        self.jump = False
        self.attacking = False
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

    def move(self, surface, target, round_over):
        SPEED = 9 * display.scr_w
        GRAVITY = 2 * display.scr_h
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        # key presses
        key = pygame.key.get_pressed()
        hit = 10
        mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
        if key[pygame.K_LSHIFT] and not self.jump:
            SPEED += 4.3 * display.scr_w
        # if player is stunned by beam
        if self.stunned > 0:
            self.stunned -= 1
            self.take_damage(0.2)
            self.vel_y = 0
        # heal player aboba os ability sprint
        self.heal(0.017)
        # can only perform other actions if not attacking
        if not self.attacking and self.alive and not round_over:

            match self.player:
                # bt25t final
                case 12:
                    SPEED += 3 * display.scr_w
                    self.shield_on = False
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f] \
                            or mouse_middle:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 9
                            hit = 10
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 3
                            hit = 18
                        elif key[pygame.K_f] or mouse_middle:
                            if self.huge_attack_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                                self.attack_type = 7
                                hit = 15
                                self.huge_attack_cooldown = 300
                        self.attack(surface, target, 1.09, hit)
                # trio
                case 11:
                    SPEED += 2 * display.scr_w
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -50 * display.scr_h
                        self.jump = True
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 17
                            hit = 12
                            self.attack(surface, target, 2.9, hit)
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 16
                            hit = 20
                            self.attack(surface, target, 2.4, hit)
                # walker
                case 10:
                    SPEED -= 5 * display.scr_w
                    # атаковать ли
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 22
                            hit = 25
                            self.attack(surface, target, 1.5, hit)
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 14
                            hit = 35
                            self.shield_cooldown = 200
                            self.attack(surface, target, 1.5, hit)

                # bulat
                case 9:
                    SPEED -= 1 * display.scr_w
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -46 * display.scr_h
                        self.jump = True
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f] \
                            or mouse_middle:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 1
                            hit = 18
                            self.attack(surface, target, 1.5, hit)
                        elif key[pygame.K_f] or mouse_middle:
                            if self.huge_attack_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                                self.attack_type = 18
                                hit = 25
                                self.huge_attack_cooldown = 300
                                self.attack(surface, target, 2.6, hit)
                        elif key[pygame.K_t] or mouse_right:
                            if self.shield_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                                self.attack_type = 16
                                self.heal(10)
                                self.shield_cooldown = 200
                                self.attack(surface, target, 1, hit)
                # vesisa
                case 8:
                    SPEED += 2 * display.scr_w
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -50 * display.scr_h
                        self.jump = True
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 17
                            hit = 12
                            self.attack(surface, target, 2.9, hit)
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 16
                            hit = 18
                            self.attack(surface, target, 2.4, hit)

                # kingartema
                case 7:
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -46 * display.scr_h
                        self.jump = True
                        # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 1
                            hit = 17
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 3
                            hit = 12
                        self.attack(surface, target, 2.5, hit)
                # egor
                case 6:
                    # movement
                    SPEED += 4 * display.scr_w
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -52 * display.scr_h
                        self.jump = True
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 5
                            hit = 22
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 2
                            hit = 17
                        self.attack(surface, target, 1.3, hit)
                # tagir
                case 5:
                    SPEED += 1 * display.scr_w
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -50 * display.scr_h
                        self.jump = True
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 15
                            hit = 18
                            self.attack(surface, target, 1.09, hit)
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 27
                            hit = 21
                            self.attack(surface, target, 1.09, hit)

                # bt25t
                case 4:
                    SPEED += 3 * display.scr_w
                    self.shield_on = False
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 9
                            hit = 10
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 3
                            hit = 18
                        self.attack(surface, target, 1.09, hit)

                # check aks controls
                case 3:
                    SPEED += 1
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -45 * display.scr_h
                        self.jump = True
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 1
                            hit = 18
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 3
                            hit = 14
                        self.attack(surface, target, 1.09, hit)

                # check player 1 controls lisa
                case 2:
                    # movement
                    SPEED += 3 * display.scr_w
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -52 * display.scr_h
                        self.jump = True
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 1
                            hit = 18
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 2
                            hit = 12
                        self.attack(surface, target, 1.3, hit)

                # super pau player
                case 1:
                    # movement
                    SPEED += 3 * display.scr_w
                    # jump
                    if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.jump is False:
                        self.vel_y = -46 * display.scr_h
                        self.jump = True
                    # attack
                    if key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f] \
                            or mouse_middle:
                        # determine attack
                        if key[pygame.K_r] or mouse_left:
                            self.attack_type = 8
                            hit = 12
                            self.attack(surface, target, 1.3, hit)
                        elif key[pygame.K_f] or mouse_middle:
                            if self.huge_attack_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                                self.attack_type = 13
                                hit = 35
                                self.huge_attack_cooldown = 300
                                self.attack(surface, target, 1.3, hit)
                        elif key[pygame.K_t] or mouse_right:
                            self.attack_type = 4
                            hit = 14
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

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.huge_attack_cooldown > 0:
            self.huge_attack_cooldown -= 1
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

        if self.player in player_attack3 and self.action == 7 and self.hit:
            self.huge_attack_cooldown = 300
        elif self.player in player_spec and self.action == 3 and self.hit and \
                self.player not in player_attack3:
            self.huge_attack_cooldown = 300
        if not self.hit and not self.attacking:
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

    # handle animation updates
    def update(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.hit = False
            self.attacking = False
            self.update_action(6)  # death
        elif self.hit:
            self.update_action(5)  # hit
        elif self.attacking:
            match self.attack_type:
                case 1 | 4 | 5 | 9 | 10 | 15 | 17 | 22:  # attack1
                    self.update_action(3)
                case 20 | 11 | 8 | 2 | 6 | 3 | 14 | 16 | 27 | 7:  # attack 2
                    self.update_action(4)
                # 3rd attack
                case 12 | 13 | 21 | 18:
                    self.update_action(7)

        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

        if self.player != 10:
            animation_cooldown = 63
        else:
            animation_cooldown = 83
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
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if attack is executed
                if self.action == 3 or self.action == 4 or self.action == 7:
                    self.attacking = False
                    self.attack_cooldown = 55
                    self.dashing = False
                # check if damage was taken

                if self.action == 5:
                    self.hit = False
                    # if player was in the middle of an attack, then attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 40
                    self.dashing = False
        if self.alive:
            if self.action == 3 or self.action == 4 or self.action == 7:
                self.attack_cooldown = 55
                self.dash()

    def attack(self, surface, target, hg_att, hit):
        if self.attack_cooldown == 0 and not self.hit:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None

            # att 1
            match self.attack_type:

                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (hg_att * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 hg_att * self.rect.width, self.rect.height)
                # att 2
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                                 2 * self.rect.width, self.rect.height)
                # att 1
                case 4:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip), self.rect.y,
                                                 2.5 * self.rect.width, self.rect.height)
                # att 1 megasword
                case 5:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.2 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.4,
                                                 1.2 * self.rect.width, self.rect.height * 1.4)
                # att 2  artestro splash
                case 6:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.7 * self.rect.width * self.flip),
                                                 self.rect.y / 1.2,
                                                 2.7 * self.rect.width, self.rect.height * 1.2)
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                                   self.rect.y - self.rect.height * 0.5,
                                                   2 * self.rect.width, self.rect.height * 1.5)
                # laser_beam
                case 7:
                    bullet_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.4,
                                              50 * display.scr_w, 50 * display.scr_h)
                    offset = 10
                    bullet_data = [20, 9.1 * display.scr_w, (offset, 10), [2, 2], self.flip]
                    create_beam(bullet_rect, bullet_data, target, hit)
                # superpau web
                case 8:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.8 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.4,
                                                 2.8 * self.rect.width, self.rect.height * 1.4)
                # spau speshal
                case 13:
                    attacking_rect = pygame.Rect(self.rect.centerx - (3.7 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.7,
                                                 3.7 * self.rect.width, self.rect.height * 1.7)
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
                #  dash bt
                case 9:
                    dash_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                            self.rect.y + self.rect.height * 0.2,
                                            2.5 * self.rect.width, self.rect.height)
                    self.dashing = True
                    if not self.flip:
                        self.dash_x = 6
                    else:
                        self.dash_x = -6
                    create_dash(dash_rect, self.flip, target, self, hit)
                # dash tagir
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
                case 16:
                    attacking_rect = pygame.Rect(self.rect.centerx - (hg_att * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 hg_att * self.rect.width, self.rect.height)
                # vesisa upd action 3
                case 17:
                    attacking_rect = pygame.Rect(self.rect.centerx - (hg_att * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height,
                                                 hg_att * self.rect.width, self.rect.height * 2)
                # upd action 7
                case 18:
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
                # walker splash for upd action 3
                case 22:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.4 * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.6,
                                                 1.4 * self.rect.width, self.rect.height * 0.4)
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - (0.8 * self.rect.width * self.flip),
                                                   self.rect.y,
                                                   0.8 * self.rect.width, self.rect.height)
                # stone attack
                case 27:
                    bullet_rect = pygame.Rect(self.rect.right - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.35,
                                              100 * display.scr_w, 100 * display.scr_h)
                    offset = 10
                    bullet_data = [200, 0.6 * display.scr_w, (offset, 10), [2, 2], self.flip]
                    create_stone(bullet_rect, bullet_data, target, hit)
                case 3:
                    size = 25
                    bullet_data = [20, 4.55 * display.scr_w, (10, 6), [2, 2], self.flip]
                    if self.player in [4, 12, 7]:
                        size = 50
                        bullet_data = [20, 9.1 * display.scr_w, (10, 6), [2, 2], self.flip]
                    bullet_rect = pygame.Rect(self.rect.right - (self.rect.width * self.flip),
                                              self.rect.y + self.rect.height * 0.4,
                                              size * display.scr_w, size * display.scr_h)
                    create_bullet(bullet_rect, bullet_data, target, hit)

            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect)

            if self.attack_type == self.temp_attack:
                self.same_attack_count += 1
            else:
                self.same_attack_count = 0
            self.temp_attack = self.attack_type
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, target, hit)
            # punish player for spamming same attacks)))) heheheha!
            if self.same_attack_count == 3 and target.player != 10:
                target.hit = False
                target.attack_cooldown = 8
                self.same_attack_count = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update anim settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
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

    def dash(self):
        if self.dashing:
            self.rect.x += self.dash_x * display.scr_w
            if self.player == 4:
                self.shield_on = True

    def stun(self):
        self.stunned = 45

    def take_damage(self, hit):
        if not self.shield_on:
            self.health -= hit
            self.hit = True
            if not self.stunned:
                create_damage_number((50 * display.scr_w, 150 * display.scr_h),
                                     self.flip, hit)
                create_particles((self.rect.centerx, self.rect.top), self.flip, self.particle)
                choice(self.hurt_sfx).play()
        else:
            self.shield_on = False
            shield_sfx.play()
            create_particles((self.rect.centerx, self.rect.top), self.flip, shield_parts)
