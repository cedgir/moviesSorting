# coding:utf-8

from utils.single_dispatcher import SingleDispatcher
import settings


class Base(object, SingleDispatcher):
    def __init__(self, dictionary, info):
        super(Base, self).__init__()
        self.__dict__.update(dictionary)
        self.info_file = info

    def treat(self, key):
        if self.info_file['extension'] in settings.MOVIE_EXTENSIONS_LIST:
            self.__callbacks__[key](self)
