from lib.fighter import FighterEnemy
from lib.player_fighter import FighterPLAYER
from constants.audio.effects import bt_sound, human_sound, woman_sound, boss_sound
import constants.textures.sprites as sheet
from lib.display import display

# define fighter variables
from lib.players_data.LISA_PLAYER import LisaPlayer
from lib.players_data.SUPER_PAU_PLAYER import SuperPauPlayer

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

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 8, 8, 3, 7]
MAGE_ANIMATION_STEPS = [8, 8, 1, 5, 5, 3, 7]
AKSENOV_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6]
LISA_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6]
LISA_BOSS_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6, 10]
KINGARTEMA_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 7]
SOLDIER_ANIMATION_STEPS = [8, 8, 1, 7, 4, 3, 6]
YACUGI_ANIMATION_STEPS = [8, 8, 1, 5, 7, 3, 6]
NEGROMINATOR_ANIMATION_STEPS = [8, 8, 1, 7, 5, 3, 6]
GENERAL_ANIMATION_STEPS = [4, 4, 1, 8, 4, 3, 4, 7]
WALKER_ANIMATION_STEPS = [4, 4, 1, 7, 4, 3, 4]
SUPER_PAU_ANIMATION_STEPS = [8, 8, 1, 6, 7, 3, 6, 4]
SUPER_PAU_PLAYER_ANIMATION_STEPS = [8, 8, 1, 6, 7, 3, 6, 8]
SUPER_PAU_BOSS_ANIMATION_STEPS = [8, 8, 1, 6, 7, 3, 7]
BULAT_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6, 7]
bt25_animation_steps = [10, 3, 1, 7, 4, 3, 7]
MAISEEV_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6, 5]
TAGIR_ANIMATION_STEPS = [8, 4, 1, 6, 4, 3, 6]
SUPERTANK_ANIMATION_STEPS = [4, 4, 1, 8, 8, 3, 4, 8]

LISA_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 10, 3, 5, 6]
SUPER_PAU_PLAYER_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 6, 7, 8, 3, 5, 6]
VESISA_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 0, 3, 5, 6]


# create instances of fighters

# players_for_online = [
#     [False, False, False, None],
#     [False, False, False, None]]

# super_pau_online = SuperPauPlayer(1, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 3, 6, 2, 8])
# lisa_online = LisaPlayer(1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, [2, 1, 3, 2, 8])
# PAU_ANIMATION_LIST = super_pau_online.load_images(sheet.super_pau_2, SUPER_PAU_PLAYER_2_ANIMATION_STEPS)
# LISA_ANIMATION_LIST = lisa_online.load_images(sheet.lisa_2, LISA_2_ANIMATION_STEPS)

# player
def bt_final_battle():
    return FighterPLAYER(12, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bt25t,
                         bt25_animation_steps,
                         bt_sound, sheet.bt_parts, [0, 2])


def trio():
    return FighterPLAYER(11, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.trio,
                         LISA_ANIMATION_STEPS,
                         human_sound, sheet.blood, [3, 2])


def walker():
    return FighterPLAYER(10, 340 * display.scr_w, 370 * display.scr_h, False, GENERAL_DATA, sheet.walker,
                         WALKER_ANIMATION_STEPS,
                         bt_sound, sheet.electricity, [2, 1])


def bulat():
    return FighterPLAYER(9, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bulat,
                         BULAT_ANIMATION_STEPS,
                         human_sound, sheet.blood, [2, 2, 2])


def vasisa():
    return FighterPLAYER(8, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.vesisa,
                         LISA_ANIMATION_STEPS,
                         woman_sound, sheet.blood, [2, 2])


def kingartema():
    return FighterPLAYER(7, 400 * display.scr_w, 540 * display.scr_h, False, KINGARTEMA_DATA, sheet.kingartema,
                         KINGARTEMA_ANIMATION_STEPS,
                         boss_sound, sheet.dumplings, [2, 2])


def egor():
    return FighterPLAYER(6, 400 * display.scr_w, 740 * display.scr_h, False, EGOR_DATA, sheet.egor,
                         LISA_ANIMATION_STEPS,
                         human_sound, sheet.blood, [2, 3])


def super_pau():
    return FighterPLAYER(1, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.SUPER_PAU,
                         SUPER_PAU_PLAYER_ANIMATION_STEPS, human_sound,
                         sheet.blood, [2, 3, 6])


