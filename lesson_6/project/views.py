from pprint import pprint
from mouse_fm.templator import render
from engine import Logger, Engine
from patterns.structure_deco import Debug, Route
from patterns.behavioral_patterns import FileWriter, ConsoleWriter
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    ListView, CreateView

# можно выбрать способ вывода лога FileWriter(), ConsoleWriter()
logger = Logger('views', ConsoleWriter())
# главный класс движка
site = Engine()
# сюда декоратор @Route наполняет маршруты маршрутизации
routes = {}
# для паттерна Наблюдатель. его наблюдатели для прикрепления к курсу
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@Route(routes, '/')
class Index:
    def __call__(self, request):
        """ Контроллер - главная страница """
        logger.log('Load Index')
        [print(item.__dict__) for item in site.categories]

        objects_list = {'site': request.get('template_var', None), 'categories': site.categories}
        return '200 OK', render('index.html', objects_list=objects_list)


@Route(routes, '/create-category/')
class CreateCategory:
    """ Контроллер - создает новую категорию """

    @Debug('CreateCategory')
    def __call__(self, request):
        method = request.get('method', None)
        logger.log(f'Создание категории : {method}')

        if method == 'POST':
            post_data = request['post_data']
            name = post_data['name']
            try:
                self.category_id = int(post_data['cat_id'])
                category = site.find_category_by_id(int(self.category_id))
            except ValueError:
                category = None

            new_category = Engine.create_category(name, category)
            # print('!!!! ', new_category)
            site.categories.append(new_category)
            hierarchy_categories = site.hierarchy_categories

            objects_list = {'site': request.get('template_var', None), 'categories': hierarchy_categories}
            return '200 OK', render('index.html', objects_list=objects_list)
        else:
            objects_list = {'site': request.get('template_var', None), 'categories': site.categories}
            return '200 OK', render('create_category.html', objects_list=objects_list)


@Route(routes, '/category-list/')
class CategoryList:
    """ Контроллер - список категорий """

    def __call__(self, request):
        logger.log('Список категорий')
        objects_list = {'site': request.get('template_var', None), 'categories': site.categories}
        return '200 OK', render('category_list.html', objects_list=objects_list)


@Route(routes, '/create-course/')
class CreateCourse:
    """ Контроллер - создает новый курс в категории """

    def __call__(self, request):
        method = request.get('method', None)
        logger.log(f'Создание курса : {method}')

        try:
            if request['method'] == 'POST':
                post_data = request['post_data']
                name = post_data['name']
                course_type = post_data['type']
                address = post_data['address']

                self.category_id = int(post_data['cat_id'])
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course(course_type, name, category, address)

                # наблюдатели
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

                site.courses.append(course)
                courses = filter(lambda item: (item.category.id == category.id), site.courses)

                objects_list = {'site': request.get('template_var', None), 'cat_name': category.name,
                                'courses_list': courses, 'id': category.id}
                return '200 OK', render('course_list.html', objects_list=objects_list)
            else:
                self.category_id = int(request['get_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                objects_list = {'site': request.get('template_var', None), 'name': category.name, 'id': category.id}
                return '200 OK', render('create_course.html', objects_list=objects_list)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
        except Exception as e:
            return '200 OK', f'Error: {e}'


@Route(routes, '/courses-list/')
class CoursesList:
    """ Контроллер - список курсов """

    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['get_params']['id']))
            courses = filter(lambda item: (item.category.id == category.id), site.courses)

            [print(item.__dict__) for item in site.courses]
            objects_list = {'site': request.get('template_var', None), 'cat_name': category.name,
                            'courses_list': courses, 'id': category.id}

            return '200 OK', render('course_list.html', objects_list=objects_list)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
        except Exception as e:
            return '200 OK', f'Error: {e}'


@Route(routes, '/copy-course/')
class CopyCourse:
    """ Контроллер - скопировать курс """

    def __call__(self, request):
        logger.log('Копирование курса')

        try:
            request_params = request['get_params']
            id = int(request_params['id'])

            old_course = site.get_course(id)

            new_course = old_course.clone()

            new_course.id = new_course.incr_id()
            # deepcopy копирует вложенный массив, а нам нужна ссылка как у оригинала. Для счетчика
            new_course.category = old_course.category
            # new_course.category.courses_count += 1
            site.incr_category_course_count(new_course.category)
            site.courses.append(new_course)

            # отфильтрованные курсы по текущей категории
            courses = filter(lambda item: (item.category.id == new_course.category.id), site.courses)

            objects_list = {'site': request.get('template_var', None), 'cat_name': new_course.category.name,
                            'courses_list': courses, 'id': new_course.category.id}
            return '200 OK', render('course_list.html', objects_list=objects_list)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
        except Exception as e:
            return '200 OK', f'Error: {e}'


@Route(routes, '/students-list/')
class StudentsListView(ListView):
    queryset = {'students': site.students}
    template_name = 'students_list.html'

    def __call__(self, request):
        self.queryset['site'] = request.get('template_var', None)
        return super().__call__(request)


@Route(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)

    def __call__(self, request):
        logger.log(f'Create student.')
        self.queryset['site'] = request.get('template_var', None)
        return super().__call__(request)


@Route(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context[self.context_object_name]['courses'] = site.courses
        context[self.context_object_name]['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_id = int(data['course_id'])
        course = site.get_course(course_id)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)

    def __call__(self, request):
        logger.log(f'Добавление студента на курс')
        self.queryset['site'] = request.get('template_var', None)
        return super().__call__(request)


@Route(routes, '/contact/')
class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', objects_list={'site': request.get('template_var', None)})


@Route(routes, '/create_test/')
class CreateTestData:
    def __call__(self, request):
        # site.create_test_data()

        new_category1 = Engine.create_category('Программирование', None)
        site.categories.append(new_category1)
        new_category2 = Engine.create_category('Рисование', None)
        site.categories.append(new_category2)
        new_category3 = Engine.create_category('Базы данных', new_category1)
        site.categories.append(new_category3)
        new_category5 = Engine.create_category('Красками', new_category2)
        site.categories.append(new_category5)
        new_category = Engine.create_category('SQL', new_category3)
        site.categories.append(new_category)
        new_category = Engine.create_category('Карандашом', new_category2)
        site.categories.append(new_category)
        new_category = Engine.create_category('NonSQL', new_category3)
        site.categories.append(new_category)
        new_category4 = Engine.create_category('Python', new_category1)
        site.categories.append(new_category4)
        hierarchy_categories = site.hierarchy_categories

        print(f'created test data len {len(hierarchy_categories)}')

        course = site.create_course('interactive', 'Базовый курс Python', new_category4, 'www.ru')
        course.observers.append(email_notifier)
        course.observers.append(sms_notifier)
        site.courses.append(course)
        course = site.create_course('offline', 'Виды красок', new_category5, 'Москва')
        site.courses.append(course)

        new_st = site.create_user('student', 'Вася')
        site.students.append(new_st)

        return '200 OK', 'Test data created. Go to <a href="/">main page</a>'


class ErrPageNotFound404:
    def __call__(self, request):
        return '404 Not Found', '404 PAGE Not Found'


# можно добавить роутинг и так
routes['Err404'] = ErrPageNotFound404()
