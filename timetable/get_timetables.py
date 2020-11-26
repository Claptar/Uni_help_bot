import pickle

import openpyxl
import timetable


def timetable_by_course(file_name, exam=False):
    """
    Функция для считывания расписания курса из файла .xslx с несколькими листами (sheets)
    :param file_name: имя файла с расписанием
    :param exam: True, если нужно вставить расписание экзаменов
    :return: добавляет в список groups pd.DataFrame с расписанием курса
    """
    course = openpyxl.load_workbook(file_name)
    for sheet in course.worksheets:
        timetable.get_exam_timetable(sheet) if exam else timetable.get_timetable(sheet)


# Считываем расписание из экселевских файлов в базу данных
# меняем их на новые в каждом семе, при замене, возможно, нужно внести правки в функцию timetable.get_timetable()
def insert_timetables_to_database(first_course, last_course, distant=False, faculty=None):
    # openpyxl умеет работать только с файлами формата .xslx, не .xsl
    distant = '_do' if distant else ''
    faculty = '' if faculty is None else '_' + faculty
    for i in range(first_course, last_course + 1):
        timetable_by_course('semester/{}_kurs{}{}.xlsx'.format(i, distant, faculty))


def insert_exam_timetables():
    for i in range(1, 7):
        timetable_by_course('sessiya/{}_kurs.xlsx'.format(i), exam=True)
    timetable_by_course('sessiya/Spetsialitet.xlsx')


print('Введите команду для заполнения расписания: "Семестр" или "Сессия"')
command = input()
while command not in ['Семестр', 'Сессия']:
    print('Введите верную команду: "Семестр" или "Сессия"')
    command = input()
if command == 'Семестр':
    insert_timetables_to_database(1, 5)
    insert_timetables_to_database(6, 6, faculty='faki')
    insert_timetables_to_database(6, 6, faculty='fupm')
    insert_timetables_to_database(1, 3, distant=True)
    with open('semester/blank_timetable.pickle', 'rb') as handle:
        alumni = pickle.load(handle)
    timetable.insert_update_group_timetable(
        'ALUMNI',
        alumni
    )
elif command == 'Сессия':
    insert_exam_timetables()
