from aiogram.dispatcher.filters.state import StatesGroup, State


class menu(StatesGroup):
    menu = State()


class log(StatesGroup):
    number = State()
    password = State()
    pin = State()
    confirm = State()