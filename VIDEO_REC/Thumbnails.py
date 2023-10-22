import io
import ffmpeg
from PIL import Image, UnidentifiedImageError


class Thumbnails:
    def __init__(self, video, data):
        self.video = video
        self.duration = data['duration']
        self.width = data['width']
        self.height = data['height']
        self.thumbnails = None

    def run(self):
        if self.duration >= 20:
            frame_step = int(self.duration / 16)
            frames = []
            thumbs = []

            for frame in range(int(frame_step / 2), self.duration + 1, frame_step):
                frames.append(frame)

            for frame in frames:

                out, err = (
                    ffmpeg
                    .input(self.video, ss=frame)
                    .output('pipe:', vframes=1, format='image2', vcodec='png', loglevel="quiet")
                    .global_args('-nostdin')
                    .run(capture_stdout=True)
                )

                thumbs.append(io.BytesIO(out))

            thumbnails = Image.new('RGB', (self.width * 4, self.height * 4))
            index = 0

            for x in range(0, self.height * 4, self.height):
                for y in range(0, self.width * 4, self.width):
                    try:
                        image = Image.open(thumbs[index])
                        thumbnails.paste(image, (y, x))
                    except UnidentifiedImageError:
                        pass

                    index += 1

            thumbs.clear()      # clear memory
            self.thumbnails = io.BytesIO()
            thumbnails.save(self.thumbnails, format='png')
