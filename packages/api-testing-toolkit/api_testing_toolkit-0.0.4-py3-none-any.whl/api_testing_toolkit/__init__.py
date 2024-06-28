# SPDX-FileCopyrightText: 2024-present Tom <JosephDotson@belkonar.com>
#
# SPDX-License-Identifier: MIT

from requests.structures import CaseInsensitiveDict
from IPython.display import JSON
import json


def d(data):
    if isinstance(data, CaseInsensitiveDict):
        data = dict(data) # just reset it

    if isinstance(data, dict):
        return JSON(data, expanded=True)

    return data


def load_env(name):
    try:
        f = open('env/{}.json'.format(name))
        return json.load(f)
    except FileNotFoundError:
        print('no env found, returning nothing')
        return {}

