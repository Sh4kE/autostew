def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], rem = divmod(rem, 60)
    d["seconds"], rem = divmod(rem, 1)
    d["milliseconds"] = int(tdelta.microseconds / 1000)
    return fmt.format(**d)


def std_time_format(tdelta):
    return strfdelta(tdelta, "{minutes}:{seconds}.{milliseconds}")