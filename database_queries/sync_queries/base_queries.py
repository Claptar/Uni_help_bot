from ..establish_connection import sync_connection, print_psycopg2_exception


def insert_update_value_in_table(sql_command: str, *args) -> tuple:
    """
    Функция для вставки или обновления значения в таблице. (синхронная)
    :param sql_command: строка с командой к базе данных.
    :param args: значения, которые вставляются в строку с командой (вместо %s)
    :return: tuple, содержащий 2 значения.
    Первое - True/False - это маркер успешного завершения операции.
    Второе - str
    В случае True это '' (пустая строка)
    В случае False -
    1) 'connection_error', если произошла ошибка при подключении
    2) 'other_error', если произошла ошибка при выполнении самой команды
    В случае возникновения ошибки информация о ней печатается с помощью функции print_psycopg2_exception().
    """
    try:
        conn = sync_connection()
        with conn.cursor() as cur:
            cur.execute(sql_command, args)
    # если при записи произошла ошибка, то возвращаем False + разделяем ошибки соединения и другие ошибки
    except OSError as err:
        print_psycopg2_exception(err, __file__, __name__)
        return False, "connection_error"
    except Exception as err:
        print_psycopg2_exception(err, __file__, __name__)
        return False, "other_error"
    else:
        conn.commit()
        conn.close()
        return True, ""


def select_value_from_table(sql_command: str, *args) -> tuple:
    """
    Функция для выбора значения из таблицы. (синхронная)
    :param sql_command: строка с командой к базе данных.
    :param args: значения, которые вставляются в строку с командой (вместо %s)
    :return: tuple, содержащий 2 значения.
    Первое - True/False - это маркер успешного завершения операции.
    Второе - str или tuple
    В случае True это
    1) найденное значение (tuple, в котором максимальный индекс равен k-1 при запросе k значений)
    В случае False -
    1) 'connection_error', если произошла ошибка при подключении
    2) 'other_error', если произошла ошибка при выполнении самой команды
    3) 'empty_result', если SELECT не нашел таких значений в таблице
    В случае возникновения ошибки информация о ней печатается с помощью функции print_psycopg2_exception().
    """
    try:
        conn = sync_connection()
        with conn.cursor() as cur:
            cur.execute(sql_command, args)
            result = conn.fetchone()  # (SMTH_0, SMTH_1, ..., SMTH_(k-1), )
    # если при записи произошла ошибка, то возвращаем False + разделяем ошибки соединения и другие ошибки
    except OSError as err:
        print_psycopg2_exception(err, __file__, __name__)
        return False, "connection_error"
    except Exception as err:
        print_psycopg2_exception(err, __file__, __name__)
        return False, "other_error"
    else:
        conn.commit()
        conn.close()
        if result is None:
            return False, "empty_result"
        else:
            return True, result
