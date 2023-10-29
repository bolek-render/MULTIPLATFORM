import os
import time
import ffmpeg
import DATA.globals as cg
from VIDEO_REC.globals import rec_procs


def record_m3u8(url, path, fn):
    if not os.path.isdir(path):
        os.makedirs(path)

    video = f'{path}{cg.SS}{fn}'

    process = (
        ffmpeg
        .input(url)
        .output(filename=video, codec='copy', t='20')
        .overwrite_output()
    )

    process = process.run_async(pipe_stdin=True, pipe_stderr=True)

    rec_procs[fn] = process

    line = process.stderr.readline()
    last_line = None
    penultimate_line = None

    while line != b'':
        penultimate_line = last_line
        last_line = line
        try:
            line = process.stderr.readline()
        except ValueError:
            time.sleep(3)
            process.terminate()
            del rec_procs[fn]
            break

    # PROCESS FINISHED
    try:
        last_line = last_line.decode('utf-8')
        penultimate_line = penultimate_line.decode('utf-8')
    except AttributeError:
        pass

    time.sleep(3)
    process.terminate()
    del rec_procs[fn]

    # print(penultimate_line)
    # print(last_line)

    # RECORD FINISHED
    try:
        if 'time' in last_line or 'time' in penultimate_line:
            return True, video

        # ERROR 404
        if '404 Not Found' in last_line or '404 Not Found' in penultimate_line:
            return False, '404 Not Found'

    except TypeError:
        return False, 'Error reading lines in ffmpeg recording'

    return False, 'Unknown error'

# process.communicate(str.encode("q"))
# time.sleep(3)
# process.terminate()