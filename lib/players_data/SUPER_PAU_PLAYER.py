import pygame

from lib.player_fighter import FighterPLAYER
from random import choice

from lib.display import display
from lib.particle import create_particles, create_damage_number
from constants.audio.effects import shield_sfx
from constants.textures.sprites import shield_parts, bullet_sprites


class SuperPauPlayer(FighterPLAYER):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, hurt_fx, particle_sprite, attack_frame):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, hurt_fx, particle_sprite, attack_frame)
        self.sprint = False

    def move(self, surface, target, round_over):
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
        # heal player aboba os ability sprint
        self.heal(0.017)
        # can only perform other actions if not attacking
        if not self.attacking and self.alive and not round_over and not self.blocking:
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
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.huge_attack_cooldown > 0:
            self.huge_attack_cooldown -= 1
        if self.shield_cooldown > 0:
            self.shield_cooldown -= 1

    def update(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.hit = False
            self.attacking = False
            self.update_action(5)  # death
        elif self.hit:
            self.update_action(4)  # hit
            self.rect.x -= 8 - 16 * self.flip
        elif self.blocking:
            self.update_action(3)  # block
            self.rect.x -= 4 - 8 * self.flip
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
        animation_cooldown = 63
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
                self.blocking = False
                self.frame_index = len(self.animation_list[self.action]) - 1
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
                # att 1
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip), self.rect.y,
                                                 2.5 * self.rect.width, self.rect.height)
                # superpau web
                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.8 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.4,
                                                 2.8 * self.rect.width, self.rect.height * 1.4)
                # spau speshal
                case 3:
                    attacking_rect = pygame.Rect(self.rect.centerx - (3.7 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height * 0.7,
                                                 3.7 * self.rect.width, self.rect.height * 1.7)
                    block_break = True
            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect)

            if self.attack_type == self.temp_attack:
                self.same_attack_count += 1
            else:
                self.same_attack_count = 0
            self.temp_attack = self.attack_type
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, target, hit, block_break)
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
                if not self.stunned:
                    create_damage_number((50 * display.scr_w, 150 * display.scr_h),
                                         self.flip, hit)
                    create_particles((self.rect.centerx, self.rect.top), self.flip, self.particle)
                    choice(self.hurt_sfx).play()
            else:
                hit = round(hit * 0.2)
                self.health -= hit
                self.blocking = True
                create_damage_number((50 * display.scr_w, 150 * display.scr_h),
                                     self.flip, hit)
        else:
            self.shield_on = False
            shield_sfx.play()
            create_particles((self.rect.centerx, self.rect.top), self.flip, shield_parts)


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, rect, rect2, target, damage, block_break=False):
        super().__init__(bullet_sprites)
        match player.attack_type:
            case 1:  # attack1
                self.attack_frame = player.attack_frame[0]
            case 2:  # attack 2
                self.attack_frame = player.attack_frame[1]
            # 3rd attack
            case 3:
                self.attack_frame = player.attack_frame[2]
        self.block_break = block_break
        self.rect, self.rect2 = rect, rect2
        self.player = player
        self.target = target
        self.damage = damage
        self.hit = False

    def update(self):
        if self.player.attacking and not self.hit and not self.player.hit:
            if self.attack_frame == self.player.frame_index:
                if self.rect.colliderect(self.target.rect) or self.rect2.colliderect(self.target.rect):
                    self.target.take_damage(self.damage, self.block_break)
                    self.hit = True
        else:
            self.kill()