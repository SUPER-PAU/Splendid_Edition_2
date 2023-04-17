from lib.players_data.particles_online import create_bag
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame


class EgorPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(1, x, y, flip, data, attack_frame)
        self.sex = 1
        self.name = "egor"
        self.is_tank = True

    def set_side(self, player):
        self.side = player
        if player == 1:
            self.start_pos = 450, 740, False
        else:
            self.start_pos = 1450, 740, True
        self.reset_pos()

    def attack(self, target, group):
        if not self.hit:
            self.attacking = True
            attacking_rect_2 = pygame.Rect(0, 0, 0, 0)
            attacking_rect = None
            block_break = True
            hit = 0
            # att 1
            match self.attack_type:
                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.y,
                                                 self.rect.width, self.rect.height)
                    hit = 18
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                                 2 * self.rect.width, self.rect.height * 2)
                    hit = 23
                case 3:
                    size = 50
                    bullet_data = [200, 0.6, (10, 10), [2, 2], True]
                    bullet_data_2 = [200, 0.6, (10, 10), [2, 2], False]
                    bullet_rect = pygame.Rect(self.rect.centerx,
                                              self.rect.y + self.rect.height * 0.4,
                                              size, size)
                    hit = 30
                    create_bag(bullet_rect, bullet_data, target, hit, 30)
                    create_bag(bullet_rect, bullet_data_2, target, hit, 30)
                    create_bag(bullet_rect, bullet_data, target, hit, 0)
            # pygame.draw.rect(surface, (255, 255, 0), attacking_rect)
            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, self.attack_type, target, hit, group, block_break)

