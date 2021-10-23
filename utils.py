import os
import textwrap
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

from config import *


def get_icon(code):
    icon_name = f'{code}@4x.png'
    icon_path = f'./icon/{icon_name}'
    if not os.path.exists(icon_path):
        with requests.get(f'http://openweathermap.org/img/wn/{icon_name}', stream=True) as response:
            result = BytesIO(response.raw.read())
            with open(icon_path, "wb") as f:
                f.write(result.getbuffer())
            return result

    with open(icon_path, 'rb') as fh:
        return BytesIO(fh.read())


def draw_image(cur_data, forecast_data):
    # define range (is needed to show today's forecast?)
    show_tommorow_forecast = int(cur_data['main']['temp']) == int(forecast_data['daily'][0]['temp']['day']) and \
                             cur_data['weather'][0]['description'] == forecast_data['daily'][0]['weather'][0][
                                 'description'] and \
                             int(cur_data['main']['humidity']) == int(forecast_data['daily'][0]['humidity']) and \
                             int(cur_data['wind']['speed']) == int(forecast_data['daily'][0]['wind_speed'])

    if show_tommorow_forecast:
        range_data = (1, 6)
    else:
        range_data = (0, 5)

    with Image.new(mode="RGBA", size=BACKGROUD_SIZE, color=BACKGROUD_COLOR) as img:
        font_60 = ImageFont.truetype(FONT_NAME, size=60)
        font_48 = ImageFont.truetype(FONT_NAME, size=48)
        font_36 = ImageFont.truetype(FONT_NAME, size=36)
        font_24 = ImageFont.truetype(FONT_NAME, size=24)
        draw = ImageDraw.Draw(img)
        x, y = BACKGROUD_SIZE

        # draw texts
        # current weather
        draw.text((x / 2, 50), cur_data['name'], anchor="mt", font=font_60, fill=FONT_COLOR)

        current_weather = f"{int(cur_data['main']['temp'])}°, {cur_data['weather'][0]['description']}\n" \
                          f"влажность {cur_data['main']['humidity']}%\n" \
                          f"ветер {round(cur_data['wind']['speed'])} м/с"
        cur_time = datetime.fromtimestamp(cur_data['dt'])
        current_time = f"на {cur_time.strftime('%H:%M')}\n{cur_time.strftime('%d %b. %Y').lower()}"

        draw.text((150 + 150 + 36, 250), current_weather, anchor="la", font=font_48, fill=FONT_COLOR)
        draw.text((1400, 250 + 36), current_time, anchor="la", align="center", font=font_48, fill=FONT_COLOR)
        draw.text((x / 2, 475), 'прогноз', anchor="mt", font=font_48, fill=FONT_COLOR)
        draw.text((x - 48, y - 48), 'данные предоставлены\nopenweathermap.org', anchor="rs", align="right",
                  font=font_24,
                  fill=FONT_COLOR)

        # draw icons
        with Image.open(get_icon(cur_data["weather"][0]["icon"])) as img_icon:
            img.paste(img_icon, (150, 250), img_icon)

        # forecast
        for i in range(range_data[0], range_data[1]):
            cur_x = i * 340 + 150
            if show_tommorow_forecast:
                cur_x -= 340
            cur_forecast = forecast_data['daily'][i]
            date = datetime.fromtimestamp(cur_forecast['dt'])
            current_time = date.strftime('%d %b.').lower()
            draw.text((cur_x, 570), current_time, anchor="la", align="center", font=font_48, fill=FONT_COLOR)

            current_desc = '\n'.join(textwrap.wrap(cur_forecast['weather'][0]['description'], width=10))
            forecast_text = f"{current_desc}\n" \
                            f"{int(cur_forecast['temp']['day'])}°, {cur_forecast['humidity']}%\n" \
                            f"{round(cur_forecast['wind_speed'])} м/с"
            draw.text((cur_x + 72, 770), forecast_text, anchor="ma", align="center", font=font_48, fill=FONT_COLOR)

        # icons
        for i in range(range_data[0], range_data[1]):
            cur_x = i * 340 + 120
            if show_tommorow_forecast:
                cur_x -= 340
            cur_forecast = forecast_data['daily'][i]
            with Image.open(get_icon(cur_forecast["weather"][0]["icon"])) as img_icon:
                img.paste(img_icon, (cur_x, 610), img_icon)

        result = BytesIO()
        result.name = 'image.png'
        img.save(result, 'PNG')
        result.seek(0)
        return result
