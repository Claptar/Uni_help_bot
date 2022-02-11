from helpers import insert_update_group_timetable
from read_all_timetables_from_file import (
    get_all_timetable_from_file,
    get_all_exam_timetable_from_file,
    blank_timetable,
)

from pathlib import Path

import openpyxl


def insert_all_timetable_from_file_to_database(file_name, exam=False):
    """
    Функция для считывания расписания курса из файла .xlsx с несколькими листами (sheets)
    :param file_name: имя файла с расписанием
    :param exam: True, если нужно вставить расписание экзаменов
    :return: добавляет в список groups pd.DataFrame с расписанием курса
    """
    course = openpyxl.load_workbook(file_name)
    for sheet in course.worksheets:
        timetables = (
            get_all_exam_timetable_from_file(sheet)
            if exam
            else get_all_timetable_from_file(sheet)
        )
        for group, group_timetable in timetables:
            if not any(group.startswith(symbol) for symbol in {"М", "Б", "С"}):
                print(group, group_timetable, file_name)
                continue
            insert_update_group_timetable(group, group_timetable, exam=exam)


# Считываем расписание из экселевских файлов в базу данных
# меняем их на новые в каждом семе, при замене, возможно, нужно внести правки в функцию timetable.get_timetable()
def insert_semester_timetables_from_files_to_database(
    first_course, last_course, distant=False, faculty=None
):
    # openpyxl умеет работать только с файлами формата .xlsx или .xlsm, не .xls
    distant = "-do" if distant else ""
    faculty = "" if faculty is None else "-" + faculty
    for i in range(first_course, last_course + 1):
        insert_all_timetable_from_file_to_database(
            Path(__file__).parent
            / "timetable_files"
            / "semester"
            / f"{i}-kurs{distant}{faculty}.xlsx"
        )


def insert_exam_timetables_from_files_to_database():
    folder_path = Path(__file__).parent / "timetable_files" / "sessiya"
    for i in range(1, 6):
        insert_all_timetable_from_file_to_database(
            folder_path / f"{i}-kurs.xlsx", exam=True
        )


if __name__ == "__main__":
    command = ""
    while command not in {"семестр", "сессия"}:
        print('Введите команду: "Семестр" или "Сессия"')
        command = input().lower()
    if command == "семестр":
        insert_semester_timetables_from_files_to_database(1, 5)

        # insert_semester_timetables_from_files_to_database(
        #     6, 6, faculty="faki"
        # )  # есть только в нечетных семестрах
        # insert_semester_timetables_from_files_to_database(
        #     6, 6, faculty="fpmi"
        # )  # есть только в нечетных семестрах

        # особенность 2020 года
        # insert_semester_timetables_from_files_to_database(
        #     1, 3, distant=True
        # )

        insert_update_group_timetable("ALUMNI", blank_timetable)
    elif command == "сессия":
        # TODO: пересмотреть, когда придет сессия
        insert_exam_timetables_from_files_to_database()
