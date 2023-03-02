from lib.Settings import settings
from pygame import mixer

mixer.init()

# Пути к звукам
woman_hurt = mixer.Sound(r"assets\audio\sounds\woman_hurt.wav")
woman_hurt_2 = mixer.Sound(r"assets\audio\sounds\woman_hurt2.wav")
woman_hurt_3 = mixer.Sound(r"assets\audio\sounds\woman_hurt1.wav")
human_hurt = mixer.Sound(r"assets\audio\sounds\human_hurt.wav")
human_hurt_2 = mixer.Sound(r"assets\audio\sounds\human_hurt1.wav")
human_hurt_3 = mixer.Sound(r"assets\audio\sounds\human_hurt2.wav")
boss_hurt = mixer.Sound(r"assets\audio\sounds\boss_hurt.wav")
boss_hurt_2 = mixer.Sound(r"assets\audio\sounds\boss_hurt1.wav")
bt_hurt = mixer.Sound(r"assets\audio\sounds\bt_hurt.mp3")
bt_hurt_2 = mixer.Sound(r"assets\audio\sounds\bt_hurt1.mp3")
woman_sound = [woman_hurt, woman_hurt_2, woman_hurt_3]
human_sound = [human_hurt, human_hurt_2, human_hurt_3]
boss_sound = [boss_hurt, boss_hurt_2]
bt_sound = [bt_hurt, bt_hurt_2]

# load sounds
explosion_1 = mixer.Sound(r"assets\audio\sounds\explosion\exp1.ogg")
explosion_2 = mixer.Sound(r"assets\audio\sounds\explosion\exp2.ogg")
explosion_3 = mixer.Sound(r"assets\audio\sounds\explosion\exp3.ogg")
explosion_sounds = [explosion_3, explosion_2, explosion_1]
# gaubica
gaubica_1 = mixer.Sound(r"assets\audio\sounds\explosion\gaubica1.ogg")
gaubica_2 = mixer.Sound(r"assets\audio\sounds\explosion\gaubica2.ogg")
gaubica_3 = mixer.Sound(r"assets\audio\sounds\explosion\gaubica3.ogg")
gaubica_sounds = [gaubica_3, gaubica_2, gaubica_1]

shield_on_sfx = mixer.Sound(r"assets\audio\sounds\shield_broke.wav")
shield_sfx = mixer.Sound(r"assets\audio\sounds\shield_on.wav")
shield_sounds = [shield_sfx, shield_on_sfx]

all_sounds = [woman_sound, human_sound, boss_sound, explosion_sounds, gaubica_sounds, shield_sounds]

for lst in all_sounds:
    for sound in lst:
        sound.set_volume(settings.get_music_volume())
