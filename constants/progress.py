import constants.audio.music as music
import constants.textures.backgrounds as bg

# Игровой прогресс
# Используется как аргументы для функции check_game_progress() в файле main.py
#   (bg., music.),
pg = [
    (bg.lab_mais_tutorial, music.lisa_boss),    # 0
    (bg.lab_mais, music.scyscrapers),   # 1
    (bg.kazan_city_2050, music.streets),    # 2
    (bg.kazan_city_2050, music.streets),    # 3
    (bg.daun_corp_2050, music.city_center),     # 4
    (bg.daun_corp_2050, music.the_only_thing_i_know_instrumental),  # 5
    (bg.daun_corp_2050, music.streets),  # 6
    (bg.destroyed_daun_corp, music.digital_justice),  # 7
    (bg.destroyed_daun_corp, music.digital_justice),  # 8
    (bg.saratov_iskhakov, music.parlament),  # 9
    (bg.saratov_moiseev, music.lisa_boss),  # 10
    (bg.saratov_moiseev, music.the_stains_of_time_instrumental),  # 11
    (bg.bunker, music.lower_levels),  # 12
    (bg.angar_animated, music.burning_town),  # 13
    (bg.canals, music.scyscrapers),  # 14
    (bg.war_kazan, music.gates_of_shadows),  # 15
    (bg.war_kazan, music.gates_of_shadows),  # 16
    (bg.kazan_afterwar, music.city_center),  # 17
    (bg.moiseev_garage, music.night_square),  # 18
    (bg.moiseev_collider, music.collider),  # 19
    (bg.moiseev_collider_animated, music.roboboss_roof),  # 20
    (bg.subway, music.night_square),  # 21
    (bg.bulat_lab, music.may),  # 22
    (bg.bulats_robot, music.gates_of_shadows),  # 23
    (bg.broken_robot, music.burning_town),  # 24
    (bg.broken_robot, music.the_only_thing_i_know_instrumental),  # 25
    (bg.broken_robot, music.broken_robot),  # 26
    (bg.shop, music.streets),  # 27
    (bg.shop, music.streets),  # 28
    (bg.aboba, music.aboba_realm),  # 29
    (bg.city_center, music.city_center),  # 30
    (bg.corporation_lab, music.lower_levels),  # 31
    (bg.parlament, music.parlament),  # 32
    (bg.parlament, music.city_center),  # 33
    (bg.buildings, music.valorant_halftrue_remix),  # 34
    (bg.shop, music.scyscrapers),  # 35
    (bg.aboba, music.aboba_realm),  # 36
    (bg.japan_lisa_fight, music.a_stranger_i_remain_instrumental),  # 37
    (bg.city_ruins, music.negrominator_invasion),  # 38
    (bg.shelter, music.lisa_boss2),  # 39
    (bg.shelter, music.lisa_boss2),  # 40
    (bg.city_ruins, music.negrominator_invasion),  # 41
    (bg.explosion, music.red_sun_instrumental),  # 42
    (bg.city_ruins, music.negrominator_invasion),  # 43
    (bg.destroyed_daun_corp, music.digital_justice),  # 44
    (bg.destroyed_iskhakov, music.digital_justice),  # 45
    (bg.corporation_lab, music.lower_levels),  # 46
    (bg.corporation_lab, music.lower_levels),  # 47
    (bg.america_rooftops, music.deep_down),  # 48
    (bg.africa_conveyer, music.war_machines),  # 49
    (bg.broken_conveyer, music.war_machines),  # 50
    (bg.american_collider, music.citadel),  # 51
    (bg.collider_top_1, music.collective_consciousness),  # 52
    (bg.collider_top_2, music.shadow_throne),  # 53
    (bg.portal_final_battle, music.titan),  # 54
    (bg.portal, music.titan),  # 55
    (bg.american_collider, music.shadow_throne)  # 56 online
]
