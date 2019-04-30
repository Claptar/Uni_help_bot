import numpy as np

b = np.array([[1,2,3],[4,5,6]])


def table_body_create(data_array, name):

    data_array = data_array.T

    lines_number = data_array.shape[0]
    columns_number = data_array.shape[1]

    print('В вашей таблице число столбцов равно', columns_number, '.', '\n',
          'Введите зашоловок для каждого:')

    lines_names = []

    for ln in range(columns_number):
        lines_names.append(str(input()))

    print('\\begin{table}[h!])', '\n', '\\begin{center}')

    print('\\begin{tabular}{', end='')

    for number in range(columns_number):
        print('|c', end='')
    print('|}')

    for ln in range(lines_number):
        print("\hline")
        if ln == 0:
            for cn in range(columns_number - 1):
                print(lines_names[cn], '&', ' ', end='')
            print(lines_names[columns_number - 1], '\\\\')

            print("\hline")

            for cn in range(columns_number - 1):
                print(data_array[ln, cn], '&', ' ', end='')
            print(data_array[ln, columns_number - 1], '\\\\')

        else:
            for cn in range(columns_number - 1):
                print(data_array[ln, cn], '&', ' ', end='')
            print(data_array[ln, columns_number - 1], '\\\\')
    print('\hline \n',
          '\\end{tabular} \n',
          '\\caption{' + str(name) + '} \n',
          '\\end{center} \n \\end{table}')


#table_regular_expression(b, 'table')
table_body_create(b, 'table')
