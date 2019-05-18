#!/usr/bin/env python3

import urllib.request, json
import pprint
import sys
import util

KEY = "9c9c48f9ab5717ed899e8b6d730883c6"


def get_data():
    try:
        with urllib.request.urlopen("http://ipinfo.io/json") as url:
            locate = json.load(url)
        if locate is None:
            return {}
        with urllib.request.urlopen(
                "https://api.darksky.net/forecast/{}/{}?exclude=[minutely,alerts,flags]".
                format(KEY, locate['loc'])) as url:
            data = json.load(url)
        return {**data, 'location': locate} if data else {}
    except:
        return {}


def get_icon(name):
    # Darksky icons
    if name == "clear-day":
        return "\ue30d"
    elif name == "clear-night":
        return "\ue32b"
    elif name == "rain":
        return "\ue318"
    elif name == "snow":
        return "\ue31a"
    elif name == "sleet":
        return "\ue3ad"
    elif name == "wind":
        return "\ue34b"
    elif name == "fog":
        return "\ue313"
    elif name == "cloudy":
        return "\ue312"
    elif name == "partly-cloudy-day":
        return "\ue302"
    elif name == "partly-cloudy-night":
        return "\ue37e"
    elif name == "hail":
        return "\ue314"
    elif name == "thunderstorm":
        return "\ue31d"
    elif name == "tornado":
        return "\ue351"
    else:
        return "\ue33b"


def gen_spark(data, key, count, perc=False):
    vals = []
    for val in data:
        vals.append(val[key])
        if len(vals) == count:
            break
    min_val = min(vals)
    max_val = max(vals)
    if perc:
        min_val = 0
        max_val = 1
    res = ""
    for v in vals:
        res += util.get_bar(100.0 * (v - min_val) / (max_val - min_val),
                            not perc)
    return res


def gen_dict(report):
    data = {**report['currently']}
    data['deg'] = '\u00b0'
    data['icon'] = get_icon(data['icon'])
    data['weekSummary'] = report['daily']['summary']
    data['daySummary'] = report['hourly']['summary']
    data['temp'] = data['temperature']
    for i, day in enumerate(report['daily']['data']):
        data['d{}'.format(i)] = {
            **day, 'tempHigh': day['temperatureHigh'],
            'tempLow': day['temperatureLow']
        }
    for i, hour in enumerate(report['hourly']['data']):
        data['h{}'.format(i)] = {**hour, 'temp': hour['temperature']}
    data['gtempH5'] = gen_spark(report['hourly']['data'], 'temperature', 5)
    data['gtempH10'] = gen_spark(report['hourly']['data'], 'temperature', 10)
    data['gtempH15'] = gen_spark(report['hourly']['data'], 'temperature', 15)
    data['gtempH24'] = gen_spark(report['hourly']['data'], 'temperature', 24)
    data['gprecipH5'] = gen_spark(report['hourly']['data'], 'precipProbability',
                                  5, True)
    data['gprecipH10'] = gen_spark(report['hourly']['data'],
                                   'precipProbability', 10, True)
    data['gprecipH15'] = gen_spark(report['hourly']['data'],
                                   'precipProbability', 15, True)
    data['gprecipH24'] = gen_spark(report['hourly']['data'],
                                   'precipProbability', 24, True)
    return data


def main():
    data = get_data()
    if data == {}:
        print("\ue33b", end='')
        return
    data = gen_dict(data)
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        for key in data:
            print(key, end=', ')
        return
    util.fmt_print(data, sys.argv[1] if len(sys.argv) > 1 else
                   "{icon}  {temperature}\u00b0 {summary}")


if __name__ == "__main__":
    main()
