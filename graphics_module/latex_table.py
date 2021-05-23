# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np


def create_data_array(file, name):
    data_array = np.array(file)
    data = []
    for i in range(data_array.shape[0]):
        m = []
        for j in range(data_array.shape[1]):
            m.append(data_array[i][j])
        data.append(m)
    stringg = table_body_create(data, name)
    return stringg


def table_body_create(data_array, name):
    """

    :param data_array: массив данных, по которым строится таблица
    :param name: имя таблицы
    :return:
    """
    global main_string

    column_names = data_array[:1]
    data_array = data_array[1:]

    data_array = np.array(data_array)

    data_array = np.vstack((column_names, data_array))

    lines_number = data_array.shape[0]
    columns_number = data_array.shape[1]

    main_string = "\\begin{table}[h!] \n \t \\begin{center} \n \t\t \\begin{tabular}{"

    for number in range(columns_number):
        main_string += "|c"
    main_string += "|} \n"

    for ln in range(lines_number):
        main_string += r"\hline" + "\n"

        for cn in range(columns_number - 1):
            main_string = main_string + "\t\t\t" + str(data_array[ln, cn]) + " " + "&"

        main_string = (
            main_string
            + "\t\t\t"
            + str(data_array[ln, columns_number - 1])
            + " "
            + "\\\\"
            + "\n"
        )

    main_string = (
        main_string
        + r"\hline"
        + "\n \t\t \\end{tabular} \n \t\t \\caption{"
        + str(name)
        + "} \n \t \\end{center} \n\\end{table}"
    )

    return main_string
