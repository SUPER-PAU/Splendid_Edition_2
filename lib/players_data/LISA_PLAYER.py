from lib.display import display
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer
from constants.textures.sprites import lisa_2, bullet_sprites
import pygame


class LisaPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, animation_steps, hurt_fx, particle_sprite, attack_frame):
        super().__init__(1, x, y, flip, data, lisa_2, animation_steps, hurt_fx, particle_sprite, attack_frame)

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
                    if self.frame_index in [2, 3, 7, 8]:
                        self.rect.x += 23 - 46 * self.flip
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
        else:
            self.kill()

