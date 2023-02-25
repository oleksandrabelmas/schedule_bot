from aiogram import executor

from bot import dp

import handlers


handlers.register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
