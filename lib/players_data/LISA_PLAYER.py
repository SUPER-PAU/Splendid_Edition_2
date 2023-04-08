from lib.display import display
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame


class LisaPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(1, x, y, flip, data, attack_frame)
        self.sex = 2
        self.name = "lisa"

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
                    self.update_action(9)
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
                if self.action in [6, 7, 8, 9, 10]:
                    self.attacking = False
                    self.grabing = False
                    self.attack_cooldown = 10
                    self.dashing = False
                    if self.action == 7:
                        self.rect.x -= (200 - 400 * self.flip) * display.scr_w
                if self.action == 11:
                    self.hit = False
                    self.in_grab = False
                    # if player was in the middle of an attack, then attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 10
                    self.dashing = False
                # check if damage was taken
                if self.action == 4:
                    self.hit = False
                    # if player was in the middle of an attack, then attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 10
                    self.dashing = False
                # check block
                if self.action == 3:
                    self.blocking = False
                    self.attack_cooldown = 10
                    self.hit = False

        if self.alive:
            if self.action == 11:
                if self.frame_index in [3, 4]:
                    self.rect.x -= (23 - 46 * self.flip) * display.scr_w
            if self.action in [6, 7, 8, 10, 9]:
                self.attack_cooldown = 15
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
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.3 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 1.3 * self.rect.width, self.rect.height)
                    hit = 18
                    # att 2
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                                 2 * self.rect.width, self.rect.height)
                    hit = 12
                # speshal
                case 3:
                    block_break = True
                    hit = 15
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height / 2,
                                                 2.5 * self.rect.width, self.rect.height * 1.6)
                    Attack(self, attacking_rect, attacking_rect_2, 5, target, hit, group, block_break)
                    hit = 20
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.6 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height / 2,
                                                 1.6 * self.rect.width, self.rect.height * 1.6)
                    # grab
                case 4:
                    block_break = True
                    hit = 15
                    attacking_rect = pygame.Rect(self.rect.centerx - (0.7 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 0.7 * self.rect.width, self.rect.height)
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, self.attack_type, target, hit, group, block_break)