def lisa():
    return FighterPLAYER(2, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.lisa,
                         LISA_ANIMATION_STEPS,
                         woman_sound,
                         sheet.blood, [2, 1])


def bt25t():
    return FighterPLAYER(4, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bt25t,
                         bt25_animation_steps,
                         bt_sound, sheet.bt_parts, [0, 2])


def aksenov():
    return FighterPLAYER(3, 400 * display.scr_w, 540 * display.scr_h, False, AKSENOV_DATA, sheet.aksenov,
                         LISA_ANIMATION_STEPS,
                         woman_sound, sheet.blood, [2, 2])


def tagir():
    return FighterPLAYER(5, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.tagir,
                         TAGIR_ANIMATION_STEPS,
                         human_sound, sheet.blood, [0, 2])


# enemy
def bt25t_enemy():
    return FighterEnemy(25, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.bt25t,
                        bt25_animation_steps,
                        bt_sound, sheet.bt_parts, [0, 2])


def moiseev_bot():
    return FighterEnemy(24, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                        sheet.moiseev_bot,
                        SOLDIER_ANIMATION_STEPS, human_sound,
                        sheet.electricity, [3, 1])


def albinos():
    return FighterEnemy(23, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                        sheet.albinos,
                        LISA_ANIMATION_STEPS, woman_sound,
                        sheet.electricity, [3])


def supertank():
    return FighterEnemy(22, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA,
                        sheet.supertank,
                        SUPERTANK_ANIMATION_STEPS, boss_sound,
                        sheet.electricity, [2, 2, 0])


def trio_enemy():
    return FighterEnemy(21, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                        sheet.trio,
                        LISA_ANIMATION_STEPS, human_sound,
                        sheet.blood, [3, 2])


def walker_enemy():
    return FighterEnemy(20, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA, sheet.walker,
                        WALKER_ANIMATION_STEPS,
                        bt_sound, sheet.electricity, [2, 1])


def moiseev_security():
    return FighterEnemy(19, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                        sheet.moiseev_security,
                        SOLDIER_ANIMATION_STEPS, human_sound,
                        sheet.blood, [4, 1])


def super_pau_final_boss():
    return FighterEnemy(18, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.super_pau,
                        SUPER_PAU_ANIMATION_STEPS, human_sound,
                        sheet.blood, [2, 3, 2])


def robot_woman():
    return FighterEnemy(17, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.robot_woman,
                        LISA_ANIMATION_STEPS,
                        woman_sound, sheet.electricity, [3, 3])


def bulat_enemy():
    return FighterEnemy(16, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.bulat,
                        BULAT_ANIMATION_STEPS,
                        human_sound, sheet.blood, [2, 2, 2])


def vasisa_enemy():
    return FighterEnemy(15, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.vesisa,
                        LISA_ANIMATION_STEPS,
                        woman_sound, sheet.blood, [2, 2])


def kingartema_enemy():
    return FighterEnemy(14, 1400 * display.scr_w, 540 * display.scr_h, True, KINGARTEMA_DATA,
                        sheet.kingartema,
                        KINGARTEMA_ANIMATION_STEPS,
                        human_sound, sheet.dumplings, [2, 2])


def egor_enemy():
    return FighterEnemy(13, 1400 * display.scr_w, 740 * display.scr_h, True, EGOR_DATA, sheet.egor,
                        LISA_ANIMATION_STEPS,
                        human_sound, sheet.blood, [2, 3])


def tagir_enemy():
    return FighterEnemy(12, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                        sheet.tagir,
                        TAGIR_ANIMATION_STEPS,
                        human_sound, sheet.blood, [2, 0])


def fighter_2():
    return FighterEnemy(0, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.artestro,
                        AKSENOV_ANIMATION_STEPS,
                        human_sound, sheet.blood, [1, 1])


def soldier():
    return FighterEnemy(5, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.soldier,
                        SOLDIER_ANIMATION_STEPS,
                        human_sound, sheet.blood, [3, 1])


def japan_soldier():
    return FighterEnemy(6, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.soldier_japan,
                        SOLDIER_ANIMATION_STEPS,
                        human_sound, sheet.blood, [3, 1])


def yacuji():
    return FighterEnemy(3, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.yacugi,
                        YACUGI_ANIMATION_STEPS,
                        human_sound,
                        sheet.blood, [2, 1])


