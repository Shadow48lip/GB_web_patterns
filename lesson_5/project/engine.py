""" Классы управления сайтом """
from datetime import datetime
import os
from patterns.cretional_singleton import SingletonByName
from patterns.cretional_fab_met import CourseFactory


class Logger(metaclass=SingletonByName):
    """
    Модуль логирования в директорию logs
    :param name: имя файла
    """

    def __init__(self, name):
        self.name = name

    def log(self, text):
        file = f'{self.name}.log'
        path = os.path.join('logs', file)
        with open(path, 'a') as f:
            f.write(f'{datetime.now()}  {text}\n')


class Category:
    auto_id = 0

    def __init__(self, name, category):
        Category.incr_id()
        self.id = Category.auto_id
        self.name = name
        self.category = category
        self.courses_count = 0

    @staticmethod
    def incr_id():
        Category.auto_id += 1

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    """ Главный класс сайта """

    def __init__(self):
        self.categories = []
        self.courses = []

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            # print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Not found category id = {id}')

    @staticmethod
    def create_course(type_, name, category, address):
        return CourseFactory.create(type_, name, category, address)

    def get_course(self, id):
        for item in self.courses:
            if item.id == id:
                return item
        raise Exception(f'Not found course id = {id}')

    # тестовое наполнение словаря
    def create_test_data(self):
        new_category1 = self.create_category('Cat 1', None)
        self.categories.append(new_category1)
        new_category2 = self.create_category('Cat 2', None)
        self.categories.append(new_category2)
        new_category = self.create_category('Cat 3', new_category2)
        self.categories.append(new_category)
        new_category = self.create_category('Cat 4', new_category1)
        self.categories.append(new_category)
        new_category = self.create_category('Cat 5', new_category2)
        self.categories.append(new_category)
        print('created test data')

