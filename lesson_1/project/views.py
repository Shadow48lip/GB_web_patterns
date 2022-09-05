from mouse_fm.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', site_title=request.get('title', None), date=request.get('date', None))


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', site_title=request.get('title', None), date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'


class ErrPageNotFound404:
    def __call__(self, request):
        return '404 Not Found', '404 PAGE Not Found'
