import asyncio
import os
import datetime
import sys

import aiopg
import psycopg2
# from psycopg2 import errorcodes

DBNAME = os.environ['DATABASE']
USER = os.environ['USER']
PASS = os.environ['PASS']
HOST = os.environ['HOST']
# PORT = os.environ['PORT']

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def print_psycopg2_exception(err):
    """
    Функция, печатающая информацию об ошибке.
    """
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occurred
    line_num = traceback.tb_lineno

    # print the poolect() error
    print("\n\n\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    # print("\nextensions.Diagnostics:", err.diag) if hasattr(err, 'diag') else print()

    # print the pgcode and pgerror exceptions
    # print("\npgerror:", err.pgerror) if hasattr(err, 'pgerror') else print()
    # print("pgcode:", err.pgcode, '-', errorcodes.lookup(err.pgcode), "\n") if hasattr(err, 'pgcode') else print()


def sync_get_connection():
    """
    Функция для проверки соединения (синхронная).
    :return: pool или False, если соединение не было установлено.
    """
    try:  # пробуем подключиться
        conn = psycopg2.connect(
            dbname=DBNAME,
            user=USER,
            password=PASS,
            host=HOST
        )
    except (OSError, TimeoutError, ConnectionError) as err:  # ловим ошибку, если не удалось подключиться
        last_err = err  # если соединение не установлено
        print_psycopg2_exception(err)
    else:
        return conn
    raise last_err


def sync_insert_update_value_in_table(sql_command: str, *args) -> tuple:
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
        conn = sync_get_connection()
        with conn.cursor() as cur:
            cur.execute(
                sql_command,
                args
            )
    # если при записи произошла ошибка, то возвращаем False + разделяем ошибки соединения и другие ошибки
    except (OSError, TimeoutError, ConnectionError) as err:
        print_psycopg2_exception(err)
        return False, 'connection_error'
    except Exception as err:
        print_psycopg2_exception(err)
        return False, 'other_error'
    else:
        conn.commit()
        conn.close()
        return True, ''


def sync_select_value_from_table(sql_command: str, *args) -> tuple:
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
        conn = sync_get_connection()
        with conn.cursor() as cur:
            cur.execute(
                sql_command,
                args
            )
            result = conn.fetchone()  # (SMTH_0, SMTH_1, ..., SMTH_(k-1), )
    # если при записи произошла ошибка, то возвращаем False + разделяем ошибки соединения и другие ошибки
    except (OSError, TimeoutError, ConnectionError) as err:
        print_psycopg2_exception(err)
        return False, 'connection_error'
    except Exception as err:
        print_psycopg2_exception(err)
        return False, 'other_error'
    else:
        conn.commit()
        conn.close()
        if result is None:
            return False, 'empty_result'
        else:
            return True, result


def sync_insert_group(group_num, timetable, exam=False):
    """
    Функция, добавляющая в таблицу Group пару номер группы - расписание группы.
    :param group_num: номер группы из расписания
    :param timetable: расписание для группы
    :param exam: если True, то обновляется расписание экзаменов группы
    :return:
    """
    if exam:
        return sync_insert_update_value_in_table(
            """INSERT INTO "Group" (name, exam_timetable) VALUES (%s, %s)""",
            group_num,
            timetable
        )
    else:
        return sync_insert_update_value_in_table(
            """INSERT INTO "Group" (name, group_timetable) VALUES (%s, %s)""",
            group_num,
            timetable
        )


def sync_update_group(group_num, timetable, exam=False, school=None):
    """
    Функция, обновляющая в таблице Group расписание группы для введенной группы.
    :param group_num: номер группы из расписания
    :param timetable: новое расписание для группы
    :param exam: если True, то обновляется расписание экзаменов группы
    :param school: Физтех-школа
    :return:
    """
    if exam:
        if school is None:
            return sync_insert_update_value_in_table(
                """UPDATE "Group" SET exam_timetable = %s WHERE "Group".name = %s""",
                timetable,
                group_num
            )
        else:
            return sync_insert_update_value_in_table(
                """UPDATE "Group" SET exam_timetable = %s, school_id = """
                """(SELECT school_id FROM "School" WHERE "School".name = %s) WHERE "Group".name = %s""",
                timetable,
                school,
                group_num
            )
    else:
        return sync_insert_update_value_in_table(
            """UPDATE "Group" SET group_timetable = %s WHERE "Group".name = %s""",
            timetable,
            group_num
        )


async def get_connection():
    """
    Функция для проверки соединения.
    :return: connection или False, если соединение не было установлено.
    """
    try:  # пробуем подключиться
        conn = await aiopg.connect(
            dbname=DBNAME,
            user=USER,
            password=PASS,
            host=HOST
        )
    except (OSError, TimeoutError, ConnectionError) as err:  # ловим ошибку, если не удалось подключиться
        last_err = err  # если соединение не установлено
        print_psycopg2_exception(err)
    else:
        return conn
    raise last_err


async def insert_update_value_in_table(sql_command: str, *args) -> tuple:
    """
    Функция для вставки или обновления значения в таблице.
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
        conn = await get_connection()
        async with conn.cursor() as cur:
            await cur.execute(
                sql_command,
                args
            )
    # если при записи произошла ошибка, то возвращаем False + разделяем ошибки соединения и другие ошибки
    except (OSError, TimeoutError, ConnectionError) as err:
        print_psycopg2_exception(err)
        return False, 'connection_error'
    except Exception as err:
        print_psycopg2_exception(err)
        return False, 'other_error'
    else:
        conn.close()
        return True, ''


async def select_value_from_table(sql_command: str, *args) -> tuple:
    """
    Функция для выбора значения из таблицы.
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
        conn = await get_connection()
        async with conn.cursor() as cur:
            await cur.execute(
                sql_command,
                args
            )
            result = await cur.fetchone()  # (SMTH_0, SMTH_1, ..., SMTH_(k-1), )
    # если при записи произошла ошибка, то возвращаем False + разделяем ошибки соединения и другие ошибки
    except (OSError, TimeoutError, ConnectionError) as err:
        print_psycopg2_exception(err)
        return False, 'connection_error'
    except Exception as err:
        print_psycopg2_exception(err)
        return False, 'other_error'
    else:
        conn.close()
        if result is None:
            return False, 'empty_result'
        else:
            return True, result


async def insert_group(group_num, timetable):
    """
    Функция, добавляющая в таблицу Group пару номер группы - расписание группы.
    :param group_num: номер группы из расписания
    :param timetable: расписание для группы
    :return:
    """
    return await insert_update_value_in_table(
        """INSERT INTO "Group" (name, group_timetable) VALUES (%s, %s)""",
        group_num,
        timetable
    )


async def update_group(group_num, timetable):
    """
    Функция, обновляющая в таблице Group расписание группы для введенной группы.
    :param group_num: номер группы из расписания
    :param timetable: новое расписание для группы
    :return:
    """
    return await insert_update_value_in_table(
        """UPDATE "Group" SET group_timetable = %s WHERE "Group".name = %s""",
        timetable,
        group_num
    )


async def insert_user(chat_id, group_num):
    """
    Функция, добавляющая в таблицу User пользователя с номером чата chat_id и группой group_num.
    :param chat_id: id чата с пользователем
    :param group_num: номер группы пользователя
    (по умолчанию - расписание группы), иначе в таблицу заносится значение NULL (None)
    :return:
    """
    return await insert_update_value_in_table(
        """INSERT INTO "User" (chat_id, group_id) """
        """VALUES (%s, (SELECT group_id FROM "Group" WHERE "Group".name = %s))""",
        chat_id,
        group_num
    )


async def update_user(chat_id, group_num: str
                      # update_custom=False
                      ):
    """
    Функция для обновления данных пользователя по его желанию.
    :param chat_id: id чата с пользователем
    :param group_num: номер группы пользователя
    # :param update_custom: если True, то user_timetable заменяется на таблицу, соответствующую новой группе.
    :return:
    """
    # if update_custom:
    #     return await insert_update_value_in_table(
    #         """UPDATE "User" SET (group_id, user_timetable) = """
    #         """((SELECT group_id FROM "Group" WHERE "Group".name = %s), """
    #         """(SELECT group_timetable FROM "Group" WHERE "Group".name = %s)) """
    #         """WHERE chat_id = %s""",
    #         group_num,
    #         group_num,
    #         chat_id
    #     )
    # else:
    return await insert_update_value_in_table(
        """UPDATE "User" SET group_id = """
        """(SELECT group_id FROM "Group" WHERE "Group".name = %s) """
        """WHERE chat_id = %s""",
        group_num,
        chat_id
    )


async def send_timetable(custom=False, my_group=False, chat_id=None, another_group=None):
    """
    Функция, возвращающая нужное пользователю расписание.
    Могут быть варианты (custom=True, my_group=False, chat_id=SMTH_IN_"User"),
                        (custom=False, my_group=True, chat_id=SMTH_IN_"User"),
                        (custom=False, my_group=False, another_group=SMTH_IN_"Group")
    :param custom: если True, то возвращается кастомное расписание пользователя
    :param my_group: если True, то возвращается расписание группы пользователя
    :param chat_id: id чата с пользователем
    (по умолчанию None - для просмотра расписания любой группы без записи в базу данных)
    :param another_group: str или None
    если is not None, то возвращается расписание этой группы по запросу пользователя
    :return:
    """
    if custom:
        return await select_value_from_table(
            """SELECT user_timetable FROM "User" WHERE "User".chat_id = %s""",
            chat_id
        )
    elif my_group:
        return await select_value_from_table(
            """SELECT group_timetable FROM "Group" """
            """WHERE (SELECT group_id FROM "User" WHERE "User".chat_id = %s) = "Group".group_id""",
            chat_id
        )
    elif another_group is not None:
        return await select_value_from_table(
            """SELECT group_timetable FROM "Group" WHERE "Group".name = %s""",
            another_group
        )
    # 1) result == (SMTH - может быть None, ),
    # если result == (None, ), то этот пользователь не завел кастомное расписание
    # 2) result is None, если такого пользователя нет в базе, или такой группы не нашлось (another_group)


async def send_exam_timetable(my_group=False, chat_id=None, another_group=None):
    """
    Функция, возвращающая нужное пользователю расписание экзаменов.
    :param my_group: если True, то возвращается расписание экзаменов группы пользователя
    :param chat_id: id чата с пользователем
    (по умолчанию None - для просмотра расписания экзаменов любой группы без записи в базу данных)
    :param another_group: str или None
    если is not None, то возвращается расписание этой группы по запросу пользователя
    :return:
    """
    if my_group:
        return await select_value_from_table(
            """SELECT exam_timetable FROM "Group" """
            """WHERE (SELECT group_id FROM "User" WHERE "User".chat_id = %s) = "Group".group_id""",
            chat_id
        )
    elif another_group is not None:
        return await select_value_from_table(
            """SELECT exam_timetable FROM "Group" WHERE "Group".name = %s""",
            another_group
        )


async def update_custom_timetable(chat_id, timetable):
    """
    Функция для обновления кастомного расписания пользователя.
    :param timetable: новое кастомное расписание
    :param chat_id: id чата с пользователем
    :return:
    """
    return await insert_update_value_in_table(
        """UPDATE "User" SET user_timetable = %s WHERE chat_id = %s""",
        timetable,
        chat_id
    )


async def create_custom_timetable(chat_id):
    """
    Функция для обновления кастомного расписания пользователя.
    :param chat_id: id чата с пользователем
    :return:
    """
    return await insert_update_value_in_table(
        """UPDATE "User" SET user_timetable = """
        """(SELECT group_timetable FROM "Group" JOIN "User" """
        """ON "Group".group_id = "User".group_id WHERE chat_id = %s) """
        """WHERE chat_id = %s""",
        chat_id,
        chat_id  # вот ЗДЕСЬ проебался
    )


async def check_user_group(chat_id):
    """
    Функция по chat_id пользователя возвращает значение его номера группы.
    :param chat_id: id чата с пользователем
    :return: Номер группы (формат как в расписании),
    записанный в базе данных, или None, если такого пользователя нет в базе.
    """
    res = await select_value_from_table(
        """SELECT name FROM "Group" """
        """WHERE (SELECT group_id FROM "User" WHERE "User".chat_id = %s) = "Group".group_id""",
        chat_id
    )
    return res
    # 1) result == (SMTH - не может быть None, )
    # 2) result is None, если такого пользователя нет в базе


async def get_user_info(chat_id):
    """
    Функция по chat_id пользователя проверяет, есть ли он в базе данных или нет.
    Выдает информацию о нем в положительном случае.
    :param chat_id: id чата с пользователем
    :return: строка из базы данных с информацией о пользователе (group_id, user_timetable)
    """
    return await select_value_from_table(
        """SELECT group_id, user_timetable FROM "User" WHERE "User".chat_id = %s""",
        chat_id
    )
    # 1) result == (SMTH - не может быть None, )
    # 2) result is None, если такого пользователя нет в базе


async def insert_action(command_name, user_id):
    """
    Функция, записывающая событие, вызванное пользователем, в базу данных.
    :param command_name: Название события
    :param user_id: id пользователя вызвавшего событие
    :return:
    """
    now = datetime.datetime.now()
    return await insert_update_value_in_table(
        """INSERT INTO "actions" (date_time, command_name, user_id) """
        """VALUES (%s, %s, %s)""",
        now,
        command_name,
        user_id
    )
