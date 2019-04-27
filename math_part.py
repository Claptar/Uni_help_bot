import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def plt_const(x, y):
    """
    Функция рассчитывает по МНК коэффициенты прямой по полученным координатам точек. Так же рассчитывает их погрешности.
    :param x: Массив абсцисс точек
    :param y: Массив оридинат точек
    :return: [значение углового коэфф a, значение коэфф b, значение погрешности a, значение погрешности b]
    """
    av_x = np.sum(x)/len(x)
    av_y = np.sum(y)/len(y)
    sigmas_x = np.sum(x*x)/len(x) - (np.sum(x)/len(x))**2
    sigmas_y = np.sum(y*y)/len(y) - (np.sum(y)/len(y))**2
    R = np.sum(x*y)/len(x) - av_x*av_y
    a = R/sigmas_x
    b = av_y - a*av_x
    d_a = 2*math.sqrt((sigmas_y/sigmas_x - a**2)/(len(x)-2))
    d_b = d_a*math.sqrt(sigmas_x + av_x**2)
    x_ = range(0, x[len(x) -1]//1 + 2)
    return [a, b, d_a, d_b]


def plot_drawer(data_file,x_lb, y_lb, tit):
    """
    Функция считывает данные из таблицы и строит графики с МНК по этим данным
    :param data_file: Название файла с данными
    :param x_lb: подпись оси абсцисс
    :param y_lb: оси ординат
    :param tit: название графика
    :return:
    """
    dataset = pd.read_excel(data_file, header=None)
    d = np.array(dataset)
    strk = 'plt.plot('
    a = []
    b = []
    x = []
    y = []
    for i in range(0, len(d[1, :] - 1), 2):
        r = plt_const(d[:, i], d[:, i + 1])
        x.append(d[:, i])
        y.append(d[:, i + 1])
        a.append(r[0])
        b.append(r[1])
    print(len(x), len(a), len(b))
    for i in range(0, len(x)):
        strk += 'x[{}], y[{}], \' ro \', np.array([min(x[{}]), max(x[{}])]),' \
                ' a[{}]*np.array([min(x[{}]), max(x[{}])]) + b[{}],'.format(i, i, i, i, i, i, i, i)
        print(i)
    strk = strk[0:-1] + ')'
    print(strk)
    eval(strk)
    plt.xlabel(x_lb)
    plt.ylabel(y_lb)
    plt.title(tit)
    plt.grid(True)
    plt.show()


plot_drawer('data.xlsx', 'time', 'velocity', 'plot_testing')