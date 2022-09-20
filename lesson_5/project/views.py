from pprint import pprint
from mouse_fm.templator import render
from engine import Logger, Engine
from patterns.structure_deco import Debug, Route

logger = Logger('views')
site = Engine()

routes = {}


@Route(routes, '/')
class Index:
    def __call__(self, request):
        """ Контроллер - главная страница """
        logger.log('Load Index')
        [print(item.__dict__) for item in site.categories]

        category_tree = []
        for item in site.categories:
            pass

        return '200 OK', render('index.html', site=request.get('template_var', None),
                                categories=site.categories)


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

            return '200 OK', render('index.html', site=request.get('template_var', None),
                                    categories=site.categories)
        else:
            return '200 OK', render('create_category.html', site=request.get('template_var', None),
                                    categories=site.categories)


@Route(routes, '/category-list/')
class CategoryList:
    """ Контроллер - список категорий """

    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', site=request.get('template_var', None),
                                categories=site.categories)


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
                site.courses.append(course)
                courses = filter(lambda item: (item.category.id == category.id), site.courses)

                return '200 OK', render('course_list.html', site=request.get('template_var', None),
                                        cources_list=courses,
                                        cat_name=category.name, id=category.id)
            else:
                self.category_id = int(request['get_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', site=request.get('template_var', None),
                                        name=category.name, id=category.id)
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

            return '200 OK', render('course_list.html', site=request.get('template_var', None),
                                    cources_list=courses, cat_name=category.name, id=category.id)
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
            new_course.category.courses_count += 1
            site.courses.append(new_course)

            return '200 OK', render('course_list.html', site=request.get('template_var', None),
                                    cources_list=site.courses, cat_name=new_course.category.name,
                                    id=new_course.category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
        except Exception as e:
            return '200 OK', f'Error: {e}'


@Route(routes, '/contact/')
class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', site=request.get('template_var', None))


@Route(routes, '/create_test/')
class CreateTestData:
    def __call__(self, request):
        site.create_test_data()
        return '200 OK', 'Test data created'


class ErrPageNotFound404:
    def __call__(self, request):
        return '404 Not Found', '404 PAGE Not Found'


# можно добавить роутинг и так
routes['Err404'] = ErrPageNotFound404()
