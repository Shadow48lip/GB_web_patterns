from jinja2 import Template
from os.path import join


def render(template_name, folder='templates', **kwargs):
    """
    Пропускает данные представления через шаблон.
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон, default templates
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    file_path = join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path, encoding='utf-8') as f:
        # Читаем шаблон
        template = Template(f.read())
    # Рендер шаблона с использованием параметров из представления
    return template.render(**kwargs)
