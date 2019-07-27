"""
Методы для работы с переменными окружения.

Архитектура простая.
Есть объект контейнер, который отвечает за переменны окружения. Эта штука шипко умная.
Она умеет преобразовывать в питон типы, умеет дополнять пополнять менять, загружить и записывать.
Она умеет поддерживать свои значения в актуальном состоянии.
Так же есть микрокомпоненты.
    -   Это парсеры переменных окружения. (Преобразует переменные в питон типы.)
    -   Это читалки переменных окружения из потоков.

"""
import logging
import os

logger = logging.getLogger('ENVIRONMENTS')


class BaseParser(object):
    """
    Базовый парсер переменных окружения.
    Принимает значение переменной, и возвращает преобразованное значение в питон тип.

    """
    @classmethod
    def _parse_row(cls, *args, **kwargs):
        """
        Преобразует сырую строку в пито типы.

        :return: Пробразованную строку. key, value
        :rtype: tuple

        :raises: ValueError - Если строку не удалось распарсить.

        """
        raise NotImplementedError()

    @classmethod
    def _parse_value(cls, value):
        """
        Преобразует переменную в питон объект.

        :param value: Значение которое нужно преобразовать.
        :type value: str

        :return: Преобразованное значение.
        :rtype: object

        """
        raise NotImplementedError()

    @classmethod
    def __call__(cls, row):
        try:
            return cls._parse_row(row)
        except Exception as e:
            raise ValueError(e)


class StandardParser(BaseParser):
    """
    Дефолтный простой пасрер.
    Преобразует булевы значения и числа.

    """

    @classmethod
    def _parse_row(cls, row):
        line_strip = row.split('=')
        if not line_strip[0].startswith('#') and row.strip() != '':
            return line_strip[0], cls._parse_value(line_strip[1].strip())

    @classmethod
    def _parse_value(cls, value):
        if value in ('False', 'True', 'FALSE', 'TRUE', 'true', 'false'):
            return eval(value)
        if value.isdigit():
            return int(value)
        return value


class KeyValueParser(BaseParser):
    """
    Парсер значений key, value переданных в виду tuple.

    """
    @classmethod
    def _parse_row(cls, row):
        key, value = row
        return key, cls._parse_value(value)

    @classmethod
    def _parse_value(cls, value):
        if value in ('False', 'True', 'FALSE', 'TRUE', 'true', 'false'):
            return eval(value)
        if value.isdigit():
            return int(value)
        return value


class LoadEnvironmentsBase(object):
    """
    Базовая загрузка переменныз окружения.

    """
    @classmethod
    def load(cls, parser, *args, **kwargs):
        """
        Загрузка переменных окружения из потока.

        :param BaseParser parser: Парсер переменных.

        """
        raise NotImplementedError()

    @classmethod
    def load_yield(cls, parser, *args, **kwargs):
        """
        ЛЕНИВАЯ Загрузка переменных окружения из потока.

        :param BaseParser parser: Парсер переменных.

        """
        raise NotImplementedError()

    @classmethod
    def dump(cls, *args, **kwargs):
        """ Запись переменных окружения в поток. """
        raise NotImplementedError()


class FileLoadEnvironments(LoadEnvironmentsBase):
    """ Загрузчик и файла. """

    @classmethod
    def load(cls, parser, file_in):
        """
        Загрузка данных из файла.

        :param BaseParser parser: Парсер переменных.
        :param str file_in: Путь до файла откуда грузим.

        :return: Распарсенные переменные.
        :rtype: dict

        """
        try:
            return {key: val for key, val in cls.load_yield(parser, file_in)}
        except Exception as e:
            logger.error('Не удалось загрузить переменные из файла `{}`. Подробнее: `{}`.'.format(file_in, e))
        return None

    @classmethod
    def load_yield(cls, parser, file_in):
        """
        Загрузка данных из файла.

        :param BaseParser parser: Парсер переменных.
        :param str file_in: Путь до файла откуда грузим.

        :return: Рапарсенные переменные. tuple(key, value)
        :rtype: tuple

        """
        try:
            with open(file_in, 'r') as read_file:
                for row in read_file.readlines():
                    try:
                        result = parser(row)
                        if result:
                            yield result
                    except Exception as e:
                        logger.error('Не удалось распарсить строчку `{}`. Подробнее: `{}`.'.format(row, e))
        except Exception as e:
            logger.error('Не удалось загрузить переменные из файла `{}`. Подробнее: `{}`.'.format(file_in, e))
        return None

    @classmethod
    def dump(cls, text, file_out):
        """
        Сохранение файла

        :param file_out: Путь до файла куда сохраняем.
        :param text: Текст, который мы пишем.
        :type file_out: str
        :type text: str

        """
        try:
            with open(file_out, 'w') as write_file:
                write_file.write(text)
        except Exception as e:
            logger.error('Не удалось записать в файл `{}`. Подробнее: `{}`.'.format(
                file_out, e
            ))


