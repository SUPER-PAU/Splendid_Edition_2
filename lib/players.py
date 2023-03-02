from lib.fighter import FighterEnemy
from lib.player_fighter import FighterPLAYER
from constants.audio.effects import bt_sound, human_sound, woman_sound, boss_sound
import constants.textures.sprites as sheet
from lib.display import display

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 9
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
MAGE_SIZE = 250
MAGE_SCALE = 7 * display.scr_h
MAGE_OFFSET = [112, 110]
MAGE_DATA = [MAGE_SIZE, MAGE_SCALE, MAGE_OFFSET]
AKSENOV_SIZE = 486
AKSENOV_SCALE = 3 * display.scr_h
AKSENOV_OFFSET = [216, 168]
AKSENOV_DATA = [AKSENOV_SIZE, AKSENOV_SCALE, AKSENOV_OFFSET]
LISA_SIZE = 486
LISA_SCALE = 3 * display.scr_h
LISA_OFFSET = [216, 168]
LISA_DATA = [LISA_SIZE, LISA_SCALE, LISA_OFFSET]
GENERAL_DATA = [486, LISA_SCALE, [180, 110]]

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 8, 8, 3, 7]
MAGE_ANIMATION_STEPS = [8, 8, 1, 5, 5, 3, 7]
AKSENOV_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6]
LISA_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 6]
KINGARTEMA_ANIMATION_STEPS = [8, 8, 1, 7, 7, 3, 7]
SOLDIER_ANIMATION_STEPS = [8, 8, 1, 7, 4, 3, 6]
YACUGI_ANIMATION_STEPS = [8, 8, 1, 5, 7, 3, 6]
NEGROMINATOR_ANIMATION_STEPS = [8, 8, 1, 7, 5, 3, 6]
GENERAL_ANIMATION_STEPS = [4, 4, 1, 7, 4, 3, 4]
WALKER_ANIMATION_STEPS = [4, 4, 1, 7, 4, 3, 4]
SUPER_PAU_ANIMATION_STEPS = [8, 8, 1, 6, 7, 3, 6, 4]
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


