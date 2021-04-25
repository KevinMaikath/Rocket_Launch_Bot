from django.apps import AppConfig

from telegram_bot.telegrambot import TelegramBot


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        TelegramBot.setup_bot()
