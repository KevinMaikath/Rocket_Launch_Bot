import requests

VIDEO_API_URL = 'https://framex-dev.wadrid.net/api/video'
VIDEO_NAME = 'Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c'


def getImageData():
    video_url = f"{VIDEO_API_URL}/{VIDEO_NAME}"
    video_api_response = requests.get(video_url)
    video_data = video_api_response.json()

    min_frame = 0
    max_frame = video_data["frames"]
    current_frame = bisect(min_frame, max_frame)
    current_image_url = getVideoImageFrameUrl(video_url, current_frame)
    times_bisected = 1

    return {
        "min_frame": min_frame,
        "max_frame": max_frame,
        "current_frame": current_frame,
        "current_image_url": current_image_url,
        "times_bisected": times_bisected
    }


def getVideoImageFrameUrl(video_url, frame):
    if '?' in video_url:
        video_url = video_url.split('?')[0] + '/'

    return f"{video_url}frame/{frame}"


def bisect(min_frame, max_frame):
    return (max_frame - min_frame) / 2
