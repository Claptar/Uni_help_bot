import pickle

import openpyxl
import timetable


def timetable_by_course(file_name):
    """
    Функция для считывания расписания курса из файла .xslx с несколькими листами (sheets)
    :param file_name: имя файла с расписанием
    :return: добавляет в список groups pd.DataFrame с расписанием курса
    """
    course = openpyxl.load_workbook(file_name)
    for sheet in course.worksheets:
        timetable.get_timetable(sheet)


# Считываем расписание из экселевских файлов в базу данных
# меняем их на новые в каждом семе, при замене, возможно, нужно внести правки в функцию timetable.get_timetable()
def insert_timetables_to_database(first_course, last_course, name_of_file: str):
    # openpyxl умеет работать только с файлами формата .xslx, не .xsl
    for i in range(first_course, last_course + 1):
        timetable_by_course('{}-{}.xlsx'.format(i, name_of_file))


def insert_sixth_course(departments):
    for department in departments:
        timetable_by_course('6-kurs-osen-{}-2020.xlsx'.format(department))


if __name__ == '__main__':
    insert_timetables_to_database(1, 5, 'kurs-osen-2020')
    insert_timetables_to_database(1, 3, 'kurs-osen-2020-do')
    insert_sixth_course(['faki', 'fupm'])
    with open('blank_timetable.pickle', 'rb') as handle:
        alumni = pickle.load(handle)
    timetable.insert_update_group_timetable(
        'ALUMNI',
        alumni
    )
