from copy import deepcopy


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


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.id = self.incr_id()
        self.name = name
        self.category = category
        self.category.courses_count += 1
        # self.category.courses.append(self)


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
        'offline': OfflineCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category, address):
        return cls.types[type_](name, category, address)
