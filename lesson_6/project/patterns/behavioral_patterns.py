""" Поведенческие паттерны """
import os
from abc import ABC, abstractmethod
from datetime import datetime
# from jsonpickle import dumps, loads
from mouse_fm.templator import render


# поведенческий паттерн - наблюдатель
# Курс
class Observer:

    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print('Notify SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject):
        print('Notify EMAIL->', 'к нам присоединился', subject.students[-1].name)



# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = {}
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        # print('++!!++', self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(ListView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['post_data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


# поведенческий паттерн - Стратегия
class AbstractWriter(ABC):
    def __init__(self):
        # default log name
        self.log_name = 'log'

    @abstractmethod
    def write(self, text):
        pass


class ConsoleWriter(AbstractWriter):

    def write(self, text):
        print(f'{self.log_name} --> {text}')


class FileWriter(AbstractWriter):

    def write(self, text):
        file = f'{self.log_name}.log'
        path = os.path.join('logs', file)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()}  {text}\n')
