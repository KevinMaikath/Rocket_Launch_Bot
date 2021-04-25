from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

from main.settings import env
from telegram_bot.models import ChatsCollection
from telegram_bot.video_service import getImageData, getVideoImageFrameUrl

import json


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

        chat_id = update.effective_chat.id
        chat = ChatsCollection.find_one({'chat_id': chat_id})
        if not chat:
            chat = {"chat_id": chat_id}
            image_data = getImageData()
            chat.update(image_data)

            response = ChatsCollection.insert_one(chat)
            # we want chat obj to be the same as fetched from collection
            chat["_id"] = response.inserted_id

        context.bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")

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
