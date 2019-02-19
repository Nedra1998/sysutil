#!/usr/bin/env python3

import psutil
import util
import sys


def get_data():
    cpus = psutil.cpu_percent(interval=5, percpu=True)
    percent = sum(cpus)
    percent /= len(cpus)
    return percent, cpus


def main():
    percent, cpu = get_data()
    data = {
        "percent": util.fmt_percent(percent),
        "bar": util.get_bar(percent),
        "icon": "\ufb19"
    }
    for i, core in enumerate(cpu):
        data["cpu" + str(i) + ""] = util.fmt_percent(core)
        data["bar" + str(i) + ""] = util.get_bar(core, minmum=True)
    util.fmt_print(data, sys.argv[1] if len(sys.argv) > 1 else "{icon} {percent}% " +
                   " ".join(["{{bar{}}}".format(i) for i in range(len(cpu))]))


if __name__ == "__main__":
    main()
