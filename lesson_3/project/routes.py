from views import Index, Contact, ErrPageNotFound404

routes = {
    '/': Index(),
    '/contact/': Contact(),
    'Err404': ErrPageNotFound404(),
}
