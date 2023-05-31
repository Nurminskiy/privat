from database import db
import string
import random


print(db.get_info_user(5620020863)[3])

#async def button_callback_handler(query: types.CallbackQuery, button_id: int):
    # Ваш код обработки нажатия кнопки
    # Отправка текста
    #await query.message.answer("Текст сообщения")

    # Проверка наличия следующей кнопки в базе данных
    #if button_id < len(buttons):
        #next_button = buttons[button_id]
    # Отправка следующей кнопки
        #await query.message.answer(next_button)
    #else:
    # Кнопки закончились, отправляем финальное сообщение
        #await query.message.answer("Финальное сообщение")

    # Обязательно отмечаем обработку CallbackQuery
    #await query.answer()

#@dp.callback_query_handler(lambda query: True)
#async def process_callback_query(query: types.CallbackQuery):
#button_id = int(query.data) # Получение идентификатора кнопки
#await button_callback_handler(query, button_id)


#inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
#for i, button in enumerate(buttons):
#inline_keyboard.add(types.InlineKeyboardButton(text=button, callback_data=str(i)))
