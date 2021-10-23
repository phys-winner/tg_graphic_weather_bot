import asyncio
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

    async def obtain_data(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.ok:
                    return await resp.json()
                await message.answer(f"something wrong with your location")

    cur_url = f'https://api.openweathermap.org/data/2.5/weather?units={units}&lang={lang}&lat={lat}&lon={long}&appid={OPENWEATHER_TOKEN}'
    forecast_url = f'https://api.openweathermap.org/data/2.5/onecall?units={units}&lang={lang}&lat={lat}&lon={long}&exclude=current,minutely,hourly,alerts&appid={OPENWEATHER_TOKEN}'

    cur_data, forecast_data = await asyncio.gather(
        obtain_data(cur_url),
        obtain_data(forecast_url)
    )
    img = draw_image(cur_data, forecast_data)

    await message.answer_photo(img)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply("Hello! Please send me location to get weather forecast!")


if __name__ == "__main__":
    executor.start_polling(dp)
