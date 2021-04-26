import requests

from telegram_bot.models import ImageState

VIDEO_API_URL = 'https://framex-dev.wadrid.net/api/video'
VIDEO_NAME = 'Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c'


def getImageData():
    video_url = f"{VIDEO_API_URL}/{VIDEO_NAME}"
    try:
        video_api_response = requests.get(video_url)
    except requests.exceptions.RequestException:
        return

    if video_api_response.status_code != 200:
        return

    video_data = video_api_response.json()

    if not video_data["frames"]:
        return

    image_data = ImageState.create(video_url, video_data["frames"])
    return image_data
