import sys

from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

from main.settings import env
from telegram_bot.models import ChatsCollection
from telegram_bot.video_service import getImageData


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

        try:
            image_data = getImageData()

            chat = ChatsCollection.find_one({'chat_id': chat_id})
            if not chat:
                chat = {"chat_id": chat_id}
                chat.update(image_data.__dict__)

                response = ChatsCollection.insert_one(chat)
                chat["_id"] = response.inserted_id
            else:
                chat.update(image_data.__dict__)
                ChatsCollection.update_one({'chat_id': chat_id}, {'$set': chat})

        except:
            context.bot.send_message(chat_id=chat_id,
                                     text="Oops! There has been an error. Please try again later")
        else:
            context.bot.send_message(chat_id=chat_id,
                                     text="Welcome! Can you help me guessing at which frame does the rocket launch?")

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
