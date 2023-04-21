import random

import pygame

import lib.players as fighter
from lib.clock import Clock
from lib.display import display
from lib.drawer import draw_health_bar, draw_text, check_bg_instance
from lib.mixer import play_music_bg
from lib.dialogs import dialogs_texts
from lib.Menu import MainMenu, ChooseModeMenu, OptionsMenu, ChooseOnlineModeMenu, ChooseHeroMenu, OnlineBattle
from lib.Database import update_gp, get_gp, get_player_name
from constants.textures.sprites import all_sprites, bullet_sprites, attack_group, enemy_attack_group, damage_num_group
from lib.Settings import settings

# Константы/переменные
import constants.textures.backgrounds as bg
import constants.audio.music as music
import constants.colors as color
import constants.fonts.turok as fonts
from constants.progress import pg
from lib.online.network import Network

import lib.players_data.online_players as online_fighter
from lib.players_data.particles_online import on_fire_class_enemy

clocks = Clock()

# fonts
font, count_font, score_font = fonts.sys, fonts.bigger_sys, fonts.bigger_sys
# dialogs
texts = dialogs_texts()
# menus
game_menu = MainMenu(display.scr_w, display.scr_h, bg.main_menu, music.main_menu)
options_menu = OptionsMenu(display.scr_w, display.scr_h, bg.options_menu)
choose_mode_menu = ChooseModeMenu(display.scr_w, display.scr_h, bg.game_menu_animated, music.main_menu)
choose_online_mode_menu = ChooseOnlineModeMenu(display.scr_w, display.scr_h, bg.online_menu, music.main_menu, "")
hero_choose_menu = ChooseHeroMenu(bg.hero_pick_menu)
bg.briff_war.play()
display.set_fps(24)


