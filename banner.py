# coding=utf-8

__project__ = 'banner'


class Banner(object):
    def __init__(self, config):
        self.__image_url = config.pop(0)
        self.show_count = int(config.pop(0))
        self.categories = config

    @property
    def image_url(self):
        self.show_count -= 1
        return self.__image_url