#!/usr/bin/env python3

import psutil
import util
import sys


def get_data():
    mem = psutil.virtual_memory()
    return mem.percent, mem.available, mem.used


def get_size(byte, sufix):
    if sufix == 'KB':
        return "{:.2f}".format(byte / 1e3)
    elif sufix == 'MB':
        return "{:.2f}".format(byte / 1e6)
    elif sufix == 'GB':
        return "{:.2f}".format(byte / 1e9)
    elif sufix == 'TB':
        return "{:.2f}".format(byte / 1e12)


def main():
    percent, total, used = get_data()
    util.fmt_print({
        "percent": util.fmt_percent(percent),
        "bar": util.get_bar(percent, True),
        "totalKB": get_size(total, 'KB'),
        "usedKB": get_size(used, 'KB'),
        "totalMB": get_size(total, 'MB'),
        "usedMB": get_size(used, 'MB'),
        "totalGB": get_size(total, 'GB'),
        "usedGB": get_size(used, 'GB'),
        "totalTB": get_size(total, 'TB'),
        "usedTB": get_size(used, 'TB'),
        "icon": "\uf85a"
    }, sys.argv[1] if len(sys.argv) > 1 else "{icon} {percent}% {bar}")


if __name__ == "__main__":
    main()
