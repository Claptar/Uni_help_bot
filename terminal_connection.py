import argparse
import math_part

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--figure",
                    help="Argument induces function which creates graphic with names of axises",
                    action="store_true")


args = parser.parse_args()


if args.figure:
    print('Введите название файла:')
    file_name = input()

    print('Введите название графика:')
    graf_tit = input()

    print('Хотите сделать подписи к осям? [Д/н]:')
    answer = input()

    if answer == 'Д':
        print('Введите название оси X:')
        name_x = input()

        print('Введите название оси Y:')
        name_y = input()

        math_part.plots_drawer(file_name, name_x, name_y, graf_tit)

    else:
        math_part.plots_drawer(file_name, '', '', graf_tit)







