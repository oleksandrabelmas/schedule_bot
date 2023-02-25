from aiogram.dispatcher.filters.state import State, StatesGroup


class MyStates(StatesGroup):
    schedule = State()

    menu = State()

