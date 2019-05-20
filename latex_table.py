# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np

b = [['мамы', 'дети'], [1, 10], [2, 11], [3, 12], [4, 13], [5, 14], [6, 15], [7, 16], [8, 20], [9, 25]]



def create_data_array(file, name):
    data_array = np.array(file)
    data = []
    for i in range(data_array.shape[0]):
        m = []
        for j in range(data_array.shape[1]):
            m.append(data_array[i][j])
        data.append(m)
    print(data)
    name = name
    table_body_create(data, name)


def table_body_create(data_array, name):
    """

    :param data_array: массив данных, по которым строится таблица
    :param name: имя таблицы
    :return:
    """

    column_names = data_array[:1]
    print(column_names)
    data_array = data_array[1:]
    print(data_array)

    data_array = np.array(data_array)

    data_array = np.vstack((column_names, data_array))

    lines_number = data_array.shape[0]
    columns_number = data_array.shape[1]



    print(' В таблице число строк -', lines_number, '\n',
          'число столбцов -', columns_number, '\n',)


    lines_number = data_array.shape[0]
    columns_number = data_array.shape[1]

    print('\\begin{table}[h!])', '\n',
          '\t', '\\begin{center}')
    print('\t\t', '\\begin{tabular}{', end='')

    for number in range(columns_number):
        print('|c', end='')
    print('|}')

    for ln in range(lines_number):
        print("\hline")

        for cn in range(columns_number - 1):
            print('\t\t\t', data_array[ln, cn], '&', ' ', end='')
        print('\t\t\t', data_array[ln, columns_number - 1], '\\\\')

    print('\hline \n',
          '\t\t', '\\end{tabular} \n',
          '\t\t', '\\caption{' + str(name) + '} \n',
          '\t', '\\end{center} \n \\end{table}')
nameee = "name"


#table_body_create(b, 'table')
