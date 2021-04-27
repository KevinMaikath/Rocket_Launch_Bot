from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_bot.telegrambot import TelegramBot


class MessageReceiver(APIView):
    def post(self, request):
        TelegramBot.register_update(request.data)
        return Response({'message': 'OK', 'request': request.data}, status.HTTP_200_OK)
