import lib.Database as db


class Settings:
    def __init__(self):
        self.music_volume, self.sound_volume, self.difficulty = db.get_settings()

    def change_music_volume(self, amount):
        self.music_volume += amount

    def change_sound_volume(self, amount):
        self.sound_volume += amount

    def change_difficulty(self, number):
        self.difficulty = number

    def save(self):
        db.save_settings(self.music_volume, self.difficulty, self.sound_volume)

    def get_music_volume(self):
        return self.music_volume

    def get_difficulty(self):
        return self.difficulty

    def get_sound_volume(self):
        return self.sound_volume


settings = Settings()
