import pygame
from constants.textures.sprites import bullet_sprites
from lib.player_fighter import FighterPLAYER


class Attack(pygame.sprite.Sprite):
    def __init__(self, player, rect, rect2, target, damage, block_break=False):
        super().__init__(bullet_sprites)
        if isinstance(player, FighterPLAYER):
            match player.attack_type:
                case 1 | 4 | 5 | 9 | 10 | 15 | 17 | 22:  # attack1
                    self.attack_frame = player.attack_frame[0]
                case 20 | 11 | 8 | 2 | 6 | 3 | 14 | 16 | 27 | 7:  # attack 2
                    self.attack_frame = player.attack_frame[1]
                # 3rd attack
                case 12 | 13 | 21 | 18:
                    self.attack_frame = player.attack_frame[2]
        else:
            match player.attack_type:
                case 1 | 4 | 5 | 7 | 9 | 10 | 15 | 16 | 18 | 22 | 25:  # attack1
                    self.attack_frame = player.attack_frame[0]
                # attack 2
                case 20 | 11 | 8 | 2 | 6 | 3 | 14 | 17 | 21 | 23 | 26 | 27:
                    self.attack_frame = player.attack_frame[1]
                # 3rd attack
                case 12 | 13 | 24 | 19:
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
