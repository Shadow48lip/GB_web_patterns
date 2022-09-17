from wsgiref.simple_server import make_server
from mouse_fm.main import Framework
from routes import routes
from fronts import fronts

application = Framework(routes, fronts)

with make_server('', 8000, application) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()