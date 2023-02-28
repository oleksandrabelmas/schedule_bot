from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from collect_data import get_classes


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Розпочати нагадування')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


class_number_kb = ReplyKeyboardMarkup(
    resize_keyboard=True
)
try:
    for k, v in get_classes().items():
        class_number_kb.insert(KeyboardButton(k))
except Exception as ex:
    print(ex)


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Припинити нагадування')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
                               )


admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Розпочати нагадування')
        ],
        [
            KeyboardButton('Змінити розклад')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
