from advert import Advert

if __name__ == '__main__':

    lesson_str = """{
       "title": "python",
        "price": 100,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        }
    }"""

    iphone_str = """{
        "title": "iPhone X",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
    }"""

    corgi_str = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }"""

    python_str = """{
        "title": "python"
    }"""

    lesson = Advert(lesson_str)
    corgi = Advert(corgi_str)
    iphone = Advert(iphone_str)
    python = Advert(python_str)

    print(corgi)