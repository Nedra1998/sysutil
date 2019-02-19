import re


def get_bar(percent, minmum=False):
    if minmum is False:
        if percent <= 11.11:
            return ' '
        elif percent <= 22.22:
            return '\u2581'
        elif percent <= 33.33:
            return '\u2582'
        elif percent <= 44.44:
            return '\u2583'
        elif percent <= 55.55:
            return '\u2584'
        elif percent <= 66.66:
            return '\u2585'
        elif percent <= 77.77:
            return '\u2586'
        elif percent <= 88.88:
            return '\u2587'
        else:
            return '\u2588'
    elif minmum is True:
        if percent <= 12.5:
            return '\u2581'
        elif percent <= 25:
            return '\u2582'
        elif percent <= 37.5:
            return '\u2583'
        elif percent <= 50:
            return '\u2584'
        elif percent <= 62.5:
            return '\u2585'
        elif percent <= 75:
            return '\u2586'
        elif percent <= 87.5:
            return '\u2587'
        else:
            return '\u2588'


def gen_color_code(string):
    string = string.strip('{')
    string = string.strip('}')
    string = string.strip('#')
    rgb_color = tuple(int(string[i:i + 2], 16) for i in (0, 2, 4))
    return "\033[38;2;{};{};{}m".format(rgb_color[0], rgb_color[1],
                                        rgb_color[2])


def fmt_print(data, fmt, end=''):
    fmt = fmt.replace("{#}", "\033[39m")
    colors = re.findall("{#.{6}}", fmt)
    for i, match in enumerate(colors):
        fmt = fmt.replace(match, ">>{}<<".format(i))
    fmt = fmt.format(**data)
    for i, match in enumerate(colors):
        # fmt = fmt.replace(">>{}<<".format(i), '%{F' + match.lstrip('{'))
        fmt = fmt.replace(">>{}<<".format(i), gen_color_code(match))
    print(fmt, end=end)


def fmt_percent(percent, whole=False):
    if whole is True:
        return "{:.0f}".format(percent)
    if percent >= 100:
        return "{:3.0f}".format(percent)
    elif percent >= 10:
        return "{:4.1f}".format(percent)
    else:
        return "{:4.2f}".format(percent)
