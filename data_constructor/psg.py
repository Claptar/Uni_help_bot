import psycopg2
from psycopg2 import OperationalError, errorcodes
import sys

config = {'connection_string': 'dbname=d35o9bn6qjau2u '
                               'user=yxnigwjuiafqql '
                               'password=1c2787f4a7bb154a724accb47df8e6ad049d8825faa3f8a0f5c128ded8c56f4f '
                               'host=ec2-54-195-247-108.eu-west-1.compute.amazonaws.com '
                               'port=5432'}


def print_psycopg2_exception(err):
    """
    Функция, печатающая информацию об ошибке.
    """
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occurred
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag) if hasattr(err, 'diag') else print()

    # print the pgcode and pgerror exceptions
    print("\npgerror:", err.pgerror) if hasattr(err, 'pgerror') else print()
    print("pgcode:", err.pgcode, '-', errorcodes.lookup(err.pgcode), "\n") if hasattr(err, 'pgcode') else print()


def get_connection():
    """
    Функция для проверки соединения.
    :return: connection или False, если соединение не было установлено.
    """
    try:  # пробуем подключиться
        conn = psycopg2.connect(config['connection_string'])
        return conn
    except OperationalError as err:  # ловим ошибку, если не удалось подключиться
        print_psycopg2_exception(err)
        return None  # если соединение не установлено


def insert_group(group_num, timetable):
    """
    Функция, добавляющая в таблицу Group пару номер группы - расписание группы.
    :param group_num: номер группы из расписания
    :param timetable: расписание для группы
    :return: True, если добавление прошло успешно, или False, если что-то пошло не так.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO "Group" (name, group_timetable) VALUES(%s, %s)""",
            (group_num, timetable)
        )
    except Exception as err:  # если при записи произошла ошибка, то возвращаем False
        print_psycopg2_exception(err)
        return False
    conn.commit()  # если все хорошо, подтверждаем транзакцию
    cur.close()
    conn.close()
    return True


def insert_user(chat_id, group_num):
    """
    Функция, добавляющая в таблицу User пользователя с номером чата chat_id и группой group_num.
    :param chat_id: id чата с пользователем
    :param group_num: номер группы пользователя
    (по умолчанию - расписание группы), иначе в таблицу заносится значение NULL (None)
    :return:
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO "User" (chat_id, group_id) """
            """VALUES(%s, (SELECT group_id FROM "Group" WHERE "Group".name = %s))""",
            (chat_id, group_num)
        )
    except Exception as err:
        print_psycopg2_exception(err)
        return False
    conn.commit()
    cur.close()
    conn.close()
    return True


def update_user(chat_id, group_num: str, update_custom: bool):
    """
    Функция для обновления данных пользователя по его желанию.
    :param chat_id: id чата с пользователем
    :param group_num: номер группы пользователя
    :param update_custom: если True, то user_timetable заменяется на таблицу, соответствующую новой группе.
    :return:
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        if update_custom:
            cur.execute(
                """UPDATE "User" SET (group_id, user_timetable) = """
                """((SELECT group_id FROM "Group" WHERE "Group".name = %s), """
                """(SELECT group_timetable FROM "Group" WHERE "Group".name = %s)) """
                """WHERE chat_id = %s""",
                (group_num, group_num, chat_id)
            )
        else:
            cur.execute(
                """UPDATE "User" SET group_id = """
                """(SELECT group_id FROM "Group" WHERE "Group".name = %s) """
                """WHERE chat_id = %s""",
                (group_num, chat_id)
            )
    except Exception as err:
        print_psycopg2_exception(err)
        return False
    conn.commit()
    cur.close()
    conn.close()
    return True


def update_custom_timetable(chat_id, timetable):
    """
    Функция для обновления кастомного расписания пользователя.
    :param timetable: новое кастомное расписание
    :param chat_id: id чата с пользователем
    :return:
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """UPDATE "User" SET user_timetable = %s WHERE chat_id = %s""",
            (timetable, chat_id)
        )
    except Exception as err:
        print_psycopg2_exception(err)
        return False
    conn.commit()
    cur.close()
    conn.close()
    return True


def send_timetable(custom: bool, my_group: bool, chat_id=None, another_group=None):
    """
    Функция, возвращающая нужное пользователю расписание.
    Могут быть варианты (custom=True, my_group=False, chat_id=SMTH_IN_"User"),
                        (custom=False, my_group=True, chat_id=SMTH_IN_"User"),
                        (custom=False, my_group=False, another_group=SMTH_IN_"Group")
    :param custom: если True, то возвращается кастомное расписание пользователя
    :param my_group: если True, то возвращается расписание группы пользователя
    :param chat_id: id чата с пользователем (по умолчанию None - для просмотра расписания любой группы
                                                                              без записи в базу данных)
    :param another_group: str или None
    если не None, то возвращается расписание другой группы по запросу пользователя
    :return: timetable: (pickle file или None, ) или None
    """
    # расписание группы должно быть в виде (SMTH, ) ( в том числе может быть (None, ) )
    # если оно None ( не (None, ) ), то SELECT не нашел его
    result = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        if custom:
            cur.execute(
                """SELECT user_timetable FROM "User" WHERE "User".chat_id = %s""",
                [chat_id]
            )
            result = cur.fetchone()
        elif my_group:
            cur.execute(
                """SELECT group_timetable FROM "Group" """
                """WHERE (SELECT group_id FROM "User" WHERE "User".chat_id = %s) = "Group".group_id""",
                [chat_id]
            )
            result = cur.fetchone()
        elif another_group is not None:
            cur.execute(
                """SELECT group_timetable FROM "Group" WHERE "Group".name = %s""",
                [another_group]
            )
            result = cur.fetchone()
    except Exception as err:
        print_psycopg2_exception(err)
        return False
    cur.close()
    conn.close()
    # 1) result == (SMTH - может быть None, ),
    # если result == (None, ), то этот пользователь не завел кастомное расписание
    # 2) result is None, если такого пользователя нет в базе, или такой группы не нашлось (another_group)
    return result


def check_user_group(chat_id):
    """
    Функция по chat_id пользователя возвращает значение его номера группы.
    :param chat_id: id чата с пользователем
    :return: Номер группы, записанный в базе данных, или None, если такого пользователя нет в базе.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT name FROM "Group" """
            """WHERE (SELECT group_id FROM "User" WHERE "User".chat_id = %s) = "Group".group_id""",
            [chat_id]
        )
        result = cur.fetchone()  # (group_num, )
    except Exception as err:
        print_psycopg2_exception(err)
        return False
    cur.close()
    conn.close()
    # 1) result == (SMTH - не может быть None, )
    # 2) result is None, если такого пользователя нет в базе
    return result


def get_user_info(chat_id):
    """
    Функция по chat_id пользователя проверяет, есть ли он в базе данных или нет.
    Выдает информацию о нем в положительном случае.
    :param chat_id: id чата с пользователем
    :return: строка из базы данных с информацией о пользователе
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT (group_id, user_timetable) FROM "User" WHERE "User".chat_id = %s""",
            [chat_id]
        )
        result = cur.fetchone()  # (group_num, )
    except Exception as err:
        print_psycopg2_exception(err)
        return False
    cur.close()
    conn.close()
    # 1) result == (SMTH - не может быть None, )
    # 2) result is None, если такого пользователя нет в базе
    return result
