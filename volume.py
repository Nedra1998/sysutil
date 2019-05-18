#!/usr/bin/end python3

import util
import subprocess
import re
import sys


def get_data():
    result = subprocess.run(["amixer", 'get', 'Master'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    vol = re.findall(r"\[([0-9]+)%\]|$", result)[0]
    mute = re.findall(r"\[(on|off)\]|$", result)[0]
    if mute == "off":
        mute = True
    else:
        mute = False
    vol = float(vol)
    return vol, mute


def get_icon(volume, mute):
    if mute is True:
        return '\uf466'
    elif volume <= 33.33:
        return '\uf026'
    elif volume <= 66.66:
        return '\uf027'
    else:
        return '\uf028'


def main():
    volume, mute = get_data()
    util.fmt_print({
        "percent": util.fmt_percent(volume, True),
        "mute": str(mute),
        "bar": util.get_bar(volume),
        "icon": get_icon(volume, mute)
    }, sys.argv[1] if len(sys.argv) > 1 else "{icon} {percent}% {bar}")


if __name__ == "__main__":
    main()

