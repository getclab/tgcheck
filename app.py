from program import get_all_balance

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import SendMessage, EditMessageText
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import BoundFilter
import os

from models import *


# Telegram
API_TOKEN = '5033305280:AAHetdlb6XxOuDpUzJ-e6TbZanCeykvdvVc'


bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    telegram_id = message.from_user.id
    try:
        with db:
            query = User.get_or_none(telegram_id=telegram_id)
            if query is None:
                User(telegram_id=telegram_id, balance=0).save()
    except:
        print('ошибка бази данных')
    await message.answer('Привет')


@dp.message_handler(content_types=['document'])
async def names(document: types.document):
    try:
        telegram_id = document.chat.id
        file_id = document.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, f'{telegram_id}.txt')

        with open(f'{telegram_id}.txt', 'r') as file:
            seeds = file.read().splitlines()
        balance_file, nft_file = get_all_balance(seeds, telegram_id)
        await document.reply_document(open(balance_file, 'rb'))
        await document.reply_document(open(nft_file, 'rb'))
        os.remove(f'{telegram_id}.txt')
        os.remove(balance_file)
        os.remove(nft_file)
    except:
        document.answer('Не удалось прочитать файл')


if __name__ == '__main__':
    with db:
        db.create_tables([User, Seed])
    executor.start_polling(dp, skip_updates=True)