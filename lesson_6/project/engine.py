""" Классы управления сайтом """

from patterns.behavioral_patterns import FileWriter
from patterns.cretional_singleton import SingletonByName
from patterns.cretional_fab_met import CourseFactory, UserFactory


class Logger(metaclass=SingletonByName):
    """
    Модуль логирования в директорию logs
    :param name: имя файла
    :param writer: объект (стратегия) записи
    """

    def __init__(self, name, writer=FileWriter()):
        self.writer = writer
        self.writer.log_name = name

    def log(self, text):
        self.writer.write(text)




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
        self.teachers = []
        self.students = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)


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
        print('courses', self.courses)
        for item in self.courses:
            if item.id == id:
                return item
        raise Exception(f'Not found course id = {id}')

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item

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


