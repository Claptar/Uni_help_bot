from .base_queries import insert_update_value_in_table


def insert_group(group_num, timetable, exam=False):
    """
    Функция, добавляющая в таблицу Group пару номер группы - расписание группы.
    :param group_num: номер группы из расписания
    :param timetable: расписание для группы
    :param exam: если True, то обновляется расписание экзаменов группы
    :return:
    """
    if exam:
        return insert_update_value_in_table(
            """INSERT INTO "Group" (name, exam_timetable) VALUES (%s, %s)""",
            group_num,
            timetable,
        )
    else:
        return insert_update_value_in_table(
            """INSERT INTO "Group" (name, group_timetable) VALUES (%s, %s)""",
            group_num,
            timetable,
        )


def update_group(group_num, timetable, exam=False, school=None):
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
            return insert_update_value_in_table(
                """UPDATE "Group" SET exam_timetable = %s WHERE "Group".name = %s""",
                timetable,
                group_num,
            )
        else:
            return insert_update_value_in_table(
                """UPDATE "Group" SET exam_timetable = %s, school_id = """
                """(SELECT school_id FROM "School" WHERE "School".name = %s) WHERE "Group".name = %s""",
                timetable,
                school,
                group_num,
            )
    else:
        return insert_update_value_in_table(
            """UPDATE "Group" SET group_timetable = %s WHERE "Group".name = %s""",
            timetable,
            group_num,
        )
