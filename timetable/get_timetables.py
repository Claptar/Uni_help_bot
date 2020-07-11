import openpyxl
import timetable


def timetable_by_course(file_name):
    """
    Функция для считывания расписания курса из файла .xslx с несколькими листами (sheets)
    :param file_name: имя файла с расписанием
    :param course: номер курса
    :return: добавляет в список groups pd.DataFrame с расписанием курса
    """
    course = openpyxl.load_workbook(file_name)
    for sheet in course.worksheets:
        timetable.get_timetable(sheet)


# Считываем расписание из экселевских файлов в базу данных
# меняем их на новые в каждом семе, при замене, возмножно, нужно внести правки в функцию timetable.get_timetable()
for i in range(1, 6):
    timetable_by_course('{}-kurs-vesna-2019_2020.xlsx'.format(i))
