# coding=utf-8

__project__ = 'banner'


class Banner(object):
    """
    >>> Banner(['http://', 1, 'none']) # doctest: +ELLIPSIS
    <banner.Banner object at 0x...>
    """
    def __init__(self, config):
        self.__image_url = config.pop(0)
        self.show_count = int(config.pop(0))
        self.categories = set(config)

    @property
    def image_url(self):
        """
        >>> b = Banner(['http://', 1, 'none'])
        >>> b.show_count
        1
        >>> b.image_url
        'http://'
        >>> b.show_count
        0
        >>> b.image_url
        '/images/404.jpg'
        """
        if not self.show_count:
            return '/images/404.jpg'

        self.show_count -= 1
        return self.__image_url