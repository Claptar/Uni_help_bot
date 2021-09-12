from ..create_env import DBNAME, USER, PASS, HOST
from .error_catcher import print_psycopg2_exception

import aiopg


async def get_connection():
    """
    Функция для проверки соединения.
    :return: connection или False, если соединение не было установлено.
    """
    try:  # пробуем подключиться
        conn = await aiopg.connect(
            dbname=DBNAME, user=USER, password=PASS, host=HOST, enable_hstore=False
        )
    except OSError as err:  # ловим ошибку, если не удалось подключиться
        last_err = err  # если соединение не установлено
        print_psycopg2_exception(err, __file__, __name__)
    else:
        return conn
    raise last_err
