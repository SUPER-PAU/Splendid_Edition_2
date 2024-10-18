import random

import pygame

from lib import mixer
from lib.clock import Clock
from lib.display import display
from lib.drawer import draw_health_bar, draw_text, check_bg_instance
from lib.joystick import joystick, get_j
from lib.mixer import play_music_bg, play_music
from lib.dialogs import dialogs_texts
from lib.Menu import MainMenu, ChooseModeMenu, OptionsMenu, ChooseOnlineModeMenu, ChooseHeroMenu
import lib.Database as dbase
import constants.textures.sprites as sprite
from lib.Settings import settings

# Константы/переменные
import constants.textures.backgrounds as bg
import constants.audio.music as music
from constants.audio.effects import update_sounds, bulat_fight
import constants.colors as color
import constants.fonts.turok as fonts
import constants.textures.icons as layout
from constants.progress import pg

import lib.players_data.online_players as online_fighter
import lib.players as players

clocks = Clock()

# fonts
font, count_font, score_font = fonts.sys, fonts.bigger_sys, fonts.bigger_sys
# dialogs
texts = dialogs_texts()
# menus
game_menu = MainMenu(display.scr_w, display.scr_h, bg.main_menu)
options_menu = OptionsMenu(display.scr_w, display.scr_h, bg.options_menu)
choose_mode_menu = ChooseModeMenu(display.scr_w, display.scr_h, bg.game_menu_animated)
choose_online_mode_menu = ChooseOnlineModeMenu(bg.online_menu, music.main_menu)
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
        self.boss_rush_on = False
        self.online_on = False
        self.aplication_run = True
        self.playing_cutscene = True
        self.ROUND_OVER_COOLDOWN = 2000
        self.idx = 0
        self.round_over_time = 1
        self.fighter_id = 0
        self.GAME_PROGRESS = dbase.get_gp()
        self.BOSS_RUSH_PROGRESS = 4
        self.BOSS_RUSH_ADD = 0
        self.game_completed = dbase.get_game_complete()
        self.boss_rush_completed_H = dbase.get_bossr_H_complete()

        self.home_timer = 0

        self.online_players = (online_fighter.super_pau, online_fighter.lisa)
        print(self.online_players)
        self.online_location = None

    def online_fight(self):
        fighter1, fighter2 = self.online_players[0].player, self.online_players[1].player
        self.check_game_progress(*pg[self.online_location])
        # show players stats
        draw_health_bar(fighter1.health, 20 * display.scr_w, 20 * display.scr_h)
        draw_health_bar(fighter2.health, 1100 * display.scr_w, 20 * display.scr_h)
        draw_text(f"{fighter1}: {str(self.score[0])} / {3}", font, color.black, 17 * display.scr_w,
                  83 * display.scr_h)
        draw_text(f"{fighter2}: {str(self.score[1])} / {3}", font, color.black, 1097 * display.scr_w,
                  83 * display.scr_h)
        draw_text(f"{fighter1}: {str(self.score[0])} / {3}", font, color.red, 20 * display.scr_w,
                  80 * display.scr_h)
        draw_text(f"{fighter2}: {str(self.score[1])} / {3}", font, color.red, 1100 * display.scr_w,
                  80 * display.scr_h)

        draw_text(f"{fighter1.health}/{fighter1.base_health}", font, color.black, 797 * display.scr_w,
                  83 * display.scr_h)
        draw_text(f"{fighter2.health}/{fighter2.base_health}", font, color.black, 1797 * display.scr_w,
                  83 * display.scr_h)
        draw_text(f"{fighter1.health}/{fighter1.base_health}", font, color.red, 800 * display.scr_w,
                  80 * display.scr_h)
        draw_text(f"{fighter2.health}/{fighter2.base_health}", font, color.red, 1800 * display.scr_w,
                  80 * display.scr_h)

        # update fighters
        fighter1.update()
        fighter2.update()

        # update countdown
        if self.intro_count <= 0:
            # move fighter
            fighter1.move(fighter2, self.round_over)
            fighter2.move(fighter1, self.round_over,
                          self.GAME_PROGRESS, self.score[0])
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
            sprite.all_sprites.empty()
            fighter2.round_over_move()
            if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                self.round_over = False
                sprite.all_sprites.empty()
                sprite.bullet_sprites.empty()
                if self.score[0] >= 3:
                    self.final_round_over = True
                    self.score = [0, 0]
                    choose_mode_menu.enable()
                    play_music_bg(music.main_menu)
                elif self.score[1] >= 3:
                    self.score = [0, 0]
                    self.final_round_over = True
                    choose_mode_menu.enable()
                    play_music_bg(music.main_menu)
                self.intro_count = 4
                fighter1.reset_params()
                fighter2.reset_params()

        sprite.attack_group.update(fighter2, fighter1, 1)

        draw_text("YOU", fonts.online_font, (0, 0, 0), fighter1.rect.centerx - 30, 1010)
        draw_text("YOU", fonts.online_font, (255, 255, 255), fighter1.rect.centerx - 31, 1011)

        sprite.all_sprites.update()
        sprite.all_sprites.draw(display.screen)
        sprite.bullet_sprites.update(fighter2, 1)

    def game_navigation(self, key_click, mouse_click, joy_click):
        global choose_online_mode_menu, hero_choose_menu
        # navigate menu
        if self.main_campain_on:
            self.main_campain_game(key_click, joy_click)
            joy_click = False
        if self.boss_rush_on:
            self.boss_rush()
        if self.online_on:
            self.online_fight()
            joy_click = False

        if choose_online_mode_menu.is_enabled():
            choose_online_mode_menu.show(mouse_click, self.online_players, joy_click)
            joy_click = False
            if choose_online_mode_menu.exit_button.is_clicked():
                choose_online_mode_menu.disable()
                display.set_normal_window()
                game_menu.enable()
            if choose_online_mode_menu.connect_button.is_clicked():
                choose_online_mode_menu.disable()
                location = random.randrange(1, 56)
                self.online_location = location
                self.final_round_over = True
                self.online_on = True

        if choose_mode_menu.is_enabled():
            choose_mode_menu.show(mouse_click, joy_click, self.GAME_PROGRESS, self.game_completed)
            joy_click = False
            if choose_mode_menu.exit_button.is_clicked():
                choose_mode_menu.disable()
                game_menu.enable()
            if choose_mode_menu.gp_button_minus.is_clicked():
                if self.GAME_PROGRESS > 0:
                    self.GAME_PROGRESS -= 1
            if choose_mode_menu.gp_button_plus.is_clicked():
                if not self.GAME_PROGRESS + 1 > 54:
                    self.GAME_PROGRESS += 1
            if choose_mode_menu.campain_button.is_clicked() and not self.GAME_PROGRESS > 54:
                players.fighter_instances.reset_players_story(self.GAME_PROGRESS)
                self.main_campain_on = True
                self.final_round_over = True
                choose_mode_menu.disable()
            if choose_mode_menu.boss_rush_button.is_clicked():
                players.fighter_instances.reset_players_story(self.BOSS_RUSH_PROGRESS)
                self.boss_rush_on = True
                self.final_round_over = True
                choose_mode_menu.disable()
            if choose_mode_menu.online_button.is_clicked():
                online_fighter.load_chara_online()
                self.online_players = (online_fighter.super_pau, online_fighter.lisa)
                hero_choose_menu = ChooseHeroMenu(bg.hero_pick_menu)
                choose_online_mode_menu.enable()
                choose_mode_menu.disable()
            if choose_mode_menu.skins_button.is_clicked():
                choose_mode_menu.disable()
                hero_choose_menu.enable()
                mouse_click = False

        if game_menu.is_enabled():
            game_menu.show(mouse_click, joy_click)
            joy_click = False
            if game_menu.exit_button.is_clicked():
                self.aplication_run = False
            if game_menu.start_button.is_clicked():
                game_menu.disable()
                choose_mode_menu.enable()
            if game_menu.options_button.is_clicked():
                game_menu.disable()
                options_menu.enable()

        if options_menu.is_enabled():
            options_menu.show(mouse_click, joy_click)
            if options_menu.exit_button.is_clicked():
                update_sounds()
                options_menu.disable()
                settings.save()
                game_menu.enable()
            if options_menu.volume_button_plus.is_clicked():
                settings.change_music_volume(0.01)
                mixer.music.set_volume(settings.get_music_volume())
            if options_menu.volume_button_minus.is_clicked():
                settings.change_music_volume(-0.01)
                mixer.music.set_volume(settings.get_music_volume())
            if options_menu.sound_button_plus.is_clicked():
                settings.change_sound_volume(0.01)
            if options_menu.sound_button_minus.is_clicked():
                settings.change_sound_volume(-0.01)

            if options_menu.normal_mode.is_clicked():
                settings.change_difficulty(1)
            if options_menu.easy_mode.is_clicked():
                settings.change_difficulty(0.5)
            if options_menu.hard_mode.is_clicked():
                settings.change_difficulty(1.5)
                bulat_fight.play()

        if hero_choose_menu.is_enabled():
            hero_choose_menu.show(mouse_click, joy_click)
            if hero_choose_menu.super_pau_v1.is_clicked():
                hero_choose_menu.super_pau_v1.set_picked()
                hero_choose_menu.super_pau_v2.set_unpicked()
                players.change_pau_skin(sprite.super_pau_player)
            if self.boss_rush_completed_H == 1:
                if hero_choose_menu.super_pau_v2.is_clicked():
                    hero_choose_menu.super_pau_v2.set_picked()
                    hero_choose_menu.super_pau_v1.set_unpicked()
                    players.change_pau_skin(sprite.super_pau_player_v2)
            else:
                hero_choose_menu.super_pau_v2.show_locked_2_line()

            if hero_choose_menu.vesisa_v1.is_clicked():
                hero_choose_menu.vesisa_v1.set_picked()
                hero_choose_menu.vesisa_v2.set_unpicked()
                players.change_ves_skin(sprite.vesisa)
            if self.game_completed:
                if hero_choose_menu.vesisa_v2.is_clicked():
                    hero_choose_menu.vesisa_v2.set_picked()
                    hero_choose_menu.vesisa_v1.set_unpicked()
                    players.change_ves_skin(sprite.vesisa_v2)
            else:
                hero_choose_menu.vesisa_v2.show_locked()

            if hero_choose_menu.lisa_v1.is_clicked():
                hero_choose_menu.lisa_v1.set_picked()
                hero_choose_menu.lisa_v2.set_unpicked()
                players.change_lisa_skin(sprite.lisa)

            elif hero_choose_menu.lisa_v2.is_clicked():
                hero_choose_menu.lisa_v2.set_picked()
                hero_choose_menu.lisa_v1.set_unpicked()
                players.change_lisa_skin(sprite.lisa_player_v2)

            if hero_choose_menu.exit_button.is_clicked():
                hero_choose_menu.disable()
                choose_mode_menu.enable()

        if bg.briff_war.is_playing():
            bg.briff_war.draw()
            key = pygame.key.get_pressed()
            if key[pygame.K_c]:
                bg.briff_war.stop()
        elif bg.end_cutscene_1.is_playing():
            bg.end_cutscene_1.draw()
            key = pygame.key.get_pressed()
            if key[pygame.K_c]:
                bg.end_cutscene_1.stop()
        elif self.playing_cutscene is True:
            self.playing_cutscene = False
            game_menu.enable()
            play_music_bg(music.main_menu)
            display.set_fps(60)

    def boss_rush(self):
        self.check_game_progress(*pg[self.BOSS_RUSH_PROGRESS])
        match self.BOSS_RUSH_PROGRESS:
            case 4:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                                "Bt25t", "Albina")
                self.BOSS_RUSH_ADD = 7
            case 11:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                                "Super PAU", "Flying El. Dumpling (Kingartema)")
                self.BOSS_RUSH_ADD = 9
            case 20:
                if self.score[0] > 0 and players.fighter_instances.enemy_figters[0].dead:
                    fighter = players.fighter_instances.enemy_figters[1]
                    if not fighter.second_phase:
                        play_music_bg(music.shadow_lord)
                        fighter.second_phase = True
                        fighter.rect.x = players.fighter_instances.enemy_figters[0].rect.x
                else:
                    fighter = players.fighter_instances.enemy_figters[0]
                self.fight_boss(players.fighter_instances.player_fighters, fighter, 3, "Super PAU", "Moiseev")
                self.BOSS_RUSH_ADD = 5
            case 25:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                                'Super PAU', "Bulat")
                self.BOSS_RUSH_ADD = 9
            case 34:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                        'Lisa', "Artestro")
                self.BOSS_RUSH_ADD = 3
            case 37:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                                "Aksenov", "Lisa")
                self.BOSS_RUSH_ADD = 5
            case 42:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                                "Aksenov", "Army General")
                self.BOSS_RUSH_ADD = 10
            case 52:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                                "Vasisa", "Stolberg")
                self.BOSS_RUSH_ADD = 1
            case 53:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                                "Bt25t", "Vasisa")
                self.BOSS_RUSH_ADD = 1
            case 54:
                self.fight_boss(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                                "Kamil", "Semen")
        sprite.all_sprites.update()
        sprite.all_sprites.draw(display.screen)
        sprite.bullet_sprites.update()

    def main_campain_game(self, key_click, joy_click):
        self.check_game_progress(*pg[self.GAME_PROGRESS])
        self.dialog(texts[self.GAME_PROGRESS], key_click, joy_click)
        # Временно
        match self.GAME_PROGRESS:
            case 0:
                self.fight_survival(players.fighter_instances.player_fighters,
                                    players.fighter_instances.enemy_figters, 2, ["Super PAU", "Bt25t"],
                                    ["Training Bot", "Training Bot"])
            case 1:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    2, ["Super PAU", "Bt25t"],
                                    ["Moiseev Security", "Moiseev Security"])
            case 2:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    2, ["Super PAU", "Bt25t"], ["Trio", "Trio"])
            case 3:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Bt25t", "Police")
            case 4:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Bt25t", "Albina")
            case 5:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Super PAU", "Bulat")
            case 6:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Bulat", "Moiseev Security")
            case 7:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    3, ["Super PAU", "Bt25t", "Bulat"], ["negrominator", "negrominator", "Walker"])
            case 8:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 1,
                           "Aksenov", "negrominator")
            case 9:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Super PAU", "NightButterfly (Tagir)")
            case 10:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    4, ["Super PAU", "Aksenov", "Bt25t", "Bulat"],
                                    ["NightButterfly (Tagir)", "NightButterfly (Tagir)", "Egor", "Egor"])
            case 11:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                           "Super PAU", "Flying El. Dumpling (Kingartema)")
            case 12:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    4, ["Super PAU", "Bt25t", "Aksenov", "Bulat"],
                                    ["NightButterfly (Tagir)", "Egor", "Egor",
                                     "Flying El. Dumpling (Kingartema)"])
            case 13:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Super PAU", "Moiseev")
            case 14:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Trio", "Moiseev Bot")
            case 15:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Super PAU", "USA Soldier")
            case 16:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Bt25t", "USA Soldier")
            case 17:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Egor", "Moiseev Bot")
            case 18:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    6, ["Super PAU", "Super PAU", "Super PAU",
                                        "Super PAU", "Super PAU", "Super PAU"],
                                    ["state mercenary", "state mercenary", "state mercenary",
                                     "state mercenary", "Moiseev Bot", "Moiseev Bot"])
            case 19:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Bulat", "Moiseev Bot")
            case 20:
                if self.score[0] > 0 and players.fighter_instances.enemy_figters[0].dead:
                    fighter = players.fighter_instances.enemy_figters[1]
                    if not fighter.second_phase:
                        play_music_bg(music.shadow_lord)
                        fighter.second_phase = True
                        fighter.rect.x = players.fighter_instances.enemy_figters[0].rect.x
                else:
                    fighter = players.fighter_instances.enemy_figters[0]
                self.fight(players.fighter_instances.player_fighters, fighter, 3, "Super PAU", "Moiseev")
            case 21:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Super PAU", "Bulat Security")
            case 22:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    8, ["Super PAU", "Super PAU", "Super PAU",
                                        "Super PAU", "Super PAU", "Super PAU",
                                        "Super PAU", "Super PAU"],
                                    ["Egor", "Egor", "Trio", "Trio", "Flying El. Dumpling (Kingartema)",
                                     "Flying El. Dumpling (Kingartema)", "Bt25t", "Bt25t"])
            case 23:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    4, ["NightButterfly (Tagir)",
                                        "NightButterfly (Tagir)", "Aksenov",
                                        "Aksenov"],
                                    ["Egor", "Trio", "Bt25t", "Flying El. Dumpling (Kingartema)"])
            case 24:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    4, ["Super PAU", "Bt25t", "Super PAU", "Bt25t"],
                                    ["Egor", "Trio", "Flying El. Dumpling (Kingartema)", "NightButterfly (Tagir)"])
            case 25:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                           'Super PAU', "Bulat")
            case 26:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Aksenov", "soldier"),
            case 27:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Lisa", "YACUJI"),
            case 28:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Lisa", "Policeman"),
            case 29:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           'Lisa', "???")
            case 30:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           'Lisa', "YACUJI")
            case 31:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           'Vasisa', "USA Bot")
            case 32:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    2,
                                    ["Lisa", "Lisa"], ["Berkutci", "Berkutci"])
            case 33:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           'Aksenov', "YACUJI")
            case 34:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           'Lisa', "Artestro")
            case 35:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           'Aksenov', "Lisa`s Soldier")
            case 36:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "SuperPAU", "Lisa")
            case 37:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                           "Aksenov", "Lisa")
            case 38:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Aksenov", "Negrominator")
            case 39:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Aksenov", "survivor")
            case 40:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    2, ["Aksenov", "Aksenov"],
                                    ["survivor", "survivor"])
            case 41:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    4, ["Aksenov", "Aksenov", "Aksenov", "Aksenov"],
                                    ["Negrominator", "Negrominator", "Walker", "Walker"])
            case 42:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                           "Aksenov", "Army General")
            case 43:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 1,
                           "Aksenov", "Walker")
            case 44:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 1,
                           "Aksenov", "negrominator")
            case 45:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    5, ["Tagir", "Aksenov", "kingartema", "Bt25t",
                                        "Egor"],
                                    ["Negrominator", "Walker", "Walker", "Walker", "General"])
            case 46:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Vasisa", "Robot_killer")
            case 47:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    2, ["Trio", "Trio"],
                                    ["USA Bot", "Robot_killer"])
            case 48:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    3,
                                    ["Aksenov", "Tagir", "Bt25t"], ["Negrominator", "Negrominator", "General"])
            case 49:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 2,
                           "Walker Hacked", "Walker")
            case 50:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    2, ["kingartema", "Egor"],
                                    ["USA Bot", "General"])
            case 51:
                self.fight_survival(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters,
                                    8,
                                    ["Aksenov", "Aksenov", "Tagir", "Tagir", "Trio", "Trio", "Bt25t", "Bt25t"],
                                    ["USA Bot", "Negrominator", "Negrominator",
                                     "Robot_killer", "Walker", "General", "Robot_killer", "General"])
            case 52:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Vasisa", "Stolberg")
            case 53:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 3,
                           "Bt25t", "Vasisa")
            case 54:
                self.fight(players.fighter_instances.player_fighters, players.fighter_instances.enemy_figters, 4,
                           "Kamil", "Semen")

        sprite.all_sprites.update()
        sprite.all_sprites.draw(display.screen)
        sprite.bullet_sprites.update()

    def dialog(self, text, key_click, joy_click):
        if self.final_round_over or self.is_dialogue:
            self.is_dialogue = True
            self.final_round_over = False
            sec = 1
            if self.post_fight_dial:
                sec = 0
            key = pygame.key.get_pressed()
            if joystick.get_joystick():
                joybutton = joystick.main_joystick.get_button
            else:
                joybutton = get_j
            if self.is_dialogue and not key[pygame.K_c] and not joybutton(3) and self.idx != len(text[sec]):
                try:
                    check_bg_instance(text[sec][self.idx][2])
                    if text[sec][self.idx][1] != '':
                        s = pygame.Surface((1920 * display.scr_w, 600 * display.scr_h),
                                           pygame.SRCALPHA)  # per-pixel alpha
                        s.fill((0, 0, 0, 128))  # notice the alpha value in the color
                        display.screen.blit(s, (0, 600 * display.scr_h))
                        # dialog_rect = pygame.Rect(0, 600 * display.scr_h, 1920 * display.scr_w, 600 * display.scr_h)
                        # pygame.draw.rect(display.screen, color.black, dialog_rect)
                        if joystick.get_layout() == "mouse":
                            draw_text("SPACE         C - to skip", font, color.white, 100 * display.scr_w,
                                      1000 * display.scr_h)
                        else:
                            l_click_rect = pygame.rect.Rect((100 * display.scr_w, 1000 * display.scr_h,
                                                             50 * display.scr_w, 50 * display.scr_h))
                            r_click_rect = pygame.rect.Rect((240 * display.scr_w, 1000 * display.scr_h,
                                                             50 * display.scr_w, 50 * display.scr_h))
                            display.screen.blit(layout.button_X, (l_click_rect.x, l_click_rect.y))
                            display.screen.blit(layout.button_Triangle, (r_click_rect.x, r_click_rect.y))
                            draw_text(" - to skip", font, color.white, 300 * display.scr_w,
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
                if ((key[pygame.K_SPACE] and key_click) or (joybutton(0) and joy_click)) and self.is_dialogue:
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
                        self.game_completed = 1
                        dbase.update_game_complete(1)
                        self.playing_cutscene = True
                    else:
                        choose_mode_menu.enable()
                        play_music_bg(music.main_menu)
                self.intro_count = 4
                return

    def check_game_progress(self, background, mus):
        if self.final_round_over and not self.post_fight_dial:
            play_music_bg(mus)
        if not self.is_dialogue:
            check_bg_instance(background)

    def fight_boss(self, fighter1, fighter2, rounds, f1_name, f2_name):
        if not self.is_dialogue:
            key = pygame.key.get_pressed()
            if joystick.get_joystick():
                joybutton = joystick.main_joystick.get_button
            else:
                joybutton = get_j

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

            draw_text(f"{int(fighter1.health)}/{fighter1.base_health}", font, color.black, 697 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{int(fighter2.health)}/{fighter2.base_health}", font, color.black, 1777 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{int(fighter1.health)}/{fighter1.base_health}", font, color.red, 700 * display.scr_w,
                      80 * display.scr_h)
            draw_text(f"{int(fighter2.health)}/{fighter2.base_health}", font, color.red, 1780 * display.scr_w,
                      80 * display.scr_h)

            if key[pygame.K_ESCAPE] or joybutton(1):
                self.home_timer += 1
            else:
                self.home_timer = 0
            if self.home_timer > 0:
                display.screen.blit(layout.home_button_sprite, (layout.home_button_rect.x, layout.home_button_rect.y))
                pygame.draw.rect(display.screen, (200, 200, 255),
                                 (900 * display.scr_w, 20 * display.scr_h, self.home_timer * display.scr_w,
                                  15 * display.scr_h))

            # update fighters
            fighter1.update()
            fighter2.update()

            # update countdown
            if self.intro_count <= 0:
                # move fighter
                fighter1.move(fighter2, self.round_over, key)
                fighter2.move(fighter1, self.round_over,
                              self.BOSS_RUSH_PROGRESS, self.score[0])
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
            fighter2.draw()
            fighter1.draw(display.screen)
            # check for player defeat
            if not self.round_over and self.home_timer < 100:
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
                    sprite.all_sprites.empty()
                    sprite.bullet_sprites.empty()
                    if self.score[0] >= rounds:
                        self.final_round_over = True
                        self.score = [0, 0]
                        if self.BOSS_RUSH_PROGRESS == 54:
                            if settings.get_difficulty() == 1.5:
                                dbase.update_bossr_H_complete(1)
                                self.boss_rush_completed_H = 1
                            self.BOSS_RUSH_PROGRESS = 4
                            self.BOSS_RUSH_ADD = 0
                            self.boss_rush_on = False
                            game_menu.enable()
                            play_music_bg(music.main_menu)
                        else:
                            self.BOSS_RUSH_PROGRESS += self.BOSS_RUSH_ADD
                            players.fighter_instances.reset_players_story(self.BOSS_RUSH_PROGRESS)
                    elif self.score[1] >= rounds or self.home_timer >= 100:
                        self.score = [0, 0]
                        self.BOSS_RUSH_PROGRESS = 4
                        self.final_round_over = True
                        self.boss_rush_on = False
                        game_menu.enable()
                        play_music_bg(music.main_menu)
                    self.intro_count = 4
                    fighter1.reset_params()
                    fighter2.reset_params()

    def fight(self, fighter1, fighter2, rounds, f1_name, f2_name):
        if not self.is_dialogue:
            key = pygame.key.get_pressed()
            if joystick.get_joystick():
                joybutton = joystick.main_joystick.get_button
            else:
                joybutton = get_j

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

            draw_text(f"{int(fighter1.health)}/{fighter1.base_health}", font, color.black, 697 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{int(fighter2.health)}/{fighter2.base_health}", font, color.black, 1777 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{int(fighter1.health)}/{fighter1.base_health}", font, color.red, 700 * display.scr_w,
                      80 * display.scr_h)
            draw_text(f"{int(fighter2.health)}/{fighter2.base_health}", font, color.red, 1780 * display.scr_w,
                      80 * display.scr_h)

            if key[pygame.K_ESCAPE] or joybutton(1):
                self.home_timer += 1
            else:
                self.home_timer = 0
            if self.home_timer > 0:
                display.screen.blit(layout.home_button_sprite, (layout.home_button_rect.x, layout.home_button_rect.y))
                pygame.draw.rect(display.screen, (200, 200, 255),
                                 (900 * display.scr_w, 20 * display.scr_h, self.home_timer * display.scr_w,
                                  15 * display.scr_h))

            # update fighters
            fighter1.update()
            fighter2.update()

            # update countdown
            if self.intro_count <= 0:
                # move fighter
                fighter1.move(fighter2, self.round_over, key)
                fighter2.move(fighter1, self.round_over,
                              self.GAME_PROGRESS, self.score[0])
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
            fighter2.draw()
            fighter1.draw(display.screen)
            # check for player defeat
            if not self.round_over and self.home_timer < 100:
                if not fighter1.alive:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                if not fighter2.alive:
                    self.score[0] += 1
                    if self.score[0] >= rounds:
                        if self.GAME_PROGRESS == 25:
                            play_music(music.the_only_thing_i_know_end)
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                fighter2.round_over_move()
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    sprite.all_sprites.empty()
                    sprite.bullet_sprites.empty()
                    if self.score[0] >= rounds:
                        self.final_round_over = True
                        self.post_fight_dial = True
                        self.score = [0, 0]
                        self.GAME_PROGRESS += 1
                        players.fighter_instances.reset_players_story(self.GAME_PROGRESS)
                        dbase.update_gp(self.GAME_PROGRESS)
                    elif self.score[1] >= rounds or self.home_timer >= 100:
                        self.score = [0, 0]
                        self.final_round_over = True
                        self.main_campain_on = False
                        choose_mode_menu.enable()
                        play_music_bg(music.main_menu)
                    self.intro_count = 4
                    fighter1.reset_params()
                    fighter2.reset_params()

    def fight_survival(self, fighters1, fighters2, rounds, f1_names, f2_names):
        if not self.is_dialogue:
            key = pygame.key.get_pressed()
            if joystick.get_joystick():
                joybutton = joystick.main_joystick.get_button
            else:
                joybutton = get_j

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

            draw_text(f"{int(fighter1.health)}/{fighter1.base_health}", font, color.black, 697 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{int(fighter2.health)}/{fighter2.base_health}", font, color.black, 1777 * display.scr_w,
                      83 * display.scr_h)
            draw_text(f"{int(fighter1.health)}/{fighter1.base_health}", font, color.red, 700 * display.scr_w,
                      80 * display.scr_h)
            draw_text(f"{int(fighter2.health)}/{fighter2.base_health}", font, color.red, 1780 * display.scr_w,
                      80 * display.scr_h)

            if key[pygame.K_ESCAPE] or joybutton(1):
                self.home_timer += 1
            else:
                self.home_timer = 0
            if self.home_timer > 0:
                display.screen.blit(layout.home_button_sprite, (layout.home_button_rect.x, layout.home_button_rect.y))
                pygame.draw.rect(display.screen, (200, 200, 255),
                                 (900 * display.scr_w, 20 * display.scr_h, self.home_timer * display.scr_w,
                                  15 * display.scr_h))

            # update fighters
            fighter1.update()
            fighter2.update()

            # update countdown
            if self.intro_count <= 0:
                # move fighter
                fighter1.move(fighter2, self.round_over, key)
                fighter2.move(fighter1, self.round_over, self.GAME_PROGRESS, self.score[0])
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
            fighter2.draw()
            fighter1.draw(display.screen)
            # check for player defeat
            if not self.round_over and self.home_timer < 100:
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
                    sprite.all_sprites.empty()
                    sprite.bullet_sprites.empty()
                    fighter1.reset_params()
                    fighter2.reset_params()
                    self.fighter_id = self.score[0]
                    self.intro_count = 4
                    if self.score[1] >= rounds or self.home_timer >= 100:
                        self.score = [0, 0]
                        self.fighter_id = 0
                        self.final_round_over = True
                        self.main_campain_on = False
                        choose_mode_menu.enable()
                        play_music_bg(music.main_menu)
                    elif self.score[0] >= rounds:
                        self.final_round_over = True
                        self.post_fight_dial = True
                        self.score = [0, 0]
                        self.fighter_id = 0
                        self.GAME_PROGRESS += 1
                        players.fighter_instances.reset_players_story(self.GAME_PROGRESS)
                        dbase.update_gp(self.GAME_PROGRESS)
