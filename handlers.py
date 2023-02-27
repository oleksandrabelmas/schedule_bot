import json
import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from states import MyStates
from collect_data import get_data
from reply import *
from bots_data import ADMIN_USER_LIST


# решаю как бидло через глобальную переменую
user_class_number = []


async def start_menu(message: types.Message, state: FSMContext):

    if str(message.from_user.id) in ADMIN_USER_LIST:
        await message.answer(f'Привіт {message.from_user.first_name}, це бот з нагадуваннями про уроки', reply_markup=admin_kb)
        await MyStates.admin.set()

    else:
        await message.answer(f'Привіт {message.from_user.first_name}, це бот з нагадуваннями про уроки', reply_markup=start_kb)
        print(message.from_user.id)
        await MyStates.choose_class_number.set()


############################################### Адмін частина ##########################################################
async def admin(message: types.Message, state: FSMContext):

    if message.text == 'Розпочати нагадування':
        await MyStates.choose_class_number.set()

    elif message.text == 'Змінити розклад':
        await MyStates.change_schedule.set()
        await message.answer('Надішли посилання на гугл таблицю')


async def change_schedule(message: types.Message, state: FSMContext):

    schedule_link = message.text
    print(schedule_link)
    get_data(schedule_link)

    if get_data(schedule_link) is False:
        await message.answer('Не моду отримати данні за посиланням')

    else:
        await message.answer('Розклад був успішно доданий')
########################################################################################################################


async def class_num(message: types.Message, state: FSMContext):
    await message.answer(f'Вибери номер класу', reply_markup=class_number_kb)
    await MyStates.choose_class_letter.set()


async def choose_class(message: types.Message, state: FSMContext):
    global user_class_number
    user_class_number.append(message.text)

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
    global user_class_number
    user_class_number += message.text

    user_class_number = '-'.join(user_class_number)

    try:
        with open('data.json', 'r') as f:
            schdl = json.load(f)

        class_numbers = []

        for class_number, class_schedule in schdl.items():
            class_numbers.append(class_number)

        await message.answer('Тепер ви будете отримувати сповіщення про уроки', reply_markup=cancel)

        for class_number, class_schedule in schdl.items():

            if class_number == user_class_number:

                # день тижня зараз
                today_is = time.asctime().split()[0]

                for day, list_lessons in class_schedule.items():

                    if day == today_is:
                        while message.text != 'Припинити нагадування':

                            # час зараз у потрібному форматі
                            time_now = time.asctime().split()[3].split(':')
                            time_now.pop(2)
                            time_now = ':'.join(time_now)

                            time.sleep(10)

                            # відправляю повідомлення
                            for lesson in list_lessons:
                                for lesson_time, lesson_name in lesson.items():

                                    if lesson_time == time_now:
                                        print(lesson_name, time_now)

                                        if lesson_name != '':
                                            await message.answer(lesson_name)
                                            time.sleep(60)

    except Exception as ex:
        print(ex)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands=['start'], state='*')
    dp.register_message_handler(admin, state=MyStates.admin)
    dp.register_message_handler(change_schedule, state=MyStates.change_schedule)
    dp.register_message_handler(class_num, state=MyStates.choose_class_number)
    dp.register_message_handler(choose_class, state=MyStates.choose_class_letter)
    dp.register_message_handler(schedule, state=MyStates.schedule)
