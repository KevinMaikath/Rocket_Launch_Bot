from django.db import models

# Create your models here.
from main.settings import MONGO_CLIENT

ChatsCollection = MONGO_CLIENT.rocket_launch_bot.chats


class ImageState:

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

        return ImageState(min_frame, max_frame, current_frame, current_image_url, times_bisected)

    def getNextIteration(self, has_rocket_launched):
        if has_rocket_launched:
            self.max_frame = self.current_frame
            self.bisectFrame()
            # self.current_frame = bisect(self.min_frame, self.current_frame)
        else:
            self.min_frame = self.current_frame
            self.bisectFrame()
            # self.current_frame = bisect(self.current_frame, self.max_frame)

        self.current_image_url = changeVideoImageFrameUrl(self.current_image_url, self.current_frame)
        self.times_bisected += 1

    def bisectFrame(self):
        self.current_frame = bisect(self.min_frame, self.max_frame)


def getVideoImageFrameUrl(video_url, frame):
    video_url = video_url.replace(' ', '%20')

    if '?' in video_url:
        video_url = video_url.split('?')[0]

    if not video_url.endswith('/'):
        video_url += '/'

    return f"{video_url}frame/{frame}"


def changeVideoImageFrameUrl(prev_image_url, next_frame):
    split = prev_image_url.split('/')
    split[-1] = f'{next_frame}'
    image_url = '/'.join(split)
    return image_url


def bisect(min_frame, max_frame):
    return round((max_frame + min_frame) / 2)
