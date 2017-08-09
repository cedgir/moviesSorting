# coding:utf-8

import re


def get_valid_filename(s):
    s = s.strip()
    s = re.sub(r'\s*:\s*', ' - ', s)
    return re.sub(r'(?u)["\\/*?<>|]', '', s)
