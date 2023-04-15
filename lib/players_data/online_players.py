import constants.textures.player_card_sprites as c
import constants.textures.sprites as sheet
from lib.display import display
from lib.players_data.LISA_PLAYER import LisaPlayer
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer
from lib.players_data.VESISA_PLAYER import VesisaPlayer
from lib.players_data.TAGIR_PLAYER import TagirPlayer
from lib.players_data.ARTESTRO import ArtestroPlayer
from lib.players_data.AKSENOV import AksenovPlayer
from lib.players_data.BULAT import BulatPlayer
from lib.players_data.ROBOT_WOMAN import RobotFemalePlayer
from lib.players_data.BT25T import Bt25T


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
        if self.player.hit_timer > 0:
            self.player.hit_timer -= 1
        if self.player.stunned > 0:
            self.player.stunned -= 1
            self.player.hit = True
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


super_pau = None
lisa = None
vesisa = None
tagir = None
artestro = None
aksenov = None
bulat = None
robot_woman = None
bt25t = None
animation_list_by_name = {}


def load_chara_online():
    global super_pau, lisa, vesisa, tagir, aksenov, artestro, animation_list_by_name, bulat, robot_woman, bt25t
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

    LISA_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 10, 3, 5, 6]
    SUPER_PAU_PLAYER_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 6, 7, 8, 3, 5, 6]
    super_pau_online = SuperPauPlayer(1, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 3, 6, 2, 8])
    lisa_online = LisaPlayer(1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, [2, 1, 3, 2, 8])
    PAU_ANIMATION_LIST = super_pau_online.load_images(sheet.super_pau_2, SUPER_PAU_PLAYER_2_ANIMATION_STEPS)
    LISA_ANIMATION_LIST = lisa_online.load_images(sheet.lisa_2, LISA_2_ANIMATION_STEPS)

    ARTESTRO_p = ArtestroPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 1, 3, 2])
    ARTESTRO_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 5, 3, 5, 6]
    ARTESTRO_ANIMATION_LIST = ARTESTRO_p.load_images(sheet.artestro_2, ARTESTRO_2_ANIMATION_STEPS)

    AKSENOV_p = AksenovPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 2, 1, 2])
    AKSENOV_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 1, 3, 5, 6]
    AKSENOV_ANIMATION_LIST = AKSENOV_p.load_images(sheet.aksenov_2, AKSENOV_2_ANIMATION_STEPS)

    BULAT_p = BulatPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 2, 2, 2])
    BULAT_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 8, 7, 7, 3, 5, 6]
    BULAT_2_ANIMATION_LIST = BULAT_p.load_images(sheet.bulat_2, BULAT_2_ANIMATION_STEPS)

    VESISA_p = VesisaPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 2, 0, 2])
    VESISA_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 1, 3, 5, 6]
    VESISA_ANIMATION_LIST = VESISA_p.load_images(sheet.vesisa_2, VESISA_2_ANIMATION_STEPS)

    ROBOT_FEM_p = RobotFemalePlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [3, 3, 8, 2])
    ROBOT_WOMAN_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 10, 3, 5, 6]
    ROBOT_WOMAN_ANIMATION_LIST = ROBOT_FEM_p.load_images(sheet.robot_woman_2, ROBOT_WOMAN_2_ANIMATION_STEPS)

    TAGIR_P = TagirPlayer(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [1, 2, 0, 2])
    TAGIR_2_ANIMATION_STEPS = [8, 4, 1, 3, 3, 6, 6, 4, 1, 3, 5, 6]
    TAGIR_ANIMATION_LIST = TAGIR_P.load_images(sheet.tagir_2, TAGIR_2_ANIMATION_STEPS)

    BT25T_p = Bt25T(400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [1, 1, 1, 0])
    BT25T_2_ANIMATION_STEPS = [10, 3, 1, 1, 3, 7, 7, 4, 1, 1, 1, 1]
    BT25T_ANIMATION_LIST = BT25T_p.load_images(sheet.bt25t_2, BT25T_2_ANIMATION_STEPS)

    super_pau = OnlinePlayer(super_pau_online, c.pau, "pau", PAU_ANIMATION_LIST)
    lisa = OnlinePlayer(lisa_online, c.lisa, "lisa", LISA_ANIMATION_LIST)
    vesisa = OnlinePlayer(VESISA_p, c.vesisa, "vesisa", VESISA_ANIMATION_LIST)
    tagir = OnlinePlayer(TAGIR_P, c.tagir, "tagir", TAGIR_ANIMATION_LIST)
    artestro = OnlinePlayer(ARTESTRO_p, c.artestro, ARTESTRO_p.name, ARTESTRO_ANIMATION_LIST)
    aksenov = OnlinePlayer(AKSENOV_p, c.aksenov, AKSENOV_p.name, AKSENOV_ANIMATION_LIST)
    bulat = OnlinePlayer(BULAT_p, c.bulat, BULAT_p.name, BULAT_2_ANIMATION_LIST)
    robot_woman = OnlinePlayer(ROBOT_FEM_p, c.robot_woman, ROBOT_FEM_p.name, ROBOT_WOMAN_ANIMATION_LIST)
    bt25t = OnlinePlayer(BT25T_p, c.bt25, BT25T_p.name, BT25T_ANIMATION_LIST)

    animation_list_by_name = {
        "pau": PAU_ANIMATION_LIST,
        "lisa": LISA_ANIMATION_LIST,
        "vesisa": VESISA_ANIMATION_LIST,
        "tagir": TAGIR_ANIMATION_LIST,
        "artestro": ARTESTRO_ANIMATION_LIST,
        "aksenov": AKSENOV_ANIMATION_LIST,
        "bulat": BULAT_2_ANIMATION_LIST,
        "robot_woman": ROBOT_WOMAN_ANIMATION_LIST,
        "bt25t": BT25T_ANIMATION_LIST
    }

