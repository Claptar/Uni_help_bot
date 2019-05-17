import xlrd

book_exam = xlrd.open_workbook("timetable/exam_timetable.xls")
sh_exam = book_exam.sheet_by_index(0)
columns_number_exam = sh_exam.ncols

book_class = xlrd.open_workbook("timetable/class_timetable.xls")
sh_class = book_class.sheet_by_index(0)
columns_number_class = sh_class.ncols


def get_exam_timetable(group_name):
    """
    Записывает в файл расписание экзаменов по номеру группу
    :param group_name: номер группы
    :return:
    """
    for i in range(columns_number_exam):
        if sh_exam.cell_value(5, i) == group_name:
            for j in range(6, 39):
                if sh_exam.cell_value(j, i) != '':
                    with open('timetable/exam.txt', 'a') as file:
                        file.write(sh_exam.cell_value(j, 1)+' ')
                        file.write(sh_exam.cell_value(j, i)+'\n')


def get_timetable(group_name, weekday):
    """
    Записывает в файл расписание по номеру группу и дне недели
    :param group_name: номер группы
    :param weekday: день недели
    :return:
    """
    row_day = {'Понедельник': 5, 'Вторник': 13, 'Среда': 21, 'Четверг': 29, 'Пятница': 37, 'Суббота': 45}
    for i in range(columns_number_class):
        if sh_class.cell_value(4, i) == group_name:
            for j in range(row_day[weekday], row_day[weekday] + 7):
                if sh_class.cell_value(j, i) != '':
                    with open('timetable/class.txt', 'a') as file:
                        file.write(sh_class.cell_value(j, 1)+' ')
                        file.write(sh_class.cell_value(j, i)+'\n')

