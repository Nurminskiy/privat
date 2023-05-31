import Config
from InstanceBot import bot, dp
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import Keyboards
from database import db
from states import Admin
import random
import string


@dp.message_handler(commands=['adm'], state='*')
async def admin_menu(message: types.Message, state: FSMContext):
    if message.from_user.id == Config.admin_id:
        await state.finish()
        await bot.send_message(message.chat.id, f'Админ-меню', reply_markup=Keyboards.kb_admin)


async def choice(call: types.CallbackQuery):
    if call.data == 'add_butt':
        await bot.send_message(call.message.chat.id, 'Введите название кнопки')
        await Admin.add_butt.name.set()
    if call.data == 'del_butt':
        await bot.send_message(call.message.chat.id, f'Выберите кнопку для удаления\n\n'
                                                     f'{db.list_btns()}')
        await Admin.del_but.choice.set()
    if call.data == 'up_past':
        pass
    if call.data == 'set_butt_photo':
        await Admin.set_photo.confirm.set()
        await bot.send_message(call.message.chat.id, 'Включить фото в кнопках?', reply_markup=Keyboards.kb_confirm)
    if call.data == 'add_q':
        await Admin.add_quest.name.set()
        await bot.send_message(call.message.chat.id, 'Введите название нужного лога')
    if call.data == 'del_q':
        await Admin.del_q.choice.set()
        await bot.send_message(call.message.chat.id, f'Какой запрос удалить?\n\n'
                                                     f'{db.list_quest()}')


async def add_butt_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Admin.add_butt.text.set()
    await bot.send_message(message.chat.id, 'Введите текст кнопки')


async def add_butt_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await Admin.add_butt.photo.set()
    await bot.send_message(message.chat.id, 'Отправьте фото кнопки')


async def add_butt_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await Admin.add_butt.confirm.set()
    await bot.send_photo(message.chat.id, data['photo'], f"Название: {data['name']}\n\n"
                                                         f"Текст: {data['text']}\n\n"
                                                         f"Добавить кнопку?", reply_markup=Keyboards.kb_confirm)


async def add_butt_confirm(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data['name']
        text = data['text']
        photo = data['photo']
    if call.data == 'yes':
        try:
            db.add_butt(name, text, photo)
            await bot.send_message(call.message.chat.id, 'Кнопка успешно добавлена.')
            await state.finish()
        except:
            await bot.send_message(call.message.chat.id, 'Ошибка. Начни заново.')
            await state.finish()
    if call.data == 'no':
        await state.finish()
        await bot.send_message(call.message.chat.id, 'Создание кнопки отменено.')


async def del_butt(message: types.Message, state: FSMContext):
    db.del_butt(message.text)
    await bot.send_message(message.chat.id, 'Кнопка удалена')
    await state.finish()


async def set_photo_confirm(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        db.send_photo_on(1)
        await bot.send_message(call.message.chat.id, 'Фото в кнопках включено (Текст + Фото)')
        await state.finish()
    if call.data == 'no':
        db.send_photo_on(0)
        await bot.send_message(call.message.chat.id, 'Фото в кнопках выключено (Только текст)')
        await state.finish()


async def add_quest_name(message: types.Message, state: FSMContext):
    call_data = db.generate_random_string(5)
    async with state.proxy() as data:
        data['name'] = message.text
        data['call_data'] = call_data
    await Admin.add_quest.text.set()
    await bot.send_message(message.chat.id, 'Отправьте содержимое кнопки')


async def add_quest_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await Admin.add_quest.confirm.set()
    await bot.send_message(message.chat.id, f'Название: {data["name"]}\n'
                                            f'Дата: {data["call_data"]}\n'
                                            f'Содержимое: {data["text"]}\n\n'
                                            f'Добавить?', reply_markup=Keyboards.kb_confirm)


async def add_quest_confirm(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        async with state.proxy() as data:
            name_butt = data['name']
            call_data = data['call_data']
            text = data['text']
        db.add_quest(name_butt, call_data, text)
        await bot.send_message(call.message.chat.id, f'Запрос лога {name_butt} добавлен')
        await state.finish()
    if call.data == 'no':
        await bot.send_message(call.message.chat.id, f'Запрос лога отменен')
        await state.finish()


async def del_quest(message: types.Message, state: FSMContext):
    db.del_quest(message.text)
    await bot.send_message(message.chat.id, 'Запрос удален')
    await state.finish()


def add_hand_admin(dp: Dispatcher):
    dp.register_callback_query_handler(choice)
    dp.register_message_handler(add_butt_name, state=Admin.add_butt.name)
    dp.register_message_handler(add_butt_text, state=Admin.add_butt.text)
    dp.register_message_handler(add_butt_photo, content_types=['photo'], state=Admin.add_butt.photo)
    dp.register_callback_query_handler(add_butt_confirm, state=Admin.add_butt.confirm)
    dp.register_message_handler(del_butt, state=Admin.del_but.choice)
    dp.register_callback_query_handler(set_photo_confirm, state=Admin.set_photo.confirm)
    dp.register_message_handler(add_quest_name, state=Admin.add_quest.name)
    dp.register_message_handler(add_quest_text, state=Admin.add_quest.text)
    dp.register_callback_query_handler(add_quest_confirm, state=Admin.add_quest.confirm)
    dp.register_message_handler(del_quest, state=Admin.del_q.choice)


