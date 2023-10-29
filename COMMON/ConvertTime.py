def convert_time(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    if hour == 0 and minutes == 0:
        return "%02ds" % sec
    elif hour == 0 and minutes > 0:
        return "%02dm%02ds" % (minutes, sec)
    else:
        return "%02dh%02dm%02ds" % (hour, minutes, sec)

