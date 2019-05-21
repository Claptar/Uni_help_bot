# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np

b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


def table_body_create(data_array, name):
    """

    :param data_array: массив данных, по которым строится таблица
    :param name: имя таблицы
    :return:
    """

    data_array = data_array.T

    lines_number = data_array.shape[0]
    columns_number = data_array.shape[1]

    lines_names = []

    print(' В таблице число строк -', lines_number, '\n',
          'число столбцов -', columns_number, '\n',
          'Введите название для каждого столбца:')

    for ln in range(columns_number):
        lines_names.append(str(input()))

    data_array = np.vstack((lines_names, data_array))
    print(data_array)

    print('Хотите оставить текущий формат?[Д/н]:')
    answer = input()

    if answer == 'н':
        data_array = data_array.T

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


#table_body_create(b, 'table')
