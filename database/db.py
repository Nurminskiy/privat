import random
import sqlite3
import string


def generate_random_string(length):
    rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return rand_string


def check_db():
    db = sqlite3.connect('db.db', check_same_thread=False)
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM buttons')
        print('Кнопки запущены')
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE IF NOT EXISTS buttons (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name_butt TEXT,
                          text_butt TEXT,
                          photo_butt TEXT)''')
        db.commit()
    try:
        cursor.execute('SELECT * FROM inline_butt')
        print('Вопросы запущены')
    except:
        cursor.execute('''CREATE TABLE IF NOT EXISTS inline_butt (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name_butt TEXT,
                          call_data TEXT,
                          text TEXT)''')
    try:
        cursor.execute('SELECT * FROM setting')
        print('Настройки запущены')
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE IF NOT EXISTS setting (
                          photo INTEGER)''')
        cursor.execute('INSERT INTO setting (photo) VALUES (1)')
        db.commit()
    try:
        cursor.execute('SELECT * FROM users')
        print('Юзеры запущены')
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER,
                          username TEXT,
                          ref_id INTEGER,
                          ban INTEGER)''')
        db.commit()
    try:
        cursor.execute('SELECT * FROM past')
        print('Пасты запущены')
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE IF NOT EXISTS past (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          past1 TEXT,
                          past2 TEXT,
                          past3 TEXT,
                          past4 TEXT,
                          past5 TEXT)''')
        db.commit()


def add_user(user_id, username, ref_id, ban):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    if not cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone():
        cursor.execute('INSERT INTO users (user_id, username, ref_id, ban) VALUES (?, ?, ?, ?)', (user_id, username, ref_id, ban))
        db.commit()


def ban_user(user_id):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('UPDATE users SET ban = 1 WHERE user_id = ?', (user_id,))
    db.commit()


def unban_user(user_id):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('UPDATE users SET ban = 0 WHERE user_id = ?', (user_id,))
    db.commit()


def get_info_user(user_id):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchall()
    return row[0]


def user_exist(user_id):
    db = sqlite3.connect('db.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute('''SELECT user_id FROM users WHERE user_id = ?''', (user_id,))
    if cursor.fetchone() is None:
        return False
    else:
        return True


def send_photo_on(value):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('UPDATE setting SET photo = ?', (value,))
    db.commit()


def get_setting():
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM setting')
    row = cursor.fetchall()
    return row


def add_quest(name_butt, call_data, text):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('INSERT INTO inline_butt (name_butt, call_data, text) VALUES (?, ?, ?)', (name_butt, call_data, text,))
    db.commit()


def del_quest(value):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    list_btn = get_quest()

    name = list_btn[int(value)][1]

    cursor.execute(f'DELETE FROM inline_butt WHERE name_butt = ?', (name,))
    db.commit()


def list_quest():
    list_btn = get_quest()
    msg = ''
    for i in range(len(list_btn)):
        msg += f'№ {i} | {list_btn[i][1]}\n'
    return msg


def hand_quest():
    base = get_quest()
    btn_list = []
    for i in base:
        btn_list.append(i[2])
    return btn_list


def get_hand_quest(call_data):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM inline_butt WHERE call_data = ?', (call_data,))
    row = cursor.fetchone()
    return row


def get_quest():
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM inline_butt')
    row = cursor.fetchall()
    return row


def add_butt(name, text, photo):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('INSERT INTO buttons (name_butt, text_butt, photo_butt) VALUES (?, ?, ?)', (name, text, photo,))
    db.commit()


def del_butt(value):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    list_btn = get_butt()

    name = list_btn[int(value)][1]

    cursor.execute(f'DELETE FROM buttons WHERE name_butt = ?', (name,))
    db.commit()


def list_btns():
    list_btn = get_butt()
    msg = ''
    for i in range(len(list_btn)):
        msg += f'№ {i} | {list_btn[i][1]}\n'
    return msg


def get_butt():
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM buttons')
    row = cursor.fetchall()
    return row


def hand_butt():
    base = get_butt()
    btn_list = []
    for i in base:
        btn_list.append(i[1])
    return btn_list


def get_hand_butt(name):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM buttons WHERE name_butt = ?', (name,))
    row = cursor.fetchone()
    return row


def update_past(past1, past2, past3, past4, past5):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('UPDATE past SET past1 = ?', (past1,))
    cursor.execute('UPDATE past SET past2 = ?', (past2,))
    cursor.execute('UPDATE past SET past3 = ?', (past3,))
    cursor.execute('UPDATE past SET past4 = ?', (past4,))
    cursor.execute('UPDATE past SET past5 = ?', (past5,))
    db.commit()


def get_past():
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM past')
    row = cursor.fetchall()
    return row
