from pathlib import Path
import sys

# TODO: разобраться с импортом модуля с бд кверями
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from database_queries.sync_queries import insert_group, update_group

import time


def insert_update_group_timetable(group_name: str, timetable: dict, exam=False):
    """
    Функция, вставляющая или обновляющая значение расписания в таблице.
    :param group_name: номер группы
    :param timetable: расписание группы
    :param exam: если True, то обновляется расписание экзаменов группы
    :return:
    """
    insert = insert_group(group_name, timetable, exam=exam)
    timeout = (
        time.time() + 30
    )  # если подключение к серверу длится дольше 30 секунд, то вызываем ошибку
    while not insert[0] and insert[1] == "connection_error":
        insert = insert_group(
            group_name,
            timetable,
            exam=exam,
        )
        if time.time() > timeout:
            raise RuntimeError
    # если возникает какая-то ошибка при вставке, то пробуем обновить значение, а не вставить
    if not insert[0] and insert[1] == "other_error":
        update = update_group(
            group_name,
            timetable,
            exam=exam,
        )
        timeout = (
            time.time() + 30
        )  # если подключение к серверу длится дольше 30 секунд, то вызываем ошибку
        while not update[0] and update[1] == "connection_error":
            update = update_group(
                group_name,
                timetable,
                exam=exam,
            )
            if time.time() > timeout:
                raise RuntimeError
