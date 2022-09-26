""" Порождающий паттерн Singleton """

from threading import Lock, Thread

"""
Гарантирует, что у класса есть только один экземпляр, и предоставляет к нему глобальную точку доступа.
Класс Одиночка объявляет свой конструктор приватным. С одной стороны, это не позволяет клиентскому 
коду самовольно порождать инстансы Одиночки, с другой — предоставляет статический метод getInstance, 
возвращающий инстанс объекта Одиночки, инстанциация которого полностью контролируется классом-Одиночкой.
"""


# Одиночка модифицирован для работы в многопоточной среде
class SingletonThreads(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instances = {}
        cls.__lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                instance = super().__call__(*args, **kwargs)
                cls.__instances[cls] = instance
        return cls.__instances[cls]


# Одиночка без потоков, но с учетом имени инстанса
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instances = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name not in cls.__instances:
            cls.__instances[name] = super().__call__(*args, **kwargs)
        return cls.__instances[name]


class LoggerThread(metaclass=SingletonThreads):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        pass


# class Logger(metaclass=SingletonByName):
#     def __init__(self, name):
#         self.name = name
#
#     def log(self, text):
#         file = f'{self.name}.log'
#         path = os.path.join('logs', file)
#         with open(path, 'a') as f:
#             f.write(f'{datetime.now()}  {text}\n')


if __name__ == "__main__":
    def test_logger_thread(name):
        logger = LoggerThread(name)
        print(logger.name)


    process1 = Thread(target=test_logger_thread, args=("FOO",))
    process2 = Thread(target=test_logger_thread, args=("BAR",))
    process1.start()
    process2.start()

    # test_logger('test_log')

    # logger1 = Logger('main')
    # logger1.log('taram param')
    #
    # logger2 = Logger('main')
    # print(logger1 is logger2)
    #
    # logger3 = Logger('other')
    # print(logger1 is logger3)
