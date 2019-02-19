#!/usr/bin/env python3

import psutil
import util
import subprocess
import sys

def get_data():
    if not hasattr(psutil, "sensors_battery"):
        return sys.exit("platform not supported")
    battery = psutil.sensors_battery()
    precent = battery.percent
    minute, sec = divmod(battery.secsleft, 60)
    hour, minute = divmod(minute, 60)
    charging = False
    if hour < 0 or minute < 0 or sec < 0:
        hour *= -1 if hour < 0 else 1
        minute *= -1 if minute < 0 else 1
        sec *= -1 if sec < 0 else 1
        charging = True
    time = [hour, minute, sec]
    return precent, charging, time


def get_icon(percent, charging):
    if charging is True:
        return '\uf1e6'
    elif percent <= 20:
        return '\uf244'
    elif percent <= 40:
        return '\uf243'
    elif percent <= 60:
        return '\uf242'
    elif percent <= 80:
        return '\uf241'
    else:
        return '\uf240'


def main():
    percent, charging, time = get_data()
    if len(sys.argv) > 1 and sys.argv[1] == "--charging":
        if charging is True:
            print("Charging", end='')
        else:
            print("Discharging", end='')
        return
    elif len(sys.argv) > 1 and sys.argv[1] == "--notify":
        if percent <= 5:
            title = "\uf071 Battery Critical!"
            content = "\uf244 " + util.fmt_percent(percent)
            content += "\n\uf017 {:02}:{:02}:{:02}".format(time[0], time[1], time[2])
            subprocess.run(["notify-send", "--urgency=critical", title, content])
        elif percent <= 10:
            title = "\uf071 Battery Low!"
            content = "\uf243 " + util.fmt_percent(percent)
            content += "\n\uf017 {:02}:{:02}:{:02}".format(time[0], time[1], time[2])
            subprocess.run(["notify-send", "--urgency=critical", title, content])
        elif percent >= 90 and charging is True:
            title = "\uf071 Battery Full!"
            content = "\uf240 " + util.fmt_percent(percent)
            content += "\n\uf017 {:02}:{:02}:{:02}".format(time[0], time[1], time[2])
            subprocess.run(["notify-send", title, content])
        return
    data = {"percent": util.fmt_percent(percent),
            "bar": util.get_bar(percent),
            "icon": get_icon(percent, charging),
            "H": "{:02}".format(time[0]),
            "M": "{:02}".format(time[1]),
            "S": "{:02}".format(time[2])}
    util.fmt_print(data, sys.argv[1] if len(sys.argv) > 1 else "{icon} [{H}:{M}:{S}]{percent}%{bar}")


if __name__ == "__main__":
    main()

