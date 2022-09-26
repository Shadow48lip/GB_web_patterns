""" Декораторы """
from datetime import datetime
import time


class Debug:
    """ Замер времени выполнения метода класса """

    def __init__(self, name):
        self.class_name = name

    def __call__(self, cls):
        # Вспомогательный декоратор будет декорировать каждый метод класса/
        def timeit(method):
            def timed(*args, **kwargs):
                ts = datetime.now()
                result = method(*args, **kwargs)
                worktime = datetime.now() - ts
                print(f'Время выполнения {self.class_name}.{method.__name__} выполнялся {worktime}')
                return result

            return timed

        return timeit(cls)


class Route:
    """
    Декоратор для добавления пути в таблицу роутинга. На входе словарь роутинга и PATH_INFO
    """

    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


if __name__ == "__main__":
    class Person:
        @Debug("Person")
        def __call__(self, *args, **kwargs):
            time.sleep(1)
            print('test')


    obj = Person()
    obj('ww')
