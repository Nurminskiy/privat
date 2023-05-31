from aiogram.dispatcher.filters.state import StatesGroup, State


class add_butt(StatesGroup):
    name = State()
    text = State()
    photo = State()
    confirm = State()


class del_but(StatesGroup):
    choice = State()


class add_quest(StatesGroup):
    name = State()
    text = State()
    confirm = State()


class del_q(StatesGroup):
    choice = State()


class set_photo(StatesGroup):
    confirm = State()


class past(StatesGroup):
    past1 = State()
    past2 = State()
    past3 = State()
    past4 = State()
    past5 = State()
    confirm = State()