class OSLoadEnvironments(LoadEnvironmentsBase):
    """
    Загрузчик системных переменных окружения.

    """
    parser = KeyValueParser

    @classmethod
    def load(cls, parser):
        """
        Загрузчик переменных из системы.

        :param BaseParser parser: Парсер переменных.

        :return: Словарь переменных из системы.

        """
        try:
            return {key: val for key, val in cls.load_yield(parser)}
        except Exception as e:
            logger.error('Не удалось загрузить переменные из системы. Подробнее: `{}`.'.format(e))
        return None

    @classmethod
    def load_yield(cls, parser):
        """
        Ленивая загрузка переменных.

        :param BaseParser parser: Парсер переменных.

        :return: Распарсенные переменные.
        :rtype: tuple(key, val)

        """
        try:
            for key, val in dict(os.environ).items():
                try:
                    yield parser((key, val))
                except Exception as e:
                    logger.error(
                        'Не удалось распарсить переменную `{0}`: `{1}`. Подробнее: `{2}`.'.format(key, val, e)
                    )
        except Exception as e:
            logger.error('Не удалось загрузить переменные из системы. Подробнее: `{}`.'.format(e))
        return None

    @classmethod
    def dump(cls, params):
        """
        Установка переменных в окружение.

        :param dict params: Словарь с переменными.

        """
        if isinstance(params, dict):
            for key, val in params.items():
                try:
                    os.environ[key] = val
                except Exception as e:
                    logger.error(
                        'Не удалось установить переменную `{0}`: `{1}`. Подробнее: `{2}`.'.format(key, val, e)
                    )


class EnvironmentFileToDict(dict):
    """
    Объект с интерфейсом словаря но с варнингами если такого ключа нет.

    """
    parser_class = StandardParser
    load_class = FileLoadEnvironments

    def load(self, file_in, load_class=FileLoadEnvironments, parser_class=StandardParser):
        """
        Загружает переменные окружения в себя.

        :param file_in: Путь до потока с переменными окружения.
        :param load_class: Класс для загрузки переменных.
        :param parser_class: Класс для парсинга переменных.
        :type file_in: str
        :type load_class: LoadEnvironmentsBase
        :type parser_class: BaseParser

        """
        load_class = load_class() if load_class else self.load_class()
        parser_class = parser_class() if parser_class else self.parser_class()

        for key, val in load_class.load_yield(parser_class, file_in):
            try:
                self.__setitem__(key, val)
            except Exception as e:
                logger.error('Не удалось распарсить строчку `{}`. Подробнее: `{}`.'.format(
                    key, e
                ))

    def get(self, k, d=None):
        if k not in self:
            logging.warning('Запрашиваемая переменная окружения `{}` не найдена.'.format(k))
        return super(EnvironmentFileToDict, self).get(k, d)

    def __getitem__(self, y):
        if y not in self:
            logging.warning('Запрашиваемая переменная окружения `{}` не найдена.'.format(y))
        return super(EnvironmentFileToDict, self).__getitem__(y)


class EnvironmentOsToDict(EnvironmentFileToDict):
    """
    Объект с интерфейсом словаря но с варнингами для загрузки из системы.

    """
    parser_class = KeyValueParser
    load_class = OSLoadEnvironments

    def load(self, load_class=OSLoadEnvironments, parser_class=KeyValueParser):
        """
        Загружает переменные окржения из системы в себя.

        :param load_class: Класс для загрузки переменных.
        :param parser_class: Класс для парсинга переменных.
        :type load_class: LoadEnvironmentsBase
        :type parser_class: BaseParser

        """
        load_class = load_class() if load_class else self.load_class()
        parser_class = parser_class() if parser_class else self.parser_class()

        for key, val in load_class.load_yield(parser_class):
            try:
                self.__setitem__(key, val)
            except Exception as e:
                logger.error('Не удалось распарсить переменную `{}`. Подробнее: `{}`.'.format(
                    key, e
                ))


DefaultEnvironmentDict = EnvironmentOsToDict