class Game:
    def __init__(self):
        self.intro_count = 4
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]  # player scores. [P1, p2]
        self.round_over = False
        self.final_round_over = True
        self.post_fight_dial = False
        self.is_dialogue = False
        self.main_campain_on = False
        self.online_on = False
        self.aplication_run = True
        self.playing_cutscene = True
        self.ROUND_OVER_COOLDOWN = 2000
        self.idx = 0
        self.round_over_time = 1
        self.fighter_id = 0
        self.GAME_PROGRESS = get_gp()

        self.network = None
        self.online_player = online_fighter.super_pau
        self.team = [online_fighter.lisa, online_fighter.super_pau, online_fighter.tagir]
        self.enemy = None
        self.chosen = False
        self.team_player = 6
        self.choose_hero_window_on = False

        self.online_location = None
        self.playing_emoji = False
        self.enemy_was_attacking = False
        self.lost = False
        self.online_name = str(get_player_name())
        self.current_player = 1
        self.battle_menu = OnlineBattle(bg.choose_hero, self.team, self.online_name)

    def online_fight(self, mouse_click, key_press):
        self.check_game_progress(*pg[self.online_location])

        fighter1 = self.online_player.player
        fighter2 = self.enemy[0]

        fighter1.ready_for_fight()

        attack_group.update(fighter2, fighter1, 1)

        draw_text("YOU", fonts.online_font, (0, 0, 0), fighter1.rect.centerx - 30, 1010)
        draw_text("YOU", fonts.online_font, (255, 255, 255), fighter1.rect.centerx - 31, 1011)

        fighter1.draw_hp()
        fighter1.draw_round_statistic(self.online_name, font)
        fighter2.draw_hp()
        fighter2.draw_round_statistic(self.enemy[6], font)

        if fighter2.playing_emoji is True and not self.playing_emoji:
            fighter2.play_emoji()
            self.playing_emoji = True
        elif not fighter2.playing_emoji and self.playing_emoji:
            self.playing_emoji = False

        # update fighters
        fighter1.check_action()
        fighter2.check_action()

        firgter2_action, fighter2_frame_index = fighter2.get_animation_params()

        # get_image
        figter2_sprite = online_fighter.animation_list_by_name[fighter2.name][firgter2_action][fighter2_frame_index]

        # update countdown
        if self.intro_count <= 0:
            if fighter1.stunned <= 0:
                # move fighter
                fighter1.move(display.screen, fighter2, self.round_over, mouse_click, key_press)
        else:
            # display count timer
            draw_text(str(self.intro_count), count_font, color.red, display.screen_width / 2 - 20 * display.scr_w,
                      10 * display.scr_h)
            # update count timer
            if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                self.intro_count -= 1
                self.last_count_update = pygame.time.get_ticks()

        self.final_round_over = False

        # draw fighters
        fighter2.draw(display.screen, figter2_sprite)
        self.online_player.draw_p()

        if fighter2.fire_cooldown > 0:
            on_fire_class_enemy.update()
            fighter2.burn(on_fire_class_enemy.get_image())

        # check for player defeat
        if not self.round_over:
            if not fighter1.alive:
                fighter1.health = 0
                self.score[1] += 1
                self.round_over = True
                self.chosen = False
                self.team_player = 6
                self.round_over_time = pygame.time.get_ticks()
            if not fighter2.alive:
                self.score[0] += 1
                self.round_over = True
                self.round_over_time = pygame.time.get_ticks()
        else:
            all_sprites.empty()
            enemy_attack_group.empty()
            attack_group.empty()
            bullet_sprites.empty()
            if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                self.intro_count = 4
                self.battle_menu.enable()

        self.enemy[4].update(fighter1, fighter2, 2)
        self.enemy[5].update(fighter1, 2)
        all_sprites.update()
        all_sprites.draw(display.screen)
        bullet_sprites.update(fighter2, 1)

    def game_navigation(self, key_click, mouse_click):
        global choose_online_mode_menu, hero_choose_menu
        # navigate menu
        if self.main_campain_on:
            self.main_campain_game(key_click)

        if self.online_on:
            if self.final_round_over:
                self.check_game_progress(*pg[self.online_location])
                self.final_round_over = False
                self.round_over = True
                self.battle_menu = OnlineBattle(bg.choose_hero, self.team, self.online_name)
                self.battle_menu.enable()
            if self.battle_menu.is_enabled():
                damage_num_group.empty()
                bullet_sprites.empty()
                all_sprites.empty()
                enemy_attack_group.empty()
                attack_group.empty()
                self.enemy = self.network.send([self.online_player.player, self.chosen, self.lost,
                                                [self.team[0].player, self.team[1].player, self.team[2].player],
                                                attack_group, bullet_sprites, self.online_name])
                if self.online_player.player.health != 100 and not self.enemy[0]:
                    self.enemy[2] = True
                self.intro_count = 4
                self.battle_menu.show(mouse_click, self.chosen, self.enemy[3], self.enemy[6])
                if not self.enemy[0]:
                    if self.battle_menu.cansel_button.is_clicked():
                        self.battle_menu.disable()
                        self.score = [0, 0]
                        self.team_player = 6
                        choose_online_mode_menu.enable()
                        self.online_on = False
                        self.final_round_over = True

                        for player in self.team:
                            player.reset_params()
                        self.network.leave()
                        self.chosen = False
                        self.lost = False
                        self.network = None
                        self.intro_count = 4
                        mouse_click = False
                else:
                    if self.battle_menu.player_hero_1.is_clicked():
                        self.battle_menu.player_hero_1.set_picked()
                        self.online_player = self.team[0]
                        self.chosen = True
                        self.online_player.player.set_side(self.current_player)
                    elif self.battle_menu.player_hero_2.is_clicked():
                        self.battle_menu.player_hero_2.set_picked()
                        self.online_player = self.team[1]
                        self.chosen = True
                        self.online_player.player.set_side(self.current_player)
                    elif self.battle_menu.player_hero_3.is_clicked():
                        self.battle_menu.player_hero_3.set_picked()
                        self.online_player = self.team[2]
                        self.chosen = True
                        self.online_player.player.set_side(self.current_player)
                    if self.lost or self.enemy[2] or (self.score != [0, 0] and not self.enemy[0]):
                        self.battle_menu.disable()
                        self.score = [0, 0]
                        self.team_player = 6
                        choose_online_mode_menu.enable()
                        self.online_on = False
                        self.final_round_over = True

                        for player in self.team:
                            player.reset_params()
                        self.network.leave()
                        self.chosen = False
                        self.lost = False
                        self.network = None
                        self.intro_count = 4
                    elif not self.team[0].player.alive and not \
                            self.team[1].player.alive and not self.team[2].player.alive:
                        self.lost = True
                        self.network.send([self.online_player.player, self.chosen, self.lost,
                                          [self.team[0].player, self.team[1].player, self.team[2].player],
                                           attack_group, bullet_sprites, self.online_name])
                    if self.enemy[1] and self.chosen:
                        self.battle_menu.disable()
                        self.round_over = False
            else:
                self.enemy = self.network.send([self.online_player.player, self.chosen, self.lost, None,
                                       attack_group, bullet_sprites, self.online_name])
                if self.enemy[0]:
                    self.online_fight(mouse_click, key_click)
                else:
                    self.battle_menu.enable()

        if choose_online_mode_menu.is_enabled():
            choose_online_mode_menu.show(mouse_click, key_click, self.team)
            if choose_online_mode_menu.exit_button.is_clicked():
                choose_online_mode_menu.disable()
                display.set_normal_window()
                game_menu.enable()

            if choose_online_mode_menu.hero_button_1.is_clicked():
                choose_online_mode_menu.disable()
                hero_choose_menu.enable(0)
                mouse_click = False
            elif choose_online_mode_menu.hero_button_2.is_clicked():
                choose_online_mode_menu.disable()
                hero_choose_menu.enable(1)
                mouse_click = False
            elif choose_online_mode_menu.hero_button_3.is_clicked():
                choose_online_mode_menu.disable()
                hero_choose_menu.enable(2)
                mouse_click = False
            # if choose_online_mode_menu.start_server.is_clicked():
            #     self.network = FlaskNetwork(choose_online_mode_menu.line_edit.get_text())
            #     self.current_player = self.network.getP()
            #     if self.current_player != "game is full" and self.current_player:
            #         choose_online_mode_menu.disable()
            #
            #         location = random.randrange(1, 56)
            #         self.online_location = location
            #
            #         self.final_round_over = True
            #         self.online_on = True
            #     else:
            #         print(self.current_player)
            #         print("cannot find a server")
            if choose_online_mode_menu.connect_button.is_clicked():
                self.network = Network()
                self.current_player = self.network.getP()
                self.online_name = choose_online_mode_menu.line_edit.get_text()
                if self.current_player:
                    choose_online_mode_menu.disable()

                    location = random.randrange(1, 56)
                    self.online_location = location

                    self.final_round_over = True
                    self.online_on = True
                else:
                    print("cannot find a server")

        if hero_choose_menu.is_enabled():
            hero_choose_menu.show(mouse_click, self.team[hero_choose_menu.get_pick()])
            if hero_choose_menu.super_pau.is_clicked():
                if not hero_choose_menu.super_pau.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.super_pau.get_p()
            elif hero_choose_menu.lisa.is_clicked():
                if not hero_choose_menu.lisa.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.lisa.get_p()
            elif hero_choose_menu.vesisa.is_clicked():
                if not hero_choose_menu.vesisa.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.vesisa.get_p()
            elif hero_choose_menu.tagir.is_clicked():
                if not hero_choose_menu.tagir.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.tagir.get_p()
            elif hero_choose_menu.artestro.is_clicked():
                if not hero_choose_menu.artestro.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.artestro.get_p()
            elif hero_choose_menu.aksenov.is_clicked():
                if not hero_choose_menu.aksenov.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.aksenov.get_p()
            elif hero_choose_menu.bulat.is_clicked():
                if not hero_choose_menu.bulat.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.bulat.get_p()
            elif hero_choose_menu.robot_woman.is_clicked():
                if not hero_choose_menu.robot_woman.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.robot_woman.get_p()
            elif hero_choose_menu.bt25t.is_clicked():
                if not hero_choose_menu.bt25t.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.bt25t.get_p()
            elif hero_choose_menu.egor.is_clicked():
                if not hero_choose_menu.egor.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.egor.get_p()
            elif hero_choose_menu.kingartema.is_clicked():
                if not hero_choose_menu.kingartema.get_p() in self.team:
                    self.team[hero_choose_menu.get_pick()] = hero_choose_menu.kingartema.get_p()

            if hero_choose_menu.exit_button.is_clicked():
                hero_choose_menu.disable()
                choose_online_mode_menu.enable(False)

        if choose_mode_menu.is_enabled():
            choose_mode_menu.show(mouse_click)
            if choose_mode_menu.exit_button.is_clicked():
                choose_mode_menu.disable()
                game_menu.enable()
            if choose_mode_menu.campain_button.is_clicked() and not self.GAME_PROGRESS > 54:
                self.main_campain_on = True
                self.final_round_over = True
                choose_mode_menu.disable()
            if choose_mode_menu.online_button.is_clicked():

                display.set_online_window()
                online_fighter.load_chara_online()
                self.online_player = online_fighter.super_pau
                self.team = [online_fighter.lisa, online_fighter.super_pau, online_fighter.tagir]
                choose_online_mode_menu = ChooseOnlineModeMenu(display.scr_w, display.scr_h, bg.online_menu,
                                                               music.main_menu, self.online_name)
                hero_choose_menu = ChooseHeroMenu(bg.hero_pick_menu)
                choose_online_mode_menu.enable()
                choose_mode_menu.disable()

        if game_menu.is_enabled():
            game_menu.show(mouse_click)
            if game_menu.exit_button.is_clicked():
                self.aplication_run = False
            if game_menu.start_button.is_clicked():
                game_menu.disable()
                choose_mode_menu.enable()
            if game_menu.options_button.is_clicked():
                game_menu.disable()
                options_menu.enable()

        if options_menu.is_enabled():
            options_menu.show(mouse_click)
            if options_menu.exit_button.is_clicked():
                options_menu.disable()
                settings.save()
                game_menu.enable()
            if options_menu.volume_button_plus.is_clicked():
                settings.change_music_volume(0.01)
            if options_menu.volume_button_minus.is_clicked():
                settings.change_music_volume(-0.01)
            if options_menu.normal_mode.is_clicked():
                settings.change_difficulty(1)
            if options_menu.easy_mode.is_clicked():
                settings.change_difficulty(0.5)

        if bg.briff_war.is_playing():
            bg.briff_war.draw()
            key = pygame.key.get_pressed()
            if key[pygame.K_c]:
                bg.briff_war.stop()
        elif bg.end_cutscene_1.is_playing():
            bg.end_cutscene_1.draw()
        elif self.playing_cutscene is True:
            self.playing_cutscene = False
            game_menu.enable()
            display.set_fps(60)

    def main_campain_game(self, key_click):
        self.check_game_progress(*pg[self.GAME_PROGRESS])
        self.dialog(texts[self.GAME_PROGRESS], key_click)
        # Временно
        match self.GAME_PROGRESS:
            case 0:
                self.fight_survival([fighter.super_pau, fighter.bt25t],
                                    [fighter.moiseev_security, fighter.moiseev_security],
                                    2, ["Super PAU", "Bt25t"], ["Training Bot", "Training Bot"])
            case 1:
                self.fight_survival([fighter.super_pau, fighter.bt25t],
                                    [fighter.moiseev_security, fighter.moiseev_security],
                                    2, ["Super PAU", "Bt25t"], ["Moiseev Security", "Moiseev Security"])
            case 2:
                self.fight_survival([fighter.super_pau, fighter.bt25t],
                                    [fighter.trio_enemy, fighter.trio_enemy],
                                    2, ["Super PAU", "Bt25t"], ["Trio", "Trio"])
            case 3:
                self.fight(fighter.bt25t, fighter.police, 2, "Bt25t", "Police")
            case 4:
                self.fight(fighter.bt25t, fighter.albinos, 3, "Bt25t", "Albina")
            case 5:
                self.fight(fighter.super_pau, fighter.bulat_enemy, 3, "Super PAU", "Bulat")
            case 6:
                self.fight(fighter.bulat, fighter.moiseev_security, 2, "Bulat", "Moiseev Security")
            case 7:
                self.fight_survival([fighter.super_pau, fighter.bt25t, fighter.bulat],
                                    [fighter.negrominator, fighter.negrominator, fighter.walker_enemy],
                                    3, ["Super PAU", "Bt25t", "Bulat"], ["negrominator", "negrominator", "Walker"])
            case 8:
                self.fight(fighter.aksenov, fighter.negrominator, 1, "Aksenov", "negrominator")
            case 9:
                self.fight(fighter.super_pau, fighter.tagir_enemy, 3, "Super PAU", "NightButterfly (Tagir)")
            case 10:
                self.fight_survival([fighter.super_pau, fighter.aksenov, fighter.bt25t, fighter.bulat],
                                    [fighter.tagir_enemy, fighter.tagir_enemy, fighter.egor_enemy, fighter.egor_enemy],
                                    4, ["Super PAU", "Aksenov", "Bt25t", "Bulat"],
                                    ["NightButterfly (Tagir)", "NightButterfly (Tagir)", "Egor", "Egor"])
            case 11:
                self.fight(fighter.super_pau, fighter.kingartema_enemy, 3, "Super PAU",
                           "Flying El. Dumpling (Kingartema)")
            case 12:
                self.fight_survival([fighter.super_pau, fighter.bt25t, fighter.aksenov, fighter.bulat],
                                    [fighter.tagir_enemy, fighter.egor_enemy, fighter.egor_enemy,
                                     fighter.kingartema_enemy],
                                    4, ["Super PAU", "Bt25t", "Aksenov", "Bulat"],
                                    ["NightButterfly (Tagir)", "Egor", "Egor",
                                     "Flying El. Dumpling (Kingartema)"])
            case 13:
                self.fight(fighter.super_pau, fighter.moiseev, 3, "Super PAU", "Moiseev")
            case 14:
                self.fight(fighter.trio, fighter.moiseev_bot, 3, "Trio", "Moiseev Bot")
            case 15:
                self.fight(fighter.super_pau, fighter.japan_soldier, 2, "Super PAU", "USA Soldier")
            case 16:
                self.fight(fighter.bt25t, fighter.soldier, 2, "Bt25t", "USA Soldier")
            case 17:
                self.fight(fighter.egor, fighter.moiseev_bot, 2, "Egor", "Moiseev Bot")
            case 18:
                self.fight_survival([fighter.super_pau, fighter.super_pau, fighter.super_pau, fighter.super_pau,
                                     fighter.super_pau, fighter.super_pau],
                                    [fighter.soldier, fighter.soldier, fighter.japan_soldier,
                                     fighter.japan_soldier, fighter.moiseev_bot, fighter.moiseev_bot],
                                    6, ["Super PAU", "Super PAU", "Super PAU", "Super PAU", "Super PAU", "Super PAU"],
                                    ["state mercenary", "state mercenary", "state mercenary",
                                     "state mercenary", "Moiseev Bot", "Moiseev Bot"])
            case 19:
                self.fight(fighter.bulat, fighter.moiseev_bot, 2, "Bulat", "Moiseev Bot")
            case 20:
                self.fight(fighter.super_pau, fighter.moiseev, 3, "Super PAU", "Moiseev")
            case 21:
                self.fight(fighter.super_pau, fighter.moiseev_security, 3, "Super PAU", "Bulat Security")
            case 22:
                self.fight_survival([fighter.super_pau, fighter.super_pau, fighter.super_pau, fighter.super_pau,
                                     fighter.super_pau, fighter.super_pau, fighter.super_pau, fighter.super_pau],
                                    [fighter.egor_enemy, fighter.egor_enemy, fighter.trio_enemy,
                                     fighter.trio_enemy, fighter.kingartema_enemy, fighter.kingartema_enemy,
                                     fighter.bt25t_enemy, fighter.bt25t_enemy],
                                    8, ["Super PAU", "Super PAU", "Super PAU", "Super PAU", "Super PAU", "Super PAU",
                                        "Super PAU", "Super PAU"],
                                    ["Egor", "Egor", "Trio",
                                     "Trio", "Flying El. Dumpling (Kingartema)", "Flying El. Dumpling (Kingartema)",
                                     "Bt25t", "Bt25t"])
            case 23:
                self.fight_survival([fighter.tagir, fighter.tagir, fighter.aksenov, fighter.aksenov],
                                    [fighter.egor_enemy, fighter.trio_enemy, fighter.bt25t_enemy,
                                     fighter.kingartema_enemy],
                                    4, ["NightButterfly (Tagir)", "NightButterfly (Tagir)", "Aksenov", "Aksenov"],
                                    ["Egor", "Trio", "Bt25t", "Flying El. Dumpling (Kingartema)"])
            case 24:
                self.fight_survival([fighter.bt25t, fighter.super_pau, fighter.bt25t, fighter.super_pau,
                                     fighter.super_pau, fighter.super_pau, fighter.bt25t, fighter.super_pau],
                                    [fighter.egor_enemy, fighter.egor_enemy, fighter.trio_enemy,
                                     fighter.trio_enemy, fighter.kingartema_enemy, fighter.kingartema_enemy,
                                     fighter.tagir_enemy, fighter.tagir_enemy],
                                    8, ["Bt25t", "Super PAU", "Bt25t", "Super PAU", "Super PAU", "Super PAU",
                                        "Bt25t", "Super PAU"],
                                    ["Egor", "Egor", "Trio",
                                     "Trio", "Flying El. Dumpling (Kingartema)", "Flying El. Dumpling (Kingartema)",
                                     "NightButterfly (Tagir)", "NightButterfly (Tagir)"])
            case 25:
                self.fight(fighter.super_pau, fighter.bulat_enemy, 4, 'Super PAU', "Bulat")
            case 26:
                self.fight(fighter.aksenov, fighter.soldier, 2, "Aksenov", "soldier"),
            case 27:
                self.fight(fighter.lisa, fighter.yacuji, 2, "Lisa", "YACUJI"),
            case 28:
                self.fight(fighter.lisa, fighter.police, 2, "Lisa", "Policeman"),
            case 29:
                self.fight(fighter.lisa, fighter.super_pau_boss, 3, 'Lisa', "???")
            case 30:
                self.fight(fighter.lisa, fighter.yacuji, 3, 'Lisa', "YACUJI")
            case 31:
                self.fight(fighter.vasisa, fighter.moiseev_bot, 3, 'Vasisa', "USA Bot")
            case 32:
                self.fight_survival([fighter.lisa, fighter.lisa], [fighter.police, fighter.japan_soldier], 2,
                                    ["Lisa", "Lisa"], ["Berkutci", "Berkutci"])
            case 33:
                self.fight(fighter.aksenov, fighter.yacuji, 2, 'Aksenov', "YACUJI")
            case 34:
                self.fight(fighter.lisa, fighter.artestro, 3, 'Lisa', "Artestro")
            case 35:
                self.fight(fighter.aksenov, fighter.japan_soldier, 2, 'Aksenov', "Lisa`s Soldier")
            case 36:
                self.fight(fighter.super_pau, fighter.lisa_boss, 2, "SuperPAU", "Lisa")
            case 37:
                self.fight(fighter.aksenov, fighter.lisa_boss, 3, "Aksenov", "Lisa")
            case 38:
                self.fight(fighter.aksenov, fighter.negrominator, 2, "Aksenov", "Negrominator")
            case 39:
                self.fight(fighter.aksenov, fighter.soldier, 2, "Aksenov", "survivor")
            case 40:
                self.fight_survival([fighter.aksenov, fighter.aksenov], [fighter.police, fighter.japan_soldier], 2,
                                    ["Aksenov", "Aksenov"], ["survivor", "survivor"])
            case 41:
                self.fight_survival([fighter.aksenov, fighter.aksenov, fighter.aksenov, fighter.aksenov],
                                    [fighter.negrominator, fighter.negrominator, fighter.walker_enemy,
                                     fighter.walker_enemy], 4,
                                    ["Aksenov", "Aksenov", "Aksenov", "Aksenov"], ["Negrominator", "Negrominator",
                                                                                   "Walker", "Walker"])
            case 42:
                self.fight(fighter.aksenov, fighter.general, 3, "Aksenov", "Army General")
            case 43:
                self.fight(fighter.aksenov, fighter.walker_enemy, 1, "Aksenov", "Walker")
            case 44:
                self.fight(fighter.aksenov, fighter.negrominator, 1, "Aksenov", "negrominator")
            case 45:
                self.fight_survival([fighter.tagir, fighter.aksenov, fighter.kingartema, fighter.bt25t, fighter.egor],
                            [fighter.negrominator, fighter.walker_enemy, fighter.walker_enemy, fighter.walker_enemy,
                             fighter.general], 5,
                            ["Tagir", "Aksenov", "kingartema", "Bt25t", "Egor"], ["Negrominator", "Walker",
                                                                                  "Walker", "Walker", "General"])
            case 46:
                self.fight(fighter.vasisa, fighter.robot_woman, 3, "Vasisa", "Robot_killer")
            case 47:
                self.fight_survival([fighter.trio, fighter.trio],
                                    [fighter.moiseev_bot, fighter.robot_woman], 2,
                                    ["Trio", "Trio"], ["USA Bot", "Robot_killer"])
            case 48:
                self.fight_survival([fighter.aksenov, fighter.tagir, fighter.bt25t],
                            [fighter.negrominator, fighter.negrominator, fighter.general], 3,
                            ["Aksenov", "Tagir", "Bt25t"], ["Negrominator", "Negrominator", "General"])
            case 49:
                self.fight(fighter.walker, fighter.negrominator, 2, "Walker Hacked", "Negrominator")
            case 50:
                self.fight_survival([fighter.kingartema, fighter.egor],
                                    [fighter.moiseev_bot, fighter.general], 2,
                                    ["kingartema", "Egor"], ["USA Bot", "General"])
            case 51:
                self.fight_survival([fighter.aksenov, fighter.aksenov, fighter.tagir, fighter.tagir,
                                     fighter.trio, fighter.trio, fighter.bt25t, fighter.bt25t],
                                    [fighter.moiseev_bot, fighter.negrominator, fighter.negrominator,
                                     fighter.robot_woman, fighter.walker_enemy, fighter.general, fighter.robot_woman,
                                     fighter.general], 8,
                                    ["Aksenov", "Aksenov", "Tagir", "Tagir", "Trio", "Trio", "Bt25t", "Bt25t"],
                                    ["USA Bot", "Negrominator", "Negrominator",
                                     "Robot_killer", "Walker", "General", "Robot_killer", "General"])
            case 52:
                self.fight(fighter.vasisa, fighter.supertank, 3, "Vasisa", "Stolberg")
            case 53:
                self.fight(fighter.bt25t, fighter.vasisa_enemy, 3, "Bt25t", "Vasisa")
            case 54:
                self.fight(fighter.bt_final_battle, fighter.super_pau_final_boss, 4, "Kamil", "Semen")

        all_sprites.update()
        all_sprites.draw(display.screen)
        bullet_sprites.update()

    def dialog(self, text, key_click):
        if self.final_round_over or self.is_dialogue:
            self.is_dialogue = True
            self.final_round_over = False
            sec = 1
            if self.post_fight_dial:
                sec = 0
            key = pygame.key.get_pressed()
            if self.is_dialogue and not key[pygame.K_c] and self.idx != len(text[sec]):
                try:
                    check_bg_instance(text[sec][self.idx][2])
                    if text[sec][self.idx][1] != '':
                        s = pygame.Surface((1920 * display.scr_w, 600 * display.scr_h),
                                           pygame.SRCALPHA)  # per-pixel alpha
                        s.fill((0, 0, 0, 128))  # notice the alpha value in the color
                        display.screen.blit(s, (0, 600 * display.scr_h))
                        # dialog_rect = pygame.Rect(0, 600 * display.scr_h, 1920 * display.scr_w, 600 * display.scr_h)
                        # pygame.draw.rect(display.screen, color.black, dialog_rect)
                        draw_text("SPACE         C - to skip", font, color.white, 100 * display.scr_w,
                                  1000 * display.scr_h)
                    if type(text[sec][self.idx][0]) == tuple:
                        scaled_dial = pygame.transform.scale(
                            pygame.image.load(text[sec][self.idx][0][0]).convert_alpha(),
                            (display.screen_width, display.screen_height))
                        display.screen.blit(scaled_dial, (500 * display.scr_w, 0 * display.scr_h))
                        # chara name
                        draw_text(text[sec][self.idx][0][1], font, color.black, 98 * display.scr_w,
                                  648 * display.scr_h)
                        draw_text(text[sec][self.idx][0][1], font, (250, 200, 0), 100 * display.scr_w,
                                  650 * display.scr_h)
                    elif type(text[sec][self.idx][0]) == str:
                        draw_text(text[sec][self.idx][0], font, color.black, 98 * display.scr_w,
                                  648 * display.scr_h)
                        draw_text(text[sec][self.idx][0], font, color.white, 100 * display.scr_w,
                                  650 * display.scr_h)
                except IndexError:
                    pass
                if type(text[sec][self.idx][1]) is str:
                    # draw text
                    draw_text(text[sec][self.idx][1], font, color.black, 98 * display.scr_w, 698 * display.scr_h)
                    draw_text(text[sec][self.idx][1], font, color.white, 100 * display.scr_w, 700 * display.scr_h)
                elif type(text[sec][self.idx][1]) is tuple:
                    for index, txt in enumerate(text[sec][self.idx][1]):
                        draw_text(txt, font, color.black, 98 * display.scr_w,
                                  (698 + 60 * index) * display.scr_h)
                        draw_text(txt, font, color.white, 100 * display.scr_w,
                                  (700 + 60 * index) * display.scr_h)
                if key[pygame.K_SPACE] and self.is_dialogue and key_click:
                    self.idx += 1
            else:
                self.is_dialogue = False
                self.idx = 0
                if self.post_fight_dial:
                    self.post_fight_dial = False
                    self.main_campain_on = False
                    if self.GAME_PROGRESS == 55:
                        bg.end_cutscene_1.play()
                        display.set_fps(24)
                        self.playing_cutscene = True
                    else:
                        game_menu.enable()
                self.intro_count = 4
                return

    def check_game_progress(self, background, mus):
        if self.final_round_over and not self.post_fight_dial:
            play_music_bg(mus)
        if not self.is_dialogue:
            check_bg_instance(background)

    def fight(self, fighter1, fighter2, rounds, f1_name, f2_name):
        if not self.is_dialogue:
            # show players stats
            draw_health_bar(fighter1.health, 20 * display.scr_w, 20 * display.scr_h)
            draw_health_bar(fighter2.health, 1100 * display.scr_w, 20 * display.scr_h)
            draw_text(f"{f1_name}: {str(self.score[0])} / {rounds}", font, color.black, 17 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{f2_name}: {str(self.score[1])} / {rounds}", font, color.black, 1097 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{f1_name}: {str(self.score[0])} / {rounds}", font, color.red, 20 * display.scr_w,
                      80 * display.scr_h)
            draw_text(f"{f2_name}: {str(self.score[1])} / {rounds}", font, color.red, 1100 * display.scr_w,
                      80 * display.scr_h)
            # update fighters
            fighter1.update()
            fighter2.update()

            # update countdown
            if self.intro_count <= 0:
                # move fighter
                fighter1.move(display.screen, fighter2, self.round_over)
                fighter2.move(display.screen, fighter1, self.round_over,
                              self.GAME_PROGRESS)
            elif self.is_dialogue:
                self.intro_count = 4
            else:
                # display count timer
                draw_text(str(self.intro_count), count_font, color.red, display.screen_width / 2 - 20 * display.scr_w,
                          10 * display.scr_h)
                # update count timer
                if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()
            self.final_round_over = False
            # draw fighters
            fighter2.draw(display.screen)
            fighter1.draw(display.screen)
            # check for player defeat
            if not self.round_over:
                if not fighter1.alive:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                if not fighter2.alive:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                all_sprites.empty()
                fighter2.round_over_move()
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    all_sprites.empty()
                    bullet_sprites.empty()
                    if self.score[0] >= rounds:
                        self.final_round_over = True
                        self.post_fight_dial = True
                        self.score = [0, 0]
                        self.GAME_PROGRESS += 1
                        update_gp(self.GAME_PROGRESS)
                    elif self.score[1] >= rounds:
                        self.score = [0, 0]
                        self.final_round_over = True
                        self.main_campain_on = False
                        game_menu.enable()
                    self.intro_count = 4
                    fighter1.reset_params()
                    fighter2.reset_params()

    def fight_survival(self, fighters1, fighters2, rounds, f1_names, f2_names):
        if not self.is_dialogue:
            fighter1 = fighters1[self.fighter_id]
            fighter2 = fighters2[self.fighter_id]
            # show players stats
            draw_health_bar(fighter1.health, 20 * display.scr_w, 20 * display.scr_h)
            draw_health_bar(fighter2.health, 1100 * display.scr_w, 20 * display.scr_h)
            draw_text(f"{f1_names[self.fighter_id]}: {str(self.score[0])} / {rounds}", font, color.black,
                      17 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{f1_names[self.fighter_id]}: {str(self.score[0])} / {rounds}", font, color.red,
                      20 * display.scr_w,
                      80 * display.scr_h)

            draw_text(f"{f2_names[self.fighter_id]}: {str(self.score[1])} / {rounds}", font, color.black,
                      1097 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{f2_names[self.fighter_id]}: {str(self.score[1])} / {rounds}", font, color.red,
                      1100 * display.scr_w, 80 * display.scr_h)
            # update fighters
            fighter1.update()
            fighter2.update()

            # update countdown
            if self.intro_count <= 0:
                # move fighter
                fighter1.move(display.screen, fighter2, self.round_over)
                fighter2.move(display.screen, fighter1, self.round_over, self.GAME_PROGRESS)
            else:
                # display count timer
                draw_text(str(self.intro_count), count_font, color.red, display.screen_width / 2 - 20 * display.scr_w,
                          10 * display.scr_h)
                # update count timer
                if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()
            self.final_round_over = False
            # draw fighters
            fighter2.draw(display.screen)
            fighter1.draw(display.screen)
            # check for player defeat
            if not self.round_over:
                if not fighter1.alive:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                if not fighter2.alive:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                fighter2.round_over_move()
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    all_sprites.empty()
                    bullet_sprites.empty()
                    fighter1.reset_params()
                    fighter2.reset_params()
                    self.fighter_id = self.score[0]
                    self.intro_count = 4
                    if self.score[1] >= rounds:
                        self.score = [0, 0]
                        self.fighter_id = 0
                        self.final_round_over = True
                        self.main_campain_on = False
                        game_menu.enable()
                    elif self.score[0] >= rounds:
                        self.final_round_over = True
                        self.post_fight_dial = True
                        self.score = [0, 0]
                        self.fighter_id = 0
                        self.GAME_PROGRESS += 1
                        update_gp(self.GAME_PROGRESS)
