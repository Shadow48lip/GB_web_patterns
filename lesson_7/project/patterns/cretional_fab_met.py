from copy import deepcopy
from patterns.behavioral_patterns import Subject
from patterns.architectural_system_pattern_unit_of_work import DomainObject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# преподаватель
class Teacher(User, DomainObject):
    def __init__(self, name):
        self.teachers = []
        super().__init__(name)


# студент
class Student(User, DomainObject):

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип
class CoursePrototype:
    # прототип курсов обучения
    auto_id = 0

    @staticmethod
    def incr_id():
        CoursePrototype.auto_id += 1
        return CoursePrototype.auto_id

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.id = self.incr_id()
        self.name = name
        self.category = category
        self.students = []
        super().__init__()
        # self.category.courses.append(self)

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# интерактивный курс
class InteractiveCourse(Course):
    def __init__(self, name, category, address):
        super().__init__(name, category)
        self.type = 'interactive'
        self.address = address


# курс в записи
class OfflineCourse(Course):
    def __init__(self, name, category, address):
        super().__init__(name, category)
        self.type = 'offline'
        self.address = address


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'offline': OfflineCourse,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category, address):
        return cls.types[type_](name, category, address)


