from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonRequestUser


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Припинити нагадування')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
                               )


