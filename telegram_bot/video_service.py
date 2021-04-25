import requests

from telegram_bot.models import ImageData

VIDEO_API_URL = 'https://framex-dev.wadrid.net/api/video'
VIDEO_NAME = 'Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c'


def getImageData():
    video_url = f"{VIDEO_API_URL}/{VIDEO_NAME}"
    video_api_response = requests.get(video_url)
    video_data = video_api_response.json()

    image_data = ImageData.create(video_url, video_data["frames"])
    return image_data
