from jinja2 import FileSystemLoader
from jinja2.environment import Environment



def render(template_name, folder='templates', **kwargs):
    """
    Пропускает данные представления через шаблон.
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон, default templates
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # создаем объект окружения
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)
