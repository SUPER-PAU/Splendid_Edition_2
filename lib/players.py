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
LISA_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 7, 7, 10]
KINGARTEMA_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 7]
SOLDIER_ANIMATION_STEPS = [8, 8, 1, 7, 4, 3, 6]
YACUGI_ANIMATION_STEPS = [8, 8, 1, 5, 7, 3, 6]
NEGROMINATOR_ANIMATION_STEPS = [8, 8, 1, 7, 5, 3, 6]
GENERAL_ANIMATION_STEPS = [4, 4, 1, 7, 4, 3, 4]
WALKER_ANIMATION_STEPS = [4, 4, 1, 7, 4, 3, 4]
SUPER_PAU_ANIMATION_STEPS = [8, 8, 1, 6, 7, 3, 6, 4]
SUPER_PAU_PLAYER_ANIMATION_STEPS = [8, 8, 1, 6, 7, 3, 6, 8]
SUPER_PAU_PLAYER_2_ANIMATION_STEPS = [8, 8, 1, 3, 3, 6, 6, 7, 8]
SUPER_PAU_BOSS_ANIMATION_STEPS = [8, 8, 1, 6, 7, 3, 7]
BULAT_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6, 7]
bt25_animation_steps = [10, 3, 1, 7, 4, 3, 7]
MAISEEV_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6, 5]
TAGIR_ANIMATION_STEPS = [8, 4, 1, 6, 4, 3, 6]
SUPERTANK_ANIMATION_STEPS = [4, 4, 1, 8, 8, 3, 4, 8]

# create instances of fighters
lisa = aksenov = super_pau = bt25t = fighter_2 = soldier = japan_soldier = yacuji = police = negrominator = None
artestro = lisa_boss = general = super_pau_boss = moiseev = tagir = tagir_enemy = egor = egor_enemy = None
kingartema = kingartema_enemy = vasisa = vasisa_enemy = bulat = bulat_enemy = robot_woman = super_pau_final_boss = None
moiseev_security = walker_enemy = walker = trio = trio_enemy = supertank = albinos = moiseev_bot = bt25t_enemy = None
bt_final_battle = None

players_for_online = [
    SuperPauPlayer(1, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, [2, 3, 6]),
    LisaPlayer(1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, [2, 1, 3])]
PAU_ANIMATION_LIST = players_for_online[0].load_images(sheet.super_pau_2, SUPER_PAU_PLAYER_2_ANIMATION_STEPS)
LISA_ANIMATION_LIST = players_for_online[1].load_images(sheet.lisa_2, LISA_2_ANIMATION_STEPS)


