import os

import requests
from dotenv import load_dotenv

load_dotenv('../.env')


def get_weather(city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"""
                Погода в городе {city}:
                Температура: {data['main']['temp']}°C
                Ощущаемая температура: {data['main']['feels_like']}°C
                Описание (на английском): {data['weather'][0]['description']}
                Влажность: {data['main']['humidity']}%
                Скорость ветра: {data['wind']['speed']}м/с
                """
    else:
        return "Нет информации, проверьте название города."