def reset_players():
    global lisa, fighter_2, aksenov, soldier, yacuji, japan_soldier, police, \
        negrominator, artestro, lisa_boss, general, super_pau_boss, super_pau, bt25t, moiseev, tagir, \
        tagir_enemy, egor, egor_enemy, kingartema, kingartema_enemy, vasisa, vasisa_enemy, bulat, bulat_enemy, \
        robot_woman, super_pau_final_boss, moiseev_security, walker, walker_enemy, trio_enemy, trio, supertank, \
        albinos, moiseev_bot, bt25t_enemy, bt_final_battle
    # restore fighter param
    # player
    bt_final_battle = FighterPLAYER(12, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bt25t,
                              bt25_animation_steps,
                              bt_sound, sheet.bt_parts, sheet.shield_parts)
    trio = FighterPLAYER(11, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.trio,
                         LISA_ANIMATION_STEPS,
                         human_sound, sheet.blood)
    walker = FighterPLAYER(10, 340 * display.scr_w, 370 * display.scr_h, False, GENERAL_DATA, sheet.walker,
                           WALKER_ANIMATION_STEPS,
                           bt_sound, sheet.electricity)
    bulat = FighterPLAYER(9, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bulat,
                          BULAT_ANIMATION_STEPS,
                          human_sound, sheet.blood)
    vasisa = FighterPLAYER(8, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.vesisa,
                           LISA_ANIMATION_STEPS,
                           woman_sound, sheet.blood)
    kingartema = FighterPLAYER(7, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.kingartema,
                               KINGARTEMA_ANIMATION_STEPS,
                               boss_sound, sheet.dumplings)
    egor = FighterPLAYER(6, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.egor,
                         LISA_ANIMATION_STEPS,
                         human_sound, sheet.blood)
    super_pau = FighterPLAYER(1, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.super_pau,
                              SUPER_PAU_ANIMATION_STEPS, human_sound,
                              sheet.blood)
    lisa = FighterPLAYER(2, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.lisa,
                         LISA_ANIMATION_STEPS,
                         woman_sound,
                         sheet.blood)
    aksenov = FighterPLAYER(3, 400 * display.scr_w, 540 * display.scr_h, False, AKSENOV_DATA, sheet.aksenov,
                            LISA_ANIMATION_STEPS,
                            woman_sound, sheet.blood)

    bt25t = FighterPLAYER(4, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.bt25t,
                          bt25_animation_steps,
                          bt_sound, sheet.bt_parts, sheet.shield_parts)
    tagir = FighterPLAYER(5, 400 * display.scr_w, 540 * display.scr_h, False, LISA_DATA, sheet.tagir,
                          TAGIR_ANIMATION_STEPS,
                          human_sound, sheet.blood)
    # enemy
    bt25t_enemy = FighterEnemy(25, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.bt25t,
                          bt25_animation_steps,
                          bt_sound, sheet.bt_parts, sheet.shield_parts)
    moiseev_bot = FighterEnemy(24, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                           sheet.moiseev_bot,
                           SOLDIER_ANIMATION_STEPS, human_sound,
                           sheet.electricity)
    albinos = FighterEnemy(23, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                           sheet.albinos,
                           LISA_ANIMATION_STEPS, woman_sound,
                           sheet.electricity)
    supertank = FighterEnemy(22, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA,
                             sheet.supertank,
                             SUPERTANK_ANIMATION_STEPS, boss_sound,
                             sheet.electricity, sheet.shield_parts)
    trio_enemy = FighterEnemy(21, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                              sheet.trio,
                              LISA_ANIMATION_STEPS, human_sound,
                              sheet.blood)
    walker_enemy = FighterEnemy(20, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA, sheet.walker,
                                WALKER_ANIMATION_STEPS,
                                bt_sound, sheet.electricity, sheet.shield_parts)
    moiseev_security = FighterEnemy(19, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                                    sheet.moiseev_security,
                                    SOLDIER_ANIMATION_STEPS, human_sound,
                                    sheet.blood)
    super_pau_final_boss = FighterEnemy(18, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.super_pau,
                                        SUPER_PAU_ANIMATION_STEPS, human_sound,
                                        sheet.blood)
    robot_woman = FighterEnemy(17, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.robot_woman,
                               LISA_ANIMATION_STEPS,
                               woman_sound, sheet.electricity)
    bulat_enemy = FighterEnemy(16, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.bulat,
                               BULAT_ANIMATION_STEPS,
                               human_sound, sheet.blood)
    vasisa_enemy = FighterEnemy(15, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.vesisa,
                                LISA_ANIMATION_STEPS,
                                woman_sound, sheet.blood, sheet.dust)
    kingartema_enemy = FighterEnemy(14, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.kingartema,
                                    KINGARTEMA_ANIMATION_STEPS,
                                    human_sound, sheet.dumplings)
    egor_enemy = FighterEnemy(13, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.egor,
                              LISA_ANIMATION_STEPS,
                              human_sound, sheet.blood)
    tagir_enemy = FighterEnemy(12, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA,
                               sheet.tagir,
                               TAGIR_ANIMATION_STEPS,
                               human_sound, sheet.blood)
    fighter_2 = FighterEnemy(0, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.artestro,
                             AKSENOV_ANIMATION_STEPS,
                             human_sound, sheet.blood)
    soldier = FighterEnemy(5, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.soldier,
                           SOLDIER_ANIMATION_STEPS,
                           human_sound, sheet.blood)
    japan_soldier = FighterEnemy(6, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.soldier_japan,
                                 SOLDIER_ANIMATION_STEPS,
                                 human_sound, sheet.blood)
    yacuji = FighterEnemy(3, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.yacugi,
                          YACUGI_ANIMATION_STEPS,
                          human_sound,
                          sheet.blood)
    police = FighterEnemy(5, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.police,
                          SOLDIER_ANIMATION_STEPS,
                          human_sound, sheet.blood)
    negrominator = FighterEnemy(7, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.negrominator,
                                SOLDIER_ANIMATION_STEPS,
                                human_sound, sheet.electricity)
    artestro = FighterEnemy(8, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.artestro,
                            AKSENOV_ANIMATION_STEPS,
                            human_sound, sheet.blood)
    lisa_boss = FighterEnemy(9, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.lisa,
                             LISA_ANIMATION_STEPS,
                             woman_sound,
                             sheet.blood)
    general = FighterEnemy(10, 1340 * display.scr_w, 370 * display.scr_h, True, GENERAL_DATA, sheet.general,
                           GENERAL_ANIMATION_STEPS,
                           boss_sound, sheet.electricity, sheet.shield_parts)
    super_pau_boss = FighterEnemy(11, 1400 * display.scr_w, 540 * display.scr_h, True, LISA_DATA, sheet.super_pau_boss,
                                  SUPER_PAU_BOSS_ANIMATION_STEPS,
                                  boss_sound, sheet.blood)
    moiseev = FighterEnemy(1, 1400 * display.scr_w, 540 * display.scr_h, True, AKSENOV_DATA, sheet.moiseev,
                           MAISEEV_ANIMATION_STEPS,
                           human_sound, sheet.blood)
