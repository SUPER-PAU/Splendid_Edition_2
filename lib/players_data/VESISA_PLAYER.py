from constants.audio.effects import shield_sfx
from constants.textures.sprites import dust
from lib.display import display
from lib.particle import create_particles
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer, Attack
import pygame


class VesisaPlayer(SuperPauPlayer):
    def __init__(self, x, y, flip, data, attack_frame):
        super().__init__(1, x, y, flip, data, attack_frame)
        self.sex = 2
        self.name = "vesisa"
        self.invisible = False

    def check_action(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.hit = False
            self.invisible = False
            self.attacking = False
            self.update_action(5)  # death
        elif self.grabing:
            self.update_action(10)
            self.attacking = True
        elif self.in_grab:
            self.update_action(11)
            self.hit = True
            self.invisible = False
        elif self.hit:
            self.update_action(4)  # hit
            self.invisible = False
            self.rect.x -= (8 - 16 * self.flip) * display.scr_w
        elif self.blocking:
            self.invisible = False
            self.update_action(3)  # block
            self.rect.x -= (4 - 8 * self.flip) * display.scr_w
        elif self.attacking:
            match self.attack_type:
                case 1:
                    self.update_action(6)  # attack1
                case 2:
                    self.update_action(7)  # attack 2
                case 3:
                    self.update_action(0)  # idle
                case 4:
                    self.update_action(9)  # grab
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
                # hg for upd action 4
                case 1:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.9 * self.rect.width * self.flip),
                                                 self.rect.y - self.rect.height,
                                                 2.9 * self.rect.width, self.rect.height * 2)
                    hit = 10
                # vesisa upd action 3
                case 2:
                    attacking_rect = pygame.Rect(self.rect.centerx - (2.4 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 2.4 * self.rect.width, self.rect.height)
                    hit = 14
                # speshal
                case 3:
                    attacking_rect = pygame.Rect(0, 0, 0, 0)
                    shield_sfx.play()
                    create_particles((self.rect.centerx, self.rect.top), self.flip, dust)
                    self.invisible = True
                    self.attacking = False
                    # grab
                case 4:
                    block_break = True
                    hit = 15

                    attacking_rect = pygame.Rect(self.rect.centerx - (0.7 * self.rect.width * self.flip),
                                                 self.rect.y,
                                                 0.7 * self.rect.width, self.rect.height)
            if self.invisible:
                self.hit *= 2
                block_break = True

            # take damage
            if attacking_rect:
                Attack(self, attacking_rect, attacking_rect_2, self.attack_type, target, hit, group, block_break)

    def draw(self, surface, img):
        if not self.invisible:
            img = pygame.transform.flip(img, self.flip, False)
            # pygame.draw.rect(surface, (255, 0, 0), self.rect)
            surface.blit(img,
                         (self.rect.x - self.offset[0] * self.image_scale,
                          self.rect.y - self.offset[1] * self.image_scale))
