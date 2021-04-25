from django.db import models

# Create your models here.
from main.settings import MONGO_CLIENT

ChatsCollection = MONGO_CLIENT.rocket_launch_bot.chats
