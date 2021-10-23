import locale

import aiohttp
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils import executor
from config import *
from utils import draw_image

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)
locale.setlocale(locale.LC_ALL, 'ru_RU')


@dp.message_handler(content_types=ContentType.LOCATION)
async def location(message):
    lat = message.location.latitude
    long = message.location.longitude
    lang = 'ru'
    units = 'metric'

    # get current weather
    async with aiohttp.ClientSession() as session:
        url = f'https://api.openweathermap.org/data/2.5/weather?units={units}&lang={lang}&lat={lat}&lon={long}&appid={OPENWEATHER_TOKEN}'
        async with session.get(url) as resp:
            cur_data = await resp.json()
            if cur_data['cod'] != 200:
                await message.answer(f"something wrong with your location")

    img = draw_image(cur_data)

    await message.answer_photo(img)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply("Hello! Please send me location to get weather forecast!")

if __name__ == "__main__":
    executor.start_polling(dp)