def reset_players():
    global lisa, fighter_2, aksenov, soldier, yacuji, japan_soldier, police, \
        negrominator, artestro, lisa_boss, general, super_pau_boss, super_pau, bt25t, moiseev, tagir, \
        tagir_enemy, egor, egor_enemy, kingartema, kingartema_enemy, vasisa, vasisa_enemy, bulat, bulat_enemy, \
        robot_woman, super_pau_final_boss, moiseev_security, walker, walker_enemy, trio_enemy, trio, supertank, \
        albinos, moiseev_bot, bt25t_enemy, bt_final_battle, players_for_online
    # restore fighter param
    # player
    bt_final_battle = FighterPLAYER(12, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bt25t,
                                    bt25_animation_steps,
                                    bt_sound, sheet.bt_parts, [0, 2])
    trio = FighterPLAYER(11, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.trio,
                         LISA_ANIMATION_STEPS,
                         human_sound, sheet.blood, [3, 2])
    walker = FighterPLAYER(10, 340 * display.scr_w, 370 * display.scr_h, False, GENERAL_DATA, sheet.walker,
                           WALKER_ANIMATION_STEPS,
                           bt_sound, sheet.electricity, [2, 1])
    bulat = FighterPLAYER(9, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bulat,
                          BULAT_ANIMATION_STEPS,
                          human_sound, sheet.blood, [2, 2, 2])
    vasisa = FighterPLAYER(8, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.vesisa,
                           LISA_ANIMATION_STEPS,
                           woman_sound, sheet.blood, [2, 2])
    kingartema = FighterPLAYER(7, 400 * display.scr_w, 540 * display.scr_h, False, KINGARTEMA_DATA, sheet.kingartema,
                               KINGARTEMA_ANIMATION_STEPS,
                               boss_sound, sheet.dumplings, [2, 2])
    egor = FighterPLAYER(6, 400 * display.scr_w, 740 * display.scr_h, False, EGOR_DATA, sheet.egor,
                         LISA_ANIMATION_STEPS,
                         human_sound, sheet.blood, [2, 3])
    super_pau = FighterPLAYER(1, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.SUPER_PAU,
                              SUPER_PAU_PLAYER_ANIMATION_STEPS, human_sound,
                              sheet.blood, [2, 3, 6])
    lisa = FighterPLAYER(2, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.lisa,
                         LISA_ANIMATION_STEPS,
                         woman_sound,
                         sheet.blood, [2, 1])
    aksenov = FighterPLAYER(3, 400 * display.scr_w, 540 * display.scr_h, False, AKSENOV_DATA, sheet.aksenov,
                            LISA_ANIMATION_STEPS,
                            woman_sound, sheet.blood, [2, 2])

    bt25t = FighterPLAYER(4, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bt25t,
                          bt25_animation_steps,
                          bt_sound, sheet.bt_parts, [0, 2])
    tagir = FighterPLAYER(5, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.tagir,
                          TAGIR_ANIMATION_STEPS,
                          human_sound, sheet.blood, [0, 2])
    # enemy
    bt25t_enemy = FighterEnemy(25, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.bt25t,
                               bt25_animation_steps,
                               bt_sound, sheet.bt_parts, [0, 2])
    moiseev_bot = FighterEnemy(24, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                               sheet.moiseev_bot,
                               SOLDIER_ANIMATION_STEPS, human_sound,
                               sheet.electricity, [3, 1])
    albinos = FighterEnemy(23, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                           sheet.albinos,
                           LISA_ANIMATION_STEPS, woman_sound,
                           sheet.electricity, [3])
    supertank = FighterEnemy(22, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA,
                             sheet.supertank,
                             SUPERTANK_ANIMATION_STEPS, boss_sound,
                             sheet.electricity, [2, 2, 0])
    trio_enemy = FighterEnemy(21, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                              sheet.trio,
                              LISA_ANIMATION_STEPS, human_sound,
                              sheet.blood, [3, 2])
    walker_enemy = FighterEnemy(20, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA, sheet.walker,
                                WALKER_ANIMATION_STEPS,
                                bt_sound, sheet.electricity, [2, 1])
    moiseev_security = FighterEnemy(19, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                                    sheet.moiseev_security,
                                    SOLDIER_ANIMATION_STEPS, human_sound,
                                    sheet.blood, [4, 1])
    super_pau_final_boss = FighterEnemy(18, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.super_pau,
                                        SUPER_PAU_ANIMATION_STEPS, human_sound,
                                        sheet.blood, [2, 3, 2])
    robot_woman = FighterEnemy(17, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.robot_woman,
                               LISA_ANIMATION_STEPS,
                               woman_sound, sheet.electricity, [3, 3])
    bulat_enemy = FighterEnemy(16, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.bulat,
                               BULAT_ANIMATION_STEPS,
                               human_sound, sheet.blood, [2, 2, 2])
    vasisa_enemy = FighterEnemy(15, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.vesisa,
                                LISA_ANIMATION_STEPS,
                                woman_sound, sheet.blood, [2, 2])
    kingartema_enemy = FighterEnemy(14, 1400 * display.scr_w, 540 * display.scr_h, True, KINGARTEMA_DATA,
                                    sheet.kingartema,
                                    KINGARTEMA_ANIMATION_STEPS,
                                    human_sound, sheet.dumplings, [2, 2])
    egor_enemy = FighterEnemy(13, 1400 * display.scr_w, 740 * display.scr_h, True, EGOR_DATA, sheet.egor,
                              LISA_ANIMATION_STEPS,
                              human_sound, sheet.blood, [2, 3])
    tagir_enemy = FighterEnemy(12, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                               sheet.tagir,
                               TAGIR_ANIMATION_STEPS,
                               human_sound, sheet.blood, [2, 0])
    fighter_2 = FighterEnemy(0, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.artestro,
                             AKSENOV_ANIMATION_STEPS,
                             human_sound, sheet.blood, [1, 1])
    soldier = FighterEnemy(5, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.soldier,
                           SOLDIER_ANIMATION_STEPS,
                           human_sound, sheet.blood, [3, 1])
    japan_soldier = FighterEnemy(6, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.soldier_japan,
                                 SOLDIER_ANIMATION_STEPS,
                                 human_sound, sheet.blood, [3, 1])
    yacuji = FighterEnemy(3, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.yacugi,
                          YACUGI_ANIMATION_STEPS,
                          human_sound,
                          sheet.blood, [2, 1])
    police = FighterEnemy(5, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.police,
                          SOLDIER_ANIMATION_STEPS,
                          human_sound, sheet.blood, [3, 1])
    negrominator = FighterEnemy(7, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.negrominator,
                                SOLDIER_ANIMATION_STEPS,
                                human_sound, sheet.electricity, [2, 1])
    artestro = FighterEnemy(8, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.artestro,
                            AKSENOV_ANIMATION_STEPS,
                            human_sound, sheet.blood, [1, 2])
    lisa_boss = FighterEnemy(9, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.lisa,
                             LISA_ANIMATION_STEPS,
                             woman_sound,
                             sheet.blood, [2, 1])
    general = FighterEnemy(10, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA, sheet.general,
                           GENERAL_ANIMATION_STEPS,
                           boss_sound, sheet.electricity, [1, 2])
    super_pau_boss = FighterEnemy(11, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.super_pau_boss,
                                  SUPER_PAU_BOSS_ANIMATION_STEPS,
                                  boss_sound, sheet.blood, [2, 3])
    moiseev = FighterEnemy(1, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.moiseev,
                           MAISEEV_ANIMATION_STEPS,
                           human_sound, sheet.blood, [4, 4, 2])
