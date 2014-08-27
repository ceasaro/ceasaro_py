import re
from datetime import timedelta


def convert_string(string):
    """
    :param string: string to convert
    :return: int value of string, if string is a number or percentage.
            e.g. '11' -> 11,
                 '3%' -> 3

    otherwise the original string is returned
    """
    try:
        stripped_str = string.strip()
        if stripped_str.isdigit():
            # check if integer
            return int(stripped_str)
        elif '.' in stripped_str:
            return float(stripped_str)
        elif stripped_str.endswith('%'):
            # check if percentage
            stripped_percentage_str = stripped_str[:-1].strip()
            if stripped_percentage_str.isdigit():
                return int(stripped_percentage_str)
    except ValueError, e:
        pass  # ignore a value error just return the string
    return string


regex = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')


def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)