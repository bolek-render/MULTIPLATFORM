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
        self.record_time = None
        self.error = None
        self.name = f'M3U8.RecReader : {fn}'

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

        # PROCESS FINISHED
        else:
            self.last_line = self.last_line.decode('utf-8')
            self.penultimate_line = self.penultimate_line.decode('utf-8')
            # print(self.penultimate_line)
            # print(self.last_line)

            # RECORD FINISHED
            if 'time' in self.penultimate_line:
                _parts = self.penultimate_line.split()
                for _part in _parts:
                    if 'time' in _part:
                        self.record_time = _part.split('=')[1]

                t_parts = self.record_time.split(':')
                h = t_parts[0]
                m = t_parts[1]
                s = round(float(t_parts[2]))
                self.record_time = f'{h}:{m}:{s}'

            # ERROR 404
            if '404 Not Found' in self.last_line or '404 Not Found' in self.penultimate_line:
                self.error = '404 Not Found'

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
            .output(filename=self.fn, codec='copy', t='10')
            .overwrite_output()
        )

        self.process = self.process.run_async(pipe_stdin=True, pipe_stderr=True)

        rec_procs[self.fn] = self.process

        reader = ReadStderr(self.process, self.fn)
        reader.start()

        # self.process.communicate(str.encode("q"))
        # time.sleep(3)
        # self.process.terminate()
