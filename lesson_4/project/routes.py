from views import *

routes = {
    '/': Index(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/copy-course/': CopyCourse(),
    '/contact/': Contact(),
    'Err404': ErrPageNotFound404(),
}
