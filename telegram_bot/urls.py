from django.urls import path

from telegram_bot.views import MessageReceiver

urlpatterns = [
    path('webhook', MessageReceiver.as_view())
]
