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
        self._categories_h = []
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

    # @staticmethod
    def create_course(self, type_, name, category, address):
        new_course = CourseFactory.create(type_, name, category, address)
        self.incr_category_course_count(category)
        return new_course

    def get_course(self, id):
        for item in self.courses:
            if item.id == id:
                return item
        raise Exception(f'Not found course id = {id}')

    def _incr_category_course_count_worker(self, base_category):
        """ Рекурсивный приватный метод инкрементного увеличения счетчика по иерархии """
        base_category.courses_count += 1

        if base_category.category is None:
            return

        for category in self.categories:
            if category.id == base_category.category.id:
                self._incr_category_course_count_worker(category)
                break

    def incr_category_course_count(self, base_category):
        self._incr_category_course_count_worker(base_category)

    def _build_hierarchy_categories(self, base_category, level=0):
        """ Рекурсивная функция постройки иерархического списка категорий """
        # base_category.name = f"{'-' * level}{base_category.name}"
        base_category.name_web = f"{'-' * level}{base_category.name}"
        self._categories_h.append(base_category)
        level += 1

        for category in self.categories:
            if category.category is None:
                continue
            # ищем потомков переданной в функцию категории
            if category.category.id == base_category.id:
                self._build_hierarchy_categories(category, level)
    @property
    def hierarchy_categories(self):
        """ Метод перестраивает и возвращает иерархические категории """
        # временный сортированный список
        self._categories_h = []

        for category in self.categories:
            if category.category is None:
                self._build_hierarchy_categories(category)

        self.categories = self._categories_h
        return self.categories

    # тестовое наполнение словаря
    def create_test_data(self):
        new_category1 = self.create_category('Cat 1', None)
        self.categories.append(new_category1)
        new_category2 = self.create_category('Cat 2', None)
        self.categories.append(new_category2)
        new_category = self.create_category('Cat 3', new_category2)
        self.categories.append(new_category)
        new_category3 = self.create_category('Cat 4', new_category1)
        self.categories.append(new_category3)
        new_category = self.create_category('Cat 5', new_category2)
        self.categories.append(new_category)
        new_category = self.create_category('Cat 6', new_category3)
        self.categories.append(new_category)

        hierarchy_categories = self.hierarchy_categories

        print(f'created test data len {len(hierarchy_categories)}')
