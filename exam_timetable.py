import xlrd

book = xlrd.open_workbook("exam_timetable.xls")
sh = book.sheet_by_index(0)
columns_number = sh.ncols


def get_timetable(group_name):
    for i in range(columns_number):
        if sh.cell_value(5, i) == group_name:
            for j in range(6, 39):
                if sh.cell_value(j, i) != '':
                    with open('exam.txt', 'a') as file:
                        file.write(sh.cell_value(j, 1)+' ')
                        file.write(sh.cell_value(j, i)+'\n')
