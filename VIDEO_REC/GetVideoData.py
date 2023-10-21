import os
import ffmpeg


def get_video_data(fn):
    size = os.path.getsize(fn)
    probe = ffmpeg.probe(fn)
    duration = round(float(probe['streams'][0]['duration']))
    width = probe['streams'][0]['width']
    height = probe['streams'][0]['height']

    data = {'size': size,
            'duration': duration,
            'width': width,
            'height': height}

    return data
