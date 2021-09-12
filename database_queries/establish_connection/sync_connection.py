from ..create_env import DBNAME, USER, PASS, HOST
from .error_catcher import print_psycopg2_exception

import psycopg2


def get_connection():
    """
    Функция для проверки соединения (синхронная).
    :return: pool или False, если соединение не было установлено.
    """
    try:  # пробуем подключиться
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASS, host=HOST)
    except OSError as err:  # ловим ошибку, если не удалось подключиться
        last_err = err  # если соединение не установлено
        print_psycopg2_exception(err, __file__, __name__)
    else:
        return conn
    raise last_err
