from datetime import date

# import logging
# import logs.log_config
#
# LOG = logging.getLogger('server_log')
from engine import Logger

logger = Logger('server')


# front controller
# def secret_front(request, environ=None):
#     request['date'] = date.today()
#
#
# def title_front(request, environ=None):
#     request['title'] = 'Тестовый сайт'


def template_variables(request, environ=None):
    request['template_var'] = {
        'title': 'Тестовый сайт',
        'date': date.today(),
        'menu': request['path'],
    }


# Используем собственный модуль
def log_front(request, environ=None):
    if environ:
        # LOG.info(f'{environ["REMOTE_ADDR"]} {environ["REQUEST_METHOD"]} {environ["PATH_INFO"]}')
        logger.log(f'{environ["REMOTE_ADDR"]} {environ["REQUEST_METHOD"]} {environ["PATH_INFO"]}')
    return


fronts = [template_variables, log_front]

if __name__ == '__main__':
    # LOG.info('run fronts')
    logger.log('run fronts')
