from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonRequestUser
from collect_data import get_classes


class_number_kb = ReplyKeyboardMarkup(
    resize_keyboard=True
)
for k, v in get_classes().items():
    class_number_kb.insert(KeyboardButton(k))


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Припинити нагадування')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
                               )


