import sqlite3


def update_gp(gp_value):
    gp = int(gp_value)
    con = sqlite3.connect("G_PROGRESS.sqlite")
    # Создание курсора
    cur = con.cursor()
    cur.execute(f"""UPDATE GP
                SET GAME_PROGRESS = {gp}""")
    con.commit()
    con.close()


def get_gp():
    con = sqlite3.connect("G_PROGRESS.sqlite")
    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение результатов
    result = cur.execute("""SELECT GAME_PROGRESS FROM GP""").fetchall()
    con.close()
    gp = int(result[0][0])
    return gp


def get_settings():
    con = sqlite3.connect("G_PROGRESS.sqlite")
    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение результатов
    music_volume = cur.execute("""SELECT music_volume FROM SETTINGS""").fetchall()
    difficulty = cur.execute("""SELECT difficulty FROM SETTINGS""").fetchall()
    con.close()
    mus = float(music_volume[0][0])
    dif = float(difficulty[0][0])
    return mus, dif


def save_settings(mus_vol, diffic):
    mus = float(mus_vol)
    dif = float(diffic)
    con = sqlite3.connect("G_PROGRESS.sqlite")
    # Создание курсора
    cur = con.cursor()
    cur.execute(f"""UPDATE SETTINGS
                    SET music_volume = {mus}""")
    cur.execute(f"""UPDATE SETTINGS
                        SET difficulty = {dif}""")
    con.commit()
    con.close()
