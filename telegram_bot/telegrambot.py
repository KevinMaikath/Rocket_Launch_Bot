import json
from queue import Queue
from threading import Thread

from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

from main.settings import env


class TelegramBot:
    bot = None
    dispatcher = None
    thread = None

    @staticmethod
    def start(update, context):
        print('_____________________________')
        print('START!')
        print('_____________________________')
        print(context)
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    @staticmethod
    def setup_bot():
        if TelegramBot.bot:
            return

        print('_____________________________________')
        print('SETUP')
        print('_____________________________________')

        TelegramBot.bot = Bot(env('TELEGRAM_BOT_TOKEN'))
        TelegramBot.dispatcher = Dispatcher(TelegramBot.bot, None, workers=0)

        # Handlers
        start_handler = CommandHandler('start', TelegramBot.start)
        TelegramBot.dispatcher.add_handler(start_handler)

    @staticmethod
    def register_update(request_data):
        update = Update.de_json(request_data, TelegramBot.bot)
        TelegramBot.dispatcher.process_update(update)
