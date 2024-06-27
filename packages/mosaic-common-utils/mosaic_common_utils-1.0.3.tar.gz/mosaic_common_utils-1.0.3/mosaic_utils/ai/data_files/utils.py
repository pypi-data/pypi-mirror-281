# -*- coding: utf-8 -*-
import os
import io
import tempfile
import base64
import shutil
import math
from dateutil import tz
from datetime import datetime
import requests


def parse_file_name(file_name, prefix):
    filename = file_name.split(prefix)[-1]
    return filename


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def format_datetime(date_obj):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = date_obj.replace(tzinfo=from_zone)
    # Convert time zone
    central = utc.astimezone(to_zone)
    return str(central.strftime("%b %d, %Y %H:%M"))


def fetch_dir_file_paths(path, exclude_file):
    list_of_paths = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            data_paths = os.path.join(root, file)
            data_paths = data_paths.split(path)[-1]
            print(data_paths)
            list_of_paths.append(data_paths)
    list_of_paths.remove(exclude_file.split(path)[-1])
    return list_of_paths


def convert_into_bytes(size_string):
    units = {"KB": 1024, "MB": 1024 * 1024, "GB": 1024 * 1024 * 1024}
    for unit in units:
        if unit in size_string:
            index = size_string.find(unit)
            size = size_string[:index].strip()
            unit = size_string[index:].strip()
            return float(size) * units[unit]

    # unit is B
    return float(size_string[:-1])
