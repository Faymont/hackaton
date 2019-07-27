"""
Конвертеры URL.

https://docs.djangoproject.com/en/2.0/topics/http/urls/#registering-custom-path-converters
"""


class BaseConverter(object):
    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class UIDBase64Converter(BaseConverter):
    regex = '[0-9A-Za-z_\-]+'


class TokenConverter(BaseConverter):
    regex = '[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}'
