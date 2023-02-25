from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


BOT_TOKEN = '6129157427:AAFoVBNlT8sjIx5LjkFXpla4fzByGnpIeQk'


storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
