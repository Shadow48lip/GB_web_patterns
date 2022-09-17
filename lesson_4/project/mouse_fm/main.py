from pprint import pprint
from mouse_fm.query_requests import GetRequests, PostRequests


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
        # pprint(environ)

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'
        request = {'path': path}

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # Сразу кладем туда метод запроса GET, POST, PUT, DELETE
        request['method'] = environ['REQUEST_METHOD']

        # Получаем все данные запроса
        if request['method'] == 'POST':
            data = PostRequests().get_request_params(environ)
            print(f'Нам пришёл post-запрос: {data}')
            request['post_data'] = data
        if request['method'] == 'GET':
            request_params = GetRequests().get_request_params(environ)
            print(f'Нам пришли GET-параметры: {request_params}')
            if len(request_params) > 0:
                request['get_params'] = request_params

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = self.routes_lst['Err404']

        # Прогоняем полученные данные через middleware
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request, environ)

        print('Вот что хранится в request после работы front controller')
        pprint(request)

        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    # Это пример преподавателя. Сделаем тоже самое за счет встроенных модулей.
    # @staticmethod
    # def url_decode_value(data):
    #     """
    #     Декодирует
    #     :param data:
    #     :return:
    #     """
    #     new_data = {}
    #     for k, v in data.items():
    #         val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
    #         val_decode_str = decodestring(val).decode('UTF-8')
    #         new_data[k] = val_decode_str
    #     return new_data
