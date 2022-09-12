from datetime import date

import logging
import logs.log_config

LOG = logging.getLogger('server_log')


# front controller
def secret_front(request, environ=None):
    request['date'] = date.today()


def title_front(request, environ=None):
    request['title'] = 'Тестовый сайт'


def log_front(request, environ=None):
    if environ:
        LOG.info(f'{environ["REMOTE_ADDR"]} {environ["REQUEST_METHOD"]} {environ["PATH_INFO"]}')
    return

fronts = [secret_front, title_front, log_front]

if __name__ == '__main__':
    LOG.info('run fronts')
