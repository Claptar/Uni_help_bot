import argparse
import math_part

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--figure",
                    help="Argument induces function which creates graphic with names of axises",
                    action="store_true")
parser.add_argument("-s", "--sigma",
                    help="Argument induces function which counts the error",
                    action="store_true")

args = parser.parse_args()


if args.figure:
    print('Введите название файла:')
    figure_file_name = input()

    print('Введите название графика:')
    graf_tit = input()

    print('Хотите сделать подписи к осям? [Д/н]:')
    answer = input()

    if answer == 'Д':
        print('Введите название оси X:')
        name_x = input()

        print('Введите название оси Y:')
        name_y = input()

        math_part.plots_drawer(figure_file_name, name_x, name_y, graf_tit)

    else:
        math_part.plots_drawer(figure_file_name, '', '', graf_tit)


if args.sigma:
    print('Введите имя файла, из которого нужно взять данные:')
    sigma_file_name = input()
    xy_list = math_part.data_conv(sigma_file_name)
    print('Погрешность коэффициента наклона прямой:',
          math_part.const_dev(xy_list[0], xy_list[1])[0],
          '.', '\n',
          'Погрешность свободного коэффициента:',
          math_part.const_dev(xy_list[0], xy_list[1])[1])