def police():
    return FighterEnemy(5, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.police,
                        SOLDIER_ANIMATION_STEPS,
                        human_sound, sheet.blood, [3, 1])


def negrominator():
    return FighterEnemy(7, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.negrominator,
                        SOLDIER_ANIMATION_STEPS,
                        human_sound, sheet.electricity, [2, 1])


def artestro():
    return FighterEnemy(8, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.artestro,
                        AKSENOV_ANIMATION_STEPS,
                        human_sound, sheet.blood, [1, 2])


def lisa_boss():
    return FighterEnemy(9, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.lisa_boss,
                        LISA_BOSS_ANIMATION_STEPS,
                        woman_sound,
                        sheet.blood, [2, 1, 2, 8])


def general():
    return FighterEnemy(10, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA, sheet.general,
                        GENERAL_ANIMATION_STEPS,
                        boss_sound, sheet.electricity, [7, 2, 1])


def super_pau_boss():
    return FighterEnemy(11, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.super_pau_boss,
                        SUPER_PAU_BOSS_ANIMATION_STEPS,
                        boss_sound, sheet.blood, [2, 3])


def moiseev():
    return FighterEnemy(1, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.moiseev,
                        MAISEEV_ANIMATION_STEPS,
                        human_sound, sheet.blood, [4, 4, 2])


