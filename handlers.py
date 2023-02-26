import json
import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from states import MyStates
from collect_data import get_data
from reply import *


SHEET_ID = '165FEfvPuH9CfYK0qLp1Xa6o35aTW7WKdOmy5eqEvmWw'
SHEET_NAME = 'Розклад 20.02.2023 по 24.02.2023'


async def class_num(message: types.Message, state: FSMContext):
    await message.answer(f'Привіт {message.from_user.first_name}, вибери номер класу', reply_markup=class_number_kb)
    await MyStates.choose_class_letter.set()


async def choose_class(message: types.Message, state: FSMContext):

    # створюємо клавіатуру тут бо єбу як зробить не тут
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    for n, l in get_classes().items():
        if message.text == n:
            for letter in l:
                kb.insert(KeyboardButton(letter))

    await message.answer('Вибери свій клас', reply_markup=kb)
    await MyStates.schedule.set()


async def schedule(message: types.Message, state: FSMContext):

    get_data(SHEET_ID, SHEET_NAME)

    with open('data.json', 'r') as f:
        schdl = json.load(f)

    user_message = '-'.join(message.text.split())
    print(user_message)
    class_numbers = []

    for class_number, class_schedule in schdl.items():
        class_numbers.append(class_number)

    if user_message in class_numbers:
        await message.answer('Тепер ви будете отримувати сповіщення про уроки', reply_markup=cancel)

        for class_number, class_schedule in schdl.items():

            if class_number == user_message:

                # день тижня зараз
                today_is = time.asctime().split()[0]

                for day, list_lessons in class_schedule.items():
                    if day == today_is:
                        while user_message != 'Припинити нагадування':

                            # час зараз у потрібному форматі
                            time_now = time.asctime().split()[3].split(':')
                            time_now.pop(2)
                            time_now = ':'.join(time_now)

                            # відправляю повідомлення
                            for lesson in list_lessons:
                                for lesson_time, lesson_name in lesson.items():
                                    if lesson_time == time_now:
                                        print(lesson_name, time_now)
                                        if lesson_name != '':
                                            await message.answer(lesson_name)
                                            time.sleep(60)

                            else:
                                await message.answer('OK')

    elif message.text == 'Припинити нагадування':
        await message.answer('OK')
        await MyStates.menu.set()

    else:
        await message.answer('чьооо, я не знаю такого класу, надішліть ще раз')


#async def menu(dp: Dispatcher, state: FSMContext):


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(class_num, commands=['start'], state='*')
    dp.register_message_handler(choose_class, state=MyStates.choose_class_letter)
    dp.register_message_handler(schedule, state=MyStates.schedule)
