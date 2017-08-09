# coding:utf-8


class SingleDispatcher:
    __callbacks__ = {}

    @classmethod
    def set_callback(cls, key, cbk):
        cls.__callbacks__[key] = cbk
        return cbk

    @classmethod
    def register(cls, key):
        def wrapper(cbk):
            return cls.set_callback(key, cbk)

        return wrapper

    @property
    def dispatcher(self):
        return self.__callbacks__

    def dispatch(self, key, default=None):
        return self.__callbacks__.get(key, default)
