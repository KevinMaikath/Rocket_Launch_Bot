import telegram.error
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from main.settings import env
from telegram_bot.models import ChatsCollection, ImageState
from telegram_bot.video_service import getImageData


class TelegramBot:
    bot = None
    dispatcher = None
    thread = None

    @staticmethod
    def setup_bot():
        if TelegramBot.bot is not None:
            return

        TelegramBot.bot = Bot(env('TELEGRAM_BOT_TOKEN'))
        TelegramBot.dispatcher = Dispatcher(TelegramBot.bot, None, workers=0)

        # Handlers
        start_handler = CommandHandler('start', startHandler)
        message_handler = MessageHandler(Filters.text & ~Filters.command, messageHandler)

        TelegramBot.dispatcher.add_handler(start_handler)
        TelegramBot.dispatcher.add_handler(message_handler)

    @staticmethod
    def register_update(request_data):
        update = Update.de_json(request_data, TelegramBot.bot)
        TelegramBot.dispatcher.process_update(update)


def startHandler(update, context):
    chat_id = update.effective_chat.id

    image_data = getImageData()
    if image_data is None:
        sendErrorMessage(context.bot, chat_id)
        return

    chat = ChatsCollection.find_one({'chat_id': chat_id})
    if not chat:
        chat = {'chat_id': chat_id, 'image_state': image_data.__dict__}

        response = ChatsCollection.insert_one(chat)
        chat['_id'] = response.inserted_id
    else:
        chat['image_state'].update(image_data.__dict__)
        ChatsCollection.update_one({'chat_id': chat_id}, {'$set': chat})

    context.bot.send_message(chat_id=chat_id,
                             text="Welcome! Can you help me guessing at which frame does the rocket launch?")

    askForRocketLaunch(context.bot, chat_id, chat['image_state']['current_image_url'])


def messageHandler(update, context):
    chat_id = update.effective_chat.id
    chat = ChatsCollection.find_one({'chat_id': chat_id})
    if not chat or chat['image_state']['times_bisected'] >= 16:
        context.bot.send_message(chat_id=chat_id, text="Write /start to start the game.")
        return

    text = update.message.text.lower()
    if text in ('yes', 'no'):
        has_rocket_launched = text == 'yes'
        image_state = ImageState(**chat['image_state'])
        image_state.getNextIteration(has_rocket_launched)
        chat['image_state'] = image_state.__dict__
        ChatsCollection.update_one({'chat_id': chat_id}, {'$set': chat})

        if image_state.times_bisected < 16:
            askForRocketLaunch(context.bot, chat_id, image_state.current_image_url)
        else:
            sendAnswer(context.bot, chat_id, image_state.current_frame)

    else:
        context.bot.send_message(chat_id=chat_id, text='Please answer yes or no.')


# Send an image while asking if the rocket has launched yet
def askForRocketLaunch(bot, chat_id, photo_url):
    try:
        bot.send_photo(chat_id=chat_id, photo=photo_url, caption="Did the rocket launch yet? (yes / no)")
    except telegram.error.BadRequest:
        bot.send_message(chat_id=chat_id, text="Unable to send the image. Please try again or restart the game.")


def sendAnswer(bot, chat_id, final_frame):
    bot.send_message(chat_id=chat_id, text=f"Finished! The rocket launches at frame: {final_frame}")


def sendErrorMessage(bot, chat_id):
    text = "Oops! There has been an error. Please try again later or restart the game with /start."
    bot.send_message(
        chat_id=chat_id,
        text=text
    )
