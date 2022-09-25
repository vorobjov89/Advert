import json
from keyword import iskeyword


class JSONToObject:
    def get_atr(self, key):
        """
        Делаем свой 'fget' для динамически создаваемых свойств
        """
        def func(obj=self):
            return obj.__getattribute__('_' + key)
        return func

    def set_atr(self, key):
        """
        Делаем свой 'fset' для динамически создаваемых свойств
        """
        def func(obj=self, value=None):
            obj.__setattr__('_' + key, value)
        return func

    def __init__(self, loaded_json):
        """
        Если конструктор класса получает словарь, он рекурсивно проходит по этому словарю и
        добавляет его элементы в качестве атрибутов. Если встречаеn вложенный словарь,
        конструктор применяет к нему себя, вкладывая в качестве атрибута объект класса. Предполагается, что конструктор
        получает словарь, созданный из json-объекта.

        Если конструктор получает json-объект в виде строки, он переводит его в словарь и действует как описано выше.
        Таким образом экземпляр класса (или подкласса) может быть инициализирован как json-строкой, так и словарем.

        Все атрибуты класса получают защищенный ('_attribute_name') ключ. Для доступа к ним динамически создаются
        свойства с публичным ('attribute_name') ключом. Заполнение значениями происходит уже через свойства
        """
        if type(loaded_json) == dict:
            for key, item in loaded_json.items():  # Проходим по словарю.

                if iskeyword(key):  # Если атрибут совпадает с ключевым словом - прибавляем ему '_' с конца.
                    key = key + '_'

                setattr(self.__class__, key, property(self.get_atr(key), self.set_atr(key)))
                if type(item) == dict:
                    self.__setattr__('_' + key, JSONToObject(item))
                else:
                    self.__setattr__(key, item)
        else:
            self.__init__(json.loads(loaded_json))  # Обрабатываем json-строку.


class ColorizeMixin:
    """
    COLORTABLE - таблица фиксированных цветов для объявлений с разными названиями;
    repr_color_code - текущий цвет объявления, по умолчанию белый
    """
    COLORTABLE = {
        'default': 37,  # белый
        'Вельш-корги': 33,  # желтый
        'iPhone X': 31  # красный
    }

    repr_color_code = COLORTABLE['default']


class Advert(ColorizeMixin, JSONToObject):
    def __init__(self, loaded_json):
        JSONToObject.__init__(self, loaded_json)

        setattr(self.__class__, 'price', property(self.get_price, self.set_price))  # Меняем свойство для price.
        if hasattr(self, '_price'):
            self.__setattr__('price', self.price)  # Нужно для проверки ValueError при создании объекта

    @staticmethod
    def get_price(obj):
        """
        Делаем свой 'getter' для price.
        Свойство - атрибут класса, а не экземпляра; вместе с тем, функция fget, скармливаемая в объект свойства,
        не нуждается в ссылке на класс, для которого она реализует какую-то логику. Поэтому выбираем декоратор
        @staticmethod. Без него fget бы принимал лишний параметр - вторую ссылку на использующий свойство объект.
        """
        if hasattr(obj, '_price'):
            return obj.__getattribute__('_price')
        else:
            print(0)  # Я так и не понял из задания, нужно ли ставить здесь исключение.
            return "0 (No price value)"  # Поэтому обработал как есть.

    @staticmethod
    def set_price(obj, value):
        """
        Делаем свой 'setter' для price
        Логика метода описана выше - см. комментарий к 'getter'у.
        """
        if hasattr(obj, '_price'):
            if value < 0:
                raise ValueError('must be >= 0')  # Выбрасываем исключение при отрицательном значении цены.
            else:
                obj.__setattr__('_price', value)

    def __repr__(self):
        if self.title in self.COLORTABLE.keys():
            self.repr_color_code = self.COLORTABLE[self.title]
        else:
            self.repr_color_code = self.COLORTABLE['default']
        return f'\033[{self.repr_color_code}m{self.title} | {self.price} ₽'
