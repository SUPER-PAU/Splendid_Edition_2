from random import choice

from constants.audio.effects import human_sound
from constants.textures.sprites import attack_group
from lib.display import display
from lib.players_data.particles_online import create_tank_bullet, create_damage_number
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer
import pygame


class Kingartema(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(3, x, y, flip, data, attack_frame)
        self.sex = 1
        self.name = "kingartema"
        self.is_tank = True

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
            if (key[pygame.K_r] or key[pygame.K_t] or mouse_right or mouse_left or key[pygame.K_f]
               or mouse_middle) and (mouse_click or key_press):
                if self.attack_cooldown <= 0:
                    # determine attack
                    if key[pygame.K_r] or mouse_left:
                        self.attack_type = 1
                        self.attack(target, attack_group)
                    elif key[pygame.K_f] or mouse_middle:
                        if self.shield_cooldown <= 0 and self.attack_cooldown <= 0 and not self.hit:
                            self.attack_type = 3
                            self.shield_cooldown = 200
                            self.attack(target, attack_group)
                    elif key[pygame.K_t] or mouse_right and self.shield_cooldown <= 0:
                        self.attack_type = 2
                        self.shield_cooldown = 200
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
            self.dashing = False
        elif self.blocking:
            self.update_action(4)  # block
            self.dashing = False
        elif self.attacking:
            match self.attack_type:
                case 1:
                    self.update_action(6)  # attack1
                case 2:
                    self.update_action(7)  # attack 2
                case 3:
                    self.update_action(8)  # attack 2
        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

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
                    hit = 15
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                                 self.rect.y + self.rect.height * 0.8,
                                                 2.5 * self.rect.width, self.rect.height * 0.2)
                    attacking_rect_2 = pygame.Rect(self.rect.centerx - (self.rect.width * self.flip),
                                                   self.rect.y,
                                                   self.rect.width, self.rect.height)
                case 2:
                    size = 50
                    bullet_data = [20, 9.1, (10, 6), [2, 2], self.flip]
                    bullet_rect = pygame.Rect(self.rect.right * 0.9 - (self.rect.width * 0.2 * self.flip),
                                              self.rect.y + self.rect.height * 0.4,
                                              size, size)
                    hit = 20
                    create_tank_bullet(bullet_rect, bullet_data, target, hit)
                case 3:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 2.5 * self.rect.width, self.rect.height)
                    hit = 5

            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect)
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, self.attack_type, target, hit, group, block_break)

    def take_damage(self, hit, block_break=False, sender=2):
        if not (hit == self.prev_hit and self.hit) and self.hit_timer <= 0:
            hit = round(hit * 0.5)
            choice(human_sound).play()
            if sender == 2:
                self.hit_timer = 6
                self.prev_hit = hit
                self.health -= hit
                self.hit = True
                self.update_huge_attack_cd(60)
                if self.side == 1:
                    create_damage_number((50, 150),
                                         self.flip, hit)
                else:
                    create_damage_number((1750, 150),
                                         self.flip, hit)


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, rect, rect2, attack_type, target, damage, sprite_group, block_break=False):
        super().__init__(sprite_group)
        match attack_type:
            case 1:  # attack1
                self.attack_frame = player.attack_frame[0]
            case 2:  # attack 2
                self.attack_frame = player.attack_frame[1]
            # 3rd attack
            case 3:
                self.attack_frame = player.attack_frame[2]
            case 4:
                self.attack_frame = player.attack_frame[3]
            case 5:
                self.attack_frame = player.attack_frame[4]
        self.attack_type = attack_type
        self.block_break = block_break
        self.rect, self.rect2 = rect, rect2
        self.player = player
        self.target = target
        self.damage = damage
        self.hit = False

    def update(self, target, player, sender=1):
        if player.attacking and not player.hit:
            if self.hit and (target.hit or target.blocking):
                self.kill()
            else:
                if sender == 1 and self.hit:
                    pass
                else:
                    if self.attack_frame == player.frame_index or self.attack_frame + 1 == player.frame_index:
                        attacking_rect = pygame.Rect(
                            player.rect.centerx - (self.rect.width * player.flip),
                            self.rect.y,
                            self.rect.width, self.rect.height)
                        # pygame.draw.rect(display.screen, (255, 255, 0), attacking_rect)

                        if attacking_rect.colliderect(target.rect) or self.rect2.colliderect(target.rect):
                            if self.attack_type == 4:
                                if not target.is_tank:
                                    if not target.jump or not target.attacking:
                                        player.update_huge_attack_cd(50)
                                        player.grabing = True
                                        target.in_grab = True
                                else:
                                    self.damage = 0
                                    self.block_break = False
                            else:
                                if self.block_break or target.jump or target.sprint or target.attacking:
                                    player.update_huge_attack_cd(50)
                                else:
                                    player.update_huge_attack_cd(30)

                            target.take_damage(self.damage, self.block_break, sender)
                            if self.attack_type == 3:
                                target.set_on_fire()
                            self.hit = True
        else:
            self.kill()
