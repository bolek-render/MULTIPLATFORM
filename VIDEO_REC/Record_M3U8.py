import time
import ffmpeg
from threading import Thread
from VIDEO_REC.globals import rec_procs


class ReadStderr(Thread):
    def __init__(self, process, fn):
        Thread.__init__(self)
        self.process = process
        self.fn = fn
        self.line = None
        self.last_line = None
        self.penultimate_line = None
        self.name = f'RecReader : {fn}'

    def run(self):
        self.line = self.process.stderr.readline()

        while self.line != b'':
            self.penultimate_line = self.last_line
            self.last_line = self.line
            try:
                self.line = self.process.stderr.readline()
            except ValueError:
                time.sleep(3)
                self.process.terminate()
                del rec_procs[self.fn]
                break

        else:
            # finished
            time.sleep(3)
            self.process.terminate()
            del rec_procs[self.fn]


class RecordM3U8:

    def __init__(self, url, fn):
        self.url = url
        self.fn = fn
        self.process = None

    def run(self):
        self.process = (
            ffmpeg
            .input(self.url)
            .output(filename=self.fn, codec='copy', t='15')
        )

        self.process = self.process.run_async(pipe_stdin=True, pipe_stderr=True)

        rec_procs[self.fn] = self.process

        reader = ReadStderr(self.process, self.fn)
        reader.start()

        # self.process.communicate(str.encode("q"))
        # time.sleep(3)
        # self.process.terminate()
