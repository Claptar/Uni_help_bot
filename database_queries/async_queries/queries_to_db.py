from .base_queries import insert_update_value_in_table, select_value_from_table

import datetime


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
        timetable,
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
        group_num,
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
        group_num,
    )


async def update_user(chat_id, group_num: str):
    """
    Функция для обновления данных пользователя по его желанию.
    :param chat_id: id чата с пользователем
    :param group_num: номер группы пользователя
    # :param update_custom: если True, то user_timetable заменяется на таблицу, соответствующую новой группе.
    :return:
    """
    return await insert_update_value_in_table(
        """UPDATE "User" SET group_id = """
        """(SELECT group_id FROM "Group" WHERE "Group".name = %s) """
        """WHERE chat_id = %s""",
        group_num,
        chat_id,
    )


async def send_timetable(
    custom=False, my_group=False, chat_id=None, another_group=None
):
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
            """SELECT user_timetable FROM "User" WHERE "User".chat_id = %s""", chat_id
        )
    elif my_group:
        return await select_value_from_table(
            """SELECT group_timetable FROM "Group" """
            """WHERE (SELECT group_id FROM "User" WHERE "User".chat_id = %s) = "Group".group_id""",
            chat_id,
        )
    elif another_group is not None:
        return await select_value_from_table(
            """SELECT group_timetable FROM "Group" WHERE "Group".name = %s""",
            another_group,
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
            chat_id,
        )
    elif another_group is not None:
        return await select_value_from_table(
            """SELECT exam_timetable FROM "Group" WHERE "Group".name = %s""",
            another_group,
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
        chat_id,
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
        chat_id,  # вот ЗДЕСЬ проебался
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
        chat_id,
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
        chat_id,
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
        user_id,
    )