class FightersInstances:
    def __init__(self):
        self.enemy_figters = []
        self.player_fighters = []

    def reset_players_story(self, game_progress):
        self.enemy_figters = None
        self.player_fighters = None
        match game_progress:
            case 0:
                self.player_fighters = [super_pau(), bt25t()]
                self.enemy_figters = [moiseev_security(), moiseev_security()]
            case 1:
                self.player_fighters = [super_pau(), bt25t()]
                self.enemy_figters = [moiseev_security(), moiseev_security()]
            case 2:
                self.player_fighters = [super_pau(), bt25t()]
                self.enemy_figters = [trio_enemy(), trio_enemy()]
            case 3:
                self.player_fighters = bt25t()
                self.enemy_figters = police()
            case 4:
                self.player_fighters = bt25t()
                self.enemy_figters = albinos()
            case 5:
                self.player_fighters = super_pau()
                self.enemy_figters = bulat_enemy()
            case 6:
                self.player_fighters = bulat()
                self.enemy_figters = moiseev_security()
            case 7:
                self.player_fighters = [super_pau(), bt25t(), bulat()]
                self.enemy_figters = [negrominator(), negrominator(), walker_enemy()]
            case 8:
                self.player_fighters = aksenov()
                self.enemy_figters = negrominator()
            case 9:
                self.player_fighters = super_pau()
                self.enemy_figters = tagir_enemy()
            case 10:
                self.player_fighters = [super_pau(), aksenov(), bt25t(), bulat()]
                self.enemy_figters = [tagir_enemy(), tagir_enemy(), egor_enemy(), egor_enemy()]
            case 11:
                self.player_fighters = super_pau()
                self.enemy_figters = kingartema_enemy()
            case 12:
                self.player_fighters = [super_pau(), bt25t(), aksenov(), bulat()]
                self.enemy_figters = [tagir_enemy(), egor_enemy(), egor_enemy(), kingartema_enemy()]
            case 13:
                self.player_fighters = super_pau()
                self.enemy_figters = moiseev()
            case 14:
                self.player_fighters = trio()
                self.enemy_figters = moiseev_bot()
            case 15:
                self.player_fighters = super_pau()
                self.enemy_figters = japan_soldier()
            case 16:
                self.player_fighters = bt25t()
                self.enemy_figters = soldier()
            case 17:
                self.player_fighters = egor()
                self.enemy_figters = moiseev_bot()
            case 18:
                self.player_fighters = [super_pau(), super_pau(), super_pau(), super_pau(), super_pau(), super_pau()]
                self.enemy_figters = [soldier(), soldier(), japan_soldier(), japan_soldier(), moiseev_bot(),
                                      moiseev_bot()]
            case 19:
                self.player_fighters = bulat()
                self.enemy_figters = moiseev_bot()
            case 20:
                self.player_fighters = super_pau()
                self.enemy_figters = moiseev()
            case 21:
                self.player_fighters = super_pau()
                self.enemy_figters = moiseev_security()
            case 22:
                self.player_fighters = [super_pau(), super_pau(), super_pau(), super_pau(), super_pau(), super_pau(),
                                        super_pau(), super_pau()]
                self.enemy_figters = [egor_enemy(), egor_enemy(), trio_enemy(), trio_enemy(), kingartema_enemy(),
                                      kingartema_enemy(), bt25t_enemy(), bt25t_enemy()]
            case 23:
                self.player_fighters = [tagir(), tagir(), aksenov(), aksenov()]
                self.enemy_figters = [egor_enemy(), trio_enemy(), bt25t_enemy(), kingartema_enemy()]
            case 24:
                self.player_fighters = [bt25t(), super_pau(), bt25t(), super_pau(), super_pau(), super_pau(), bt25t(),
                                        super_pau()]
                self.enemy_figters = [egor_enemy(), egor_enemy(), trio_enemy(), trio_enemy(), kingartema_enemy(),
                                      kingartema_enemy(), tagir_enemy(), tagir_enemy()]
            case 25:
                self.player_fighters = super_pau()
                self.enemy_figters = bulat_enemy()
            case 26:
                self.player_fighters = aksenov()
                self.enemy_figters = soldier()
            case 27:
                self.player_fighters = lisa()
                self.enemy_figters = yacuji()
            case 28:
                self.player_fighters = lisa()
                self.enemy_figters = police()
            case 29:
                self.player_fighters = lisa()
                self.enemy_figters = super_pau_boss()
            case 30:
                self.player_fighters = lisa()
                self.enemy_figters = yacuji()
            case 31:
                self.player_fighters = vasisa()
                self.enemy_figters = moiseev_bot()
            case 32:
                self.player_fighters = [lisa(), lisa()]
                self.enemy_figters = [police(), japan_soldier()]
            case 33:
                self.player_fighters = aksenov()
                self.enemy_figters = yacuji()
            case 34:
                self.player_fighters = lisa()
                self.enemy_figters = artestro()
            case 35:
                self.player_fighters = aksenov()
                self.enemy_figters = japan_soldier()
            case 36:
                self.player_fighters = super_pau()
                self.enemy_figters = lisa_boss()
            case 37:
                self.player_fighters = aksenov()
                self.enemy_figters = lisa_boss()
            case 38:
                self.player_fighters = aksenov()
                self.enemy_figters = negrominator()
            case 39:
                self.player_fighters = aksenov()
                self.enemy_figters = soldier()
            case 40:
                self.player_fighters = [aksenov(), aksenov()]
                self.enemy_figters = [police(), japan_soldier()]
            case 41:
                self.player_fighters = [aksenov(), aksenov(), aksenov(), aksenov()]
                self.enemy_figters = [negrominator(), negrominator(), walker_enemy(), walker_enemy()]
            case 42:
                self.player_fighters = aksenov()
                self.enemy_figters = general()
            case 43:
                self.player_fighters = aksenov()
                self.enemy_figters = walker_enemy()
            case 44:
                self.player_fighters = aksenov()
                self.enemy_figters = negrominator()
            case 45:
                self.player_fighters = [tagir(), aksenov(), kingartema(), bt25t(), egor()]
                self.enemy_figters = [negrominator(), walker_enemy(), walker_enemy(), walker_enemy(), general()]
            case 46:
                self.player_fighters = vasisa()
                self.enemy_figters = robot_woman()
            case 47:
                self.player_fighters = [trio(), trio()]
                self.enemy_figters = [moiseev_bot(), robot_woman()]
            case 48:
                self.player_fighters = [aksenov(), tagir(), bt25t()]
                self.enemy_figters = [negrominator(), negrominator(), general()]
            case 49:
                self.player_fighters = walker()
                self.enemy_figters = negrominator()
            case 50:
                self.player_fighters = [kingartema(), egor()]
                self.enemy_figters = [moiseev_bot(), general()]
            case 51:
                self.player_fighters = [aksenov(), aksenov(), tagir(), tagir(), trio(), trio(), bt25t(), bt25t()]
                self.enemy_figters = [moiseev_bot(), negrominator(), negrominator(), robot_woman(), walker_enemy(),
                                      general(), robot_woman(), general()]
            case 52:
                self.player_fighters = vasisa()
                self.enemy_figters = supertank()
            case 53:
                self.player_fighters = bt25t()
                self.enemy_figters = vasisa_enemy()
            case 54:
                self.player_fighters = bt_final_battle()
                self.enemy_figters = super_pau_final_boss()


fighter_instances = FightersInstances()
