#!/usr/bin/env python3

import util
import sys
import psutil


def get_data():
    data = psutil.disk_usage('/')
    return data.total, data.used, data.free, data.percent


def get_size(byte, sufix):
    if sufix == 'KB':
        return "{:.2f}".format(byte / 1e3)
    elif sufix == 'MB':
        return "{:.2f}".format(byte / 1e6)
    elif sufix == 'GB':
        return "{:.2f}".format(byte / 1e9)
    elif sufix == 'TB':
        return "{:.2f}".format(byte / 1e12)
    elif sufix == 'Auto':
        if byte >= 1e12:
            return "{:.2f}".format(byte / 1e12), "TB"
        elif byte >= 1e9:
            return "{:.2f}".format(byte / 1e9), "GB"
        elif byte >= 1e6:
            return "{:.2f}".format(byte / 1e6), "MB"
        elif byte >= 1e3:
            return "{:.2f}".format(byte / 1e3), "KB"
        else:
            return "{:.2f}".format(byte), "B"


def main():
    total, used, available, percentage = get_data()
    data = dict()
    data['icon'] = '\ue706'
    data['percent'] = percentage
    data['totalKB'] = get_size(total, 'KB')
    data['totalMB'] = get_size(total, 'MB')
    data['totalGB'] = get_size(total, 'GB')
    data['totalTB'] = get_size(total, 'TB')
    data['totalAuto'], data['totalSufix'] = get_size(total, "Auto")
    data['usedKB'] = get_size(used, 'KB')
    data['usedMB'] = get_size(used, 'MB')
    data['usedGB'] = get_size(used, 'GB')
    data['usedTB'] = get_size(used, 'TB')
    data['usedAuto'], data['usedSufix'] = get_size(used, "Auto")
    data['availableKB'] = get_size(available, 'KB')
    data['availableMB'] = get_size(available, 'MB')
    data['availableGB'] = get_size(available, 'GB')
    data['availableTB'] = get_size(available, 'TB')
    data['availableAuto'], data['availableSufix'] = get_size(available, "Auto")
    data['bar'] = util.get_bar(percentage)
    util.fmt_print(data, sys.argv[1] if len(sys.argv) > 1 else
                   "{icon} {availableAuto}{availableSufix} {percent}%{bar}")


if __name__ == "__main__":
    main()
