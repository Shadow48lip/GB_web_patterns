
class Framework:
    """
    Framework - самостоятельное ядро фреймворка. Работает как библиотека.
    :param routes: массив роутингов url пути (page controller)
    :param fronts: массив функций обработчиков входящих данных (front controller)
    :return: bytes
    """

    def __init__(self, routes, fronts):
        self.routes_lst = routes
        self.fronts_lst = fronts

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        # print(environ)

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = self.routes_lst['Err404']

        request = {}
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request, environ)

        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]