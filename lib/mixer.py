from pygame import mixer
from lib.Settings import settings

mixer.init()

# Класс саунда и музыка миксера
music = mixer.music
sound = mixer.Sound


# Воспроизводство фоновой музыки
def play_music_bg(music_bg):
    music.stop()
    music.load(music_bg)
    music.set_volume(settings.get_music_volume())
    music.play(-1)

def play_music(music_bg):
    music.stop()
    music.load(music_bg)
    music.set_volume(settings.get_music_volume())
    music.play()
# def set_volume_sfx():
#     # Изменение громкости звуков
#     sfx.woman_hurt_2.set_volume(SOUND_VOLUME)
#     sfx.woman_hurt_3.set_volume(SOUND_VOLUME)
#     sfx.woman_hurt.set_volume(SOUND_VOLUME)
#
#     sfx.human_hurt.set_volume(SOUND_VOLUME)
#     sfx.danil_vin.set_volume(SOUND_VOLUME)
