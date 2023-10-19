import time

import ffmpeg


class RecordM3U8:

    def __init__(self, url, fn):
        self.process = (
            ffmpeg
            .input(url)
            .output(filename=fn, codec='copy', t='20')
        )

    async def run(self):

        self.process = self.process.run_async(pipe_stdin=True, pipe_stderr=True)
