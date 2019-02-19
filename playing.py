#!/usr/bin/env python3

import sys
import util
import subprocess
import json
from pprint import pprint
from csv import reader


def get_dict():
    data = dict()
    metadata = subprocess.run(
        ["playerctl", "metadata"],
        stdout=subprocess.PIPE).stdout.decode('utf-8')
    data['metadata'] = metadata
    metadata = metadata[1:-1]
    state = 0
    prev = str()
    current = str()
    item = []
    for ch in metadata:
        if (state == 0 and (ch == "\'" or ch == "\"")):
            if state == 0 and ch == "\'":
                state = 1
            if state == 0 and ch == "\"":
                state = 2
            current = str()
        elif (state == 0 and ch == '<'):
            state = 3
        elif (state == 3 and ch == '>'):
            if item[1] == str() and current != str():
                item[1] = current
            data[item[0]] = item[1]
            state = 0
        elif (state == 1 and ch == "\'") or (state == 2 and ch == "\""):
            state = 0
            if len(current.split(':')) > 1:
                current = current.split(':')[-1]
            item = [current, str()]
            current = str()
        elif state == 3 and ch == "\'":
            state = 4
        elif state == 4 and ch == "\'":
            state = 3
            item[1] = current
            current = str()
        elif state == 3 and ch == "\"":
            state = 5
        elif state == 5 and ch == "\"":
            state = 3
            item[1] = current
            current = str()
        elif state == 3 and ch == "[":
            state = 6
            item[1] = list()
        elif state == 6 and ch == "]":
            state = 3
        elif state == 6 and ch == "\'":
            state = 7
        elif state == 7 and ch == "\'":
            state = 6
            item[1].append(current)
            current = str()
        elif state == 6 and ch == "\"":
            state = 8
        elif state == 8 and ch == "\"":
            state = 6
            item[1].append(current)
            current = str()
        elif state != 0:
            current += ch
    return data


def get_data():
    status = subprocess.run(
        ["playerctl", "status"], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).stdout.decode('utf-8')
    if status.strip() == "Playing":
        status = True
    elif status.strip() == "Paused":
        status = False
    else:
        status = -1
    return status


def get_play_pause(status):
    if status == False:
        return '\uf04b'
    elif status == True:
        return '\uf04c'
    else:
        return ''


def get_time(micro):
    minute = int(micro / 6e7)
    micro -= minute * 6e7
    second = int(micro / 1e6)
    return "{}:{:02}".format(minute, second)


def main():
    status = get_data()
    data = dict()
    if status != -1:
        data = get_dict()
        data['artist'] = ' '.join(data['artist'])
        data['length'] = get_time(float(data['length'].split(' ')[1]))
    data['status'] = str(status)
    data['play_pause'] = get_play_pause(status)
    data['next'] = '\uf051'
    data['prev'] = '\uf048'
    data['icon'] = '\uf001'
    if len(sys.argv) == 1:
        sys.argv.append("{icon} {#FF9800}{artist}: {title:.40}{#}")
        sys.argv.append("{icon} {#90A4AE}{artist}: {title:.40}{#}")
        sys.argv.append("{#607D8B}{icon} {#}")
    if len(sys.argv) <= 2:
        util.fmt_print(data, sys.argv[1])
    if status is True and len(sys.argv) >= 3:
        util.fmt_print(data, sys.argv[1])
    elif status is False and len(sys.argv) >= 3:
        util.fmt_print(data, sys.argv[2])
    elif len(sys.argv) >= 4:
        util.fmt_print(data, sys.argv[3])


if __name__ == "__main__":
    main()
