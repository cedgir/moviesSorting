# coding:utf-8

import pynma

import settings


def send_notif(subject, message, url=""):
    p = pynma.PyNMA(settings.PYNMA_KEY)
    p.push('Torrents', subject, message, url)
