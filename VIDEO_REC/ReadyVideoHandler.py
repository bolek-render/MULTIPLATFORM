import asyncio
from threading import Thread
from TELEGRAM.SendVideo import send_video
# from TELEGRAM.globals import BOT
from VIDEO_REC.GetVideoData import get_video_data
from VIDEO_REC.Thumbnails import Thumbnails

# bot = BOT


class VideoHandler(Thread):
    def __init__(self, fn, video):
        Thread.__init__(self)
        self.fn = fn
        self.video = video
        self.name = f'VideoHandler : {fn}'

    def run(self):
        data = get_video_data(self.video)

        if data['size'] > 10485760:  # 10 MB MINIMUM TO SET THUMBNAILS ON TELEGRAM
            thumb = Thumbnails(self.video, data)
            thumb.run()
            thumbnails = thumb.thumbnails
            thumb = None        # clear memory
        else:
            thumbnails = None

        # print(asyncio.get_event_loop())

        send_video(self.fn, self.video, data, thumbnails)


