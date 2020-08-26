# -*- coding: utf-8 -*-
import os

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp

# Переменная, которая хранит путь к директории
PATH = os.path.abspath('')


def is_digit(string):
    """
    Проверка на то, является ли строка числом или нет
    :param string: Подозреваемая строка
    :return: bool
    """
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def data_conv(data_file):
    """
    Программа, которая конвертирует данные из таблицы в массив [x,y]
    :param data_file: название файла
    :return: [x,y]
    """
    data = pd.read_excel(data_file, header=None)
    # Получение столбца с информацией о графиках без NaN объектов
    info = data[0].dropna().values
    label_list = info[0:2]
    legend = info[2:]
    x = data.iloc[:, 1::2].values
    y = data.iloc[:, 2::2].values
    return x, y, label_list, legend


def plt_const(x, y):
    """
    Функция рассчитывает по МНК коэффициенты прямой по полученным координатам точек. Так же рассчитывает их погрешности.
    :param x: Массив абсцисс точек
    :param y: Массив оридинат точек
    :return: [значение углового коэфф a, значение коэфф b, значение погрешности a, значение погрешности b]
    """
    r = (x*y).mean() - x.mean() * y.mean()
    a = r / x.var()
    b = y.mean() - a * x.mean()
    try:
        d_a = 2 * math.sqrt((y.var() / x.var() - a ** 2) / (len(x) - 2))
        d_b = d_a * math.sqrt(x.var() + x.mean() ** 2)
    except Exception as e:
        print(e)
        d_a = 'error'
        d_b = 'error'
    return [a, b, d_a, d_b]


def const_dev(x, y):
    """
    Функция рассчитывает погрешности коэффициентов прямой по полученным координатам точек
    :param x: Массив абсцисс точек
    :param y: Массив оридинат точек
    :return:
    """
    return [plt_const(x, y)[2], plt_const(x, y)[3]]


def plots_drawer(data_file, tit, xerr=0, yerr=0, mnk=False):
    """
    Функция считывает данные из таблицы и строит графики с МНК по этим данным
    :param data_file: Название файла с данными
    :param tit: название графика
    :param xerr: погрешность по х
    :param yerr: погрешность по y
    :param mnk: type Bool, При True строится прямая мнк
    :return: коэфициенты прямых посчитанные по МНК
    """
    fig = plt.figure(dpi=120)
    ax = fig.add_subplot()
    x, y, label_list, legend = data_conv(data_file)
    x_ = []
    coef = []
    for i in range(0, x.shape[1]):
        if xerr != 0 or yerr != 0:
            ax.errorbar(x[:, i], y[:, i], xerr=xerr, yerr=yerr, fmt='k+', capsize=3)
        if x.shape[0] > 15:
            ax.plot(x[:, i], y[:, i], '.')
        else:
            ax.plot(x[:, i], y[:, i], 'o')
        delta = (max(x[:, i]) - min(x[:, i])) / len(x[:, i])
        x_.append([min(x[:, i]) - delta, max(x[:, i]) + delta])
    if mnk:
        for i in range(0, x.shape[1]):
            a, b, da, db = plt_const(x[:, i], y[:, i])
            coef.append([a, b, da, db])
            ax.plot(np.array(x_[i]), a * (np.array(x_[i])) + b, 'r--')
    plot_decor(ax, fig, tit, legend, label_list)
    plt.savefig('plot.pdf')
    plt.savefig('plot.png')
    plt.show()
    plt.clf()
    return coef


def plot_decor(ax, fig, tit, legend, label_list):
    """
    Функция используется для отрисовки оформления графика (сетки, осей и т.д.)
    :param ax:
    :param fig:
    :param tit: название графика
    :param legend: подписи кривых
    :param label_list: подписи осей
    :return:
    """
    ax.set_xlabel(label_list[0])
    ax.set_ylabel(label_list[0])
    ax.legend(legend)
    ax.set_title(tit)
    ax.grid(True)
    # Находим координаты углов графика
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height
    # manual arrowhead width and length
    hw = 1. / 20. * (ymax - ymin)
    hl = 1. / 20. * (xmax - xmin)
    lw = .1  # axis line width
    ohg = 0.25  # arrow overhang
    # compute matching arrowhead length and width
    yhw = hw / (ymax - ymin) * (xmax - xmin) * height / width
    yhl = hl / (xmax - xmin) * (ymax - ymin) * width / height

    # draw x and y axis
    ax.arrow(xmin, ymin, xmax - xmin, 0., fc='k', ec='k', lw=lw,
             head_width=hw / 1.5, head_length=hl / 1.5, overhang=ohg,
             length_includes_head=True, clip_on=False, width=1e-5)

    ax.arrow(xmin, ymin, 0., ymax - ymin, fc='k', ec='k', lw=lw,
             head_width=yhw / 1.5, head_length=yhl / 1.5, overhang=ohg,
             length_includes_head=True, clip_on=False, width=1e-5)
    ax.minorticks_on()
    # Настраиваем основную стеку графика
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    # Добавляем промежуточную сетку
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')


def error_calc(equation, var_list, point_list, error_list):
    """

    :param equation: формула в формате, приемлемом для python
    :param var_list: список переменных
    :param point_list: список значений переменных в точке соответсвенно со списком переменных
    :param error_list: список погрешностей для каждой переменной соответсвенно со списком переменных
    :return: погрешность
    """
    sigma = 0  # Объявляем переменную
    for number in range(len(var_list)):
        elem = sp.Symbol(var_list[number])  # переводит символ в приемлемый формат для дифференцирования
        der = sp.diff(equation, elem)  # дифференцируем выражение equation по переменной elem
        for score in range(len(point_list)):  # задаем каждую переменную, чтобы подставить ее значение
            der = sp.lambdify(var_list[score], der, 'numpy')  # говорим, что функция будет конкретной переменной
            der = der(point_list[score])  # задаем функцию в строчном виде
        sigma += error_list[number] ** 2 * der ** 2  # считем погрешность

    return sigma
