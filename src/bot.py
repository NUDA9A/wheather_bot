import os
from datetime import datetime

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackContext, ApplicationBuilder
from telegram import Update
from database import log_command
from weather import get_weather


load_dotenv('../.env')

current_city = ""


async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    response = "Привет! Я тестовый погодный бот для BobrAi. Напиши /set_city <city> чтобы указать город."
    log_command(user_id, "/start", response, datetime.now())
    await update.message.reply_text(response)


async def set_city(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста укажи название города. Напиши: /set_city <city>")
        return
    current_city = ' '.join(context.args)
    response = (f"Отлично, теперь ты можешь использовать команду /weather, чтобы получить информацию о погоде в городе "
                f"{current_city}. " "Ты так же можешь поменять город: /set_city <city>")
    log_command(user_id, f"/set_city {current_city}", response, datetime.now())
    await update.message.reply_text(response)


async def weather(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    weather_info = get_weather(current_city)
    log_command(user_id, f"/weather {current_city}", weather_info, datetime.now())
    await update.message.reply_text(weather_info)


async def city(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    response = f"У тебя установлен город {current_city}. Ты можешь поменять его с помощью команды /set_city <city>."
    log_command(user_id, f"/city", response, datetime.now())
    await update.message.reply_text(response)


def run_bot():
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    application = ApplicationBuilder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("set_city", set_city))
    application.add_handler(CommandHandler("city", city))

    application.run_polling()
