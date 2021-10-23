from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils import executor
from config import *

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=ContentType.LOCATION)
async def location(message):
    lat = message.location.latitude
    long = message.location.longitude
    await message.answer(f"latitude = {lat}\nlongitude = {long}")


@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply("Hello! Please send me location to get weather forecast!")

if __name__ == "__main__":
    executor.start_polling(dp)
