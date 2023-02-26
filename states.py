from aiogram.dispatcher.filters.state import State, StatesGroup


class MyStates(StatesGroup):
    choose_class_letter = State()

    schedule = State()

    menu = State()

