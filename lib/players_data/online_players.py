import lib.players as p
import constants.textures.player_card_sprites as c
import constants.textures.sprites as sheet
from lib.display import display
from lib.players_data.VESISA_PLAYER import VesisaPlayer
from lib.players_data.TAGIR_PLAYER import TagirPlayer
from lib.players_data.ARTESTRO import ArtestroPlayer
from lib.players_data.AKSENOV import AksenovPlayer


class OnlinePlayer:
    def __init__(self, player, img, name, animation_list):
        self.player = player
        self.img = img
        self.name = name
        self.animation_list = animation_list
        action, frame_index = self.player.get_animation_params()
        self.image = self.animation_list[action][frame_index]

    def get_p(self):
        return self.player

    def get_name(self):
        return self.name

    def card_img(self):
        return self.img

    def reset_params(self):
        self.player.reset_params()

    def get_animation_list(self):
        return self.animation_list

    def update(self):
        self.player.update(self.animation_list)
        action, frame_index = self.player.get_animation_params()
        self.image = self.animation_list[action][frame_index]

    def draw_p(self):
        self.update()
        self.player.draw(display.screen, self.image)

    def draw_menu(self, coords):
        self.draw_p()
        self.player.flip = False
        self.player.rect.x, self.player.rect.y = coords[0], coords[1]


AKSENOV_SIZE = 486
AKSENOV_SCALE = 3 * display.scr_h
AKSENOV_OFFSET = [216, 168]
AKSENOV_DATA = [AKSENOV_SIZE, AKSENOV_SCALE, AKSENOV_OFFSET, (200 * display.scr_w, 400 * display.scr_h)]
LISA_SIZE = 486
LISA_SCALE = 3 * display.scr_h
LISA_OFFSET = [216, 168]
KINGARTEMA_DATA = [LISA_SIZE, LISA_SCALE, [216, 155], (200 * display.scr_w, 450 * display.scr_h)]
LISA_DATA = [LISA_SIZE, LISA_SCALE, LISA_OFFSET, (200 * display.scr_w, 400 * display.scr_h)]
GENERAL_DATA = [486, LISA_SCALE, [180, 110], (400 * display.scr_w, 600 * display.scr_h)]
EGOR_DATA = [486, 1.5 * display.scr_h, [216, 168], (100 * display.scr_w, 200 * display.scr_h)]

ARTESTRO_p = ArtestroPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 1, 3, 2])
ARTESTRO_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 5, 3, 5, 6]
ARTESTRO_ANIMATION_LIST = ARTESTRO_p.load_images(sheet.artestro_2, ARTESTRO_2_ANIMATION_STEPS)

AKSENOV_p = AksenovPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 2, 1, 2])
AKSENOV_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 1, 3, 5, 6]
AKSENOV_ANIMATION_LIST = AKSENOV_p.load_images(sheet.aksenov_2, AKSENOV_2_ANIMATION_STEPS)

VESISA_p = VesisaPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 2, 0, 2])
VESISA_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 1, 3, 5, 6]
VESISA_ANIMATION_LIST = VESISA_p.load_images(sheet.vesisa_2, VESISA_2_ANIMATION_STEPS)

TAGIR_P = TagirPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [1, 2, 0, 2])
TAGIR_2_ANIMATION_STEPS = [8, 4, 1, 3, 3, 6, 6, 4, 1, 3, 5, 6]
TAGIR_ANIMATION_LIST = TAGIR_P.load_images(sheet.tagir_2, TAGIR_2_ANIMATION_STEPS)

super_pau = OnlinePlayer(p.super_pau_online, c.pau, "pau", p.PAU_ANIMATION_LIST)
lisa = OnlinePlayer(p.lisa_online, c.lisa, "lisa", p.LISA_ANIMATION_LIST)
vesisa = OnlinePlayer(VESISA_p, c.vesisa, "vesisa", VESISA_ANIMATION_LIST)
tagir = OnlinePlayer(TAGIR_P, c.tagir, "tagir", TAGIR_ANIMATION_LIST)
artestro = OnlinePlayer(ARTESTRO_p, c.artestro, ARTESTRO_p.name, ARTESTRO_ANIMATION_LIST)
aksenov = OnlinePlayer(AKSENOV_p, c.aksenov, AKSENOV_p.name, AKSENOV_ANIMATION_LIST)


animation_list_by_name = {
    "pau": p.PAU_ANIMATION_LIST,
    "lisa": p.LISA_ANIMATION_LIST,
    "vesisa": VESISA_ANIMATION_LIST,
    "tagir": TAGIR_ANIMATION_LIST,
    "artestro": ARTESTRO_ANIMATION_LIST,
    "aksenov": AKSENOV_ANIMATION_LIST
}

