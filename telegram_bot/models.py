from django.db import models

# Create your models here.
from main.settings import MONGO_CLIENT

ChatsCollection = MONGO_CLIENT.rocket_launch_bot.chats


class ImageData:

    def __init__(self, min_frame, max_frame, current_frame, current_image_url, times_bisected):
        self.min_frame = min_frame
        self.max_frame = max_frame
        self.current_frame = current_frame
        self.current_image_url = current_image_url
        self.times_bisected = times_bisected

    @staticmethod
    def create(video_url, max_frame):
        min_frame = 0
        current_frame = bisect(min_frame, max_frame)
        current_image_url = getVideoImageFrameUrl(video_url, current_frame)
        times_bisected = 1

        return ImageData(min_frame, max_frame, current_frame, current_image_url, times_bisected)


def getVideoImageFrameUrl(video_url, frame):
    video_url = video_url.replace(' ', '%20')

    if '?' in video_url:
        video_url = video_url.split('?')[0]

    if not video_url.endswith('/'):
        video_url += '/'

    return f"{video_url}frame/{frame}"


def bisect(min_frame, max_frame):
    return round((max_frame - min_frame) / 2)
