import tkinter as tk
from math_module import math_part
from graphics_module import latex_table
import pandas as pd
from tkinter.font import Font
from tkinter import filedialog as fd
import PIL
import os
PATH = os.path.abspath('')

root = tk.Tk()

root.title("MNK-Tool")
characteristic = "900x600"
root.geometry(characteristic)


def close():
    root.destroy()


def OK():
    """f
    Функция закрывает окно с подсказкой
    """
    help_window.destroy()


def help_button():
    """
    Функция вызывается при нажатии кропки "помощь", генерирует дополнительное окно, содержащее вспомогательную
    информацию, считываемую из текстового файла
    """
    global help_window
    help_window = tk.Toplevel(root)
    help_window.geometry("600x600")
    text = tk.Text(help_window, width=100, height=100, font=Font(family='Helvetica', size=10))
    text.pack(expand='yes', fill='both')

    with open(f'{PATH}/graphics_module/Help.txt', mode="r") as f:
        text.insert('end', f.read())

    tk.Button(help_window, text="OK", background="#555", foreground="#ccc", command=OK).place(relheight=0.1,
                                                                                              relwidth=0.2, relx=0.8,
                                                                                              rely=0.9)


def back():
    """
    Функция возвращает пользователя на главный экран, она уничтожает текуший экран и вызывает генерацию гланого
    """
    global root
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)
    start(root)


def help_image_calc_error():
    """
    Функция создает и размещант картинку-помошника для построения МНК и графика
    """
    tk.Label(root, text="Пожалуйста, заполните поля по образцу", font="Arial 14").place(relheight=0.05, relwidth=0.5,
                                                                                         relx=0.4, rely=0)

    tk.Label(root, text="Изпользуйте следующие операции при вводе уравнения:\n "
                        "+ – сложение\n"
                        "- – вычитание\n"
                        "* – умножение\n"
                        "/ – деление\n"
                        "** – возведение в степень\n"
                        "Можете использовать () – скобки при надобности", font="Arial 10").place(relheight=0.2,
                        relwidth=0.4, relx=0.5, rely=0.37)

    img = PIL.Image.open(f'{PATH}/graphics_module/help_calc_error.png')
    render = PIL.ImageTk.PhotoImage(img)
    initil = tk.Label(root, image=render)
    initil.image = render
    initil.place(relheight=0.3, relwidth=0.7, relx=0.33, rely=0.05)

    img1 = PIL.Image.open(f'{PATH}/graphics_module/derivative.gif')
    render = PIL.ImageTk.PhotoImage(img1)
    initil1 = tk.Label(root, image=render)
    initil1.image = render
    initil1.place(relheight=0.24, relwidth=0.34, relx=0, rely=0.06)


def help_image_mnk_plot():
    """
    Функция создает и размещант картинку-помошника для построения МНК и графика
    """
    tk.Label(root, text="Пожалуйста, сделайте таблицу Excel такой", font="Arial 14").place(relheight=0.05, relwidth=0.5,
                                                                                         relx=0.43, rely=0)
    img = PIL.Image.open(f'{PATH}/graphics_module/examplegr.png')
    render = PIL.ImageTk.PhotoImage(img)
    initil = tk.Label(root, image=render)
    initil.image = render
    initil.place(relheight=0.75, relwidth=0.75, relx=0.3, rely=0.05)


def help_image_table():
    """
    Функция создает и размещает картинку-помошника для создания таблицы
    """
    tk.Label(root, text="Пожалуйста, сделайте таблицу Excel такой", font="Arial 14").place(relheight=0.05, relwidth=0.5,
                                                                                         relx=0.43, rely=0)
    img = PIL.Image.open(f'{PATH}/graphics_module/exampletb.png')
    render = PIL.ImageTk.PhotoImage(img)
    initil = tk.Label(root, image=render)
    initil.image = render
    initil.place(relheight=0.75, relwidth=0.75, relx=0.3, rely=0.05)


def standard_button():
    """
    Функция возвращает генериует стандартный набор кнопок (нижняя панель)
    """
    btnback = tk.Button(text="Назад", background="#555", foreground="#ccc",
                        padx="15", pady="6", font="15", command=back)
    btnback.place(relheight=0.2, relwidth=0.33, relx=0, rely=0.8)

    btnhelp = tk.Button(text="Помощь", background="#555", foreground="#ccc",
                        padx="15", pady="6", font="15", command=help_button)
    btnhelp.place(relheight=0.2, relwidth=0.33, relx=0.33, rely=0.8)

    btnclose = tk.Button(text="Выход", background="#555", foreground="#ccc",
                         padx="15", pady="6", font="15", command=close)
    btnclose.place(relheight=0.2, relwidth=0.34, relx=0.66, rely=0.8)


def openfileMNK():
    """
    Функция открывает выбранный пользователем файл и вызывает функцию обработчик
    """
    try:
        file_name = fd.askopenfilename()
        mnk_calculate_print(file_name)
    except Exception as e:
        print(e)


def mnk_calculate_print(file_name):
    """
    Функция принимает данные из открытого файла и вызывает функцию из модуля математики, орабатывает полученные данные,
    выводит их в виде текста
    """
    xy_list = math_part.mnk_calc(file_name)
    a = round(xy_list[0][0], 4)
    d_a = round(xy_list[2][0], 4)
    b = round(xy_list[1][0], 4)
    d_b = round(xy_list[3][0], 4)

    sigma = tk.Text(width=12, height=12)
    sigma.place(relheight=0.2, relwidth=0.4, relx=0, rely=0.4)
    sigma.insert(1.0, f'Погрешность коэффициента наклона прямой: \n{a} + {d_a}'
                 f'\nПогрешность коэффициента наклона прямой: \n{b} + {d_b} ')


def generation_tab_MNK():
    """
    Функция генерирует новый экран для расчета МНК
    """
    global root
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)

    standard_button()
    help_image_mnk_plot()

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=openfileMNK)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.1)


def openfilePlots():
    """
    Функция открывает файл для считывания данных, и считывает данные из полей экрана создания графика, вызыват функцию
    из модуля математики, отвечающуу за построение графиков
    """
    try:
        file_name = fd.askopenfilename()
        x_lb = x1.get()
        y_lb = y1.get()
        linear_val = linear.get()
        cross_val = cross.get()
        tit = Name.get()

        if linear_val:
            if cross_val:
                math_part.ERROR_BAR = True
                math_part.plots_drawer(file_name, x_lb, y_lb, tit)
            else:
                math_part.ERROR_BAR = False
                math_part.plots_drawer(file_name, x_lb, y_lb, tit)
        else:
            math_part.plot_drawer(file_name, x_lb, y_lb, tit)

    except Exception as e:
        print(e)



def generation_tab_Plots():
    """
    Функция генерирует новый экран для построения графика
    """
    global root, x1, y1, Name, linear, cross
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)

    help_image_mnk_plot()
    standard_button()

    tk.Label(root, text="Название графика:").place(relheight=0.05, relwidth=0.15, relx=0, rely=0.33)
    Name = tk.Entry(root, width=8)
    Name.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.33)

    tk.Label(root, text="Название оси Ox:").place(relheight=0.05, relwidth=0.15, relx=0, rely=0.4)
    x1 = tk.Entry(root, width=8)
    x1.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.4)

    tk.Label(root, text="Название оси Oy:").place(relheight=0.05, relwidth=0.15, relx=0, rely=0.47)
    y1 = tk.Entry(root, width=8)
    y1.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.47)

    linear = tk.IntVar()
    linear.set(0)
    fllinear = tk.Checkbutton(text="Линеаризовать график", variable=linear)
    fllinear.place(relheight=0.1, relwidth=0.24, relx=0.05, rely=0.55)

    cross = tk.IntVar()
    cross.set(0)
    flcross = tk.Checkbutton(text="Построить кресты погрешностей", variable=cross)
    flcross.place(relheight=0.1, relwidth=0.3, relx=0.05, rely=0.63)

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=openfilePlots)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.1)


def openfileTable():
    """
    Функция открывает файл для считывания данных и передает его функции Table
    """
    try:
        file_name = fd.askopenfilename()
        Table(file_name)
    except Exception as e:
        print(e)


def generation_tab_Table():
    """
    Функция генерирует новый экран для создания таблиц
    """
    global root, TableName
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)

    standard_button()
    help_image_table()

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                        padx="15", pady="6", font="15", command=openfileTable)
    btnfile.place(relheight=0.06, relwidth=0.2, relx=0.1, rely=0.02)

    tk.Label(root, text="Название графика:").place(relheight=0.05, relwidth=0.15, relx=0, rely=0.12)
    TableName = tk.Entry(root, width=8)
    TableName.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.12)


def Table(file_name):
    """
    Функция принимает файл и считывает название табицы из поля на экране создания таблиц
    """
    file = pd.read_excel(file_name, header=None)
    name = TableName.get()
    string = latex_table.create_data_array(file, name)
    table = tk.Text(width=12, height=12)
    table.place(relheight=0.6, relwidth=0.35, relx=0, rely=0.17)

    table.insert(1.0, string)


def ErrorCalculate():
    equation_ls = equation.get()  # cчитывание из первого окошка
    variables_ls = variables.get().split(', ')  # считывание из второго окошка
    values_ls = [float(elem) for elem in values.get().split(', ')]  # считывание из третьего
    error_ls = [float(elem) for elem in error.get().split(', ')]  # считывание из четвертого
    value = math_part.error_calc(equation_ls, variables_ls, values_ls, error_ls)

    sigma = tk.Text(width=12, height=12)
    sigma.place(relheight=0.1, relwidth=0.4, relx=0.5, rely=0.6)
    sigma.insert(1.0, f'Погрешность : {value}')


def generation_tab_Error_Calculate():
    global root, equation, variables, values, error
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)

    standard_button()
    help_image_calc_error()

    tk.Label(root, text="Уравнение", anchor="w").place(relheight=0.05, relwidth=0.2, relx=0.02, rely=0.35)
    equation = tk.Entry(root, width=8)
    equation.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.35)

    tk.Label(root, text="Список переменных", anchor="w").place(relheight=0.05, relwidth=0.2, relx=0.02, rely=0.42)
    variables = tk.Entry(root, width=8)
    variables.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.42)

    tk.Label(root, text="Список значений", anchor="w").place(relheight=0.05, relwidth=0.2, relx=0.02, rely=0.49)
    values = tk.Entry(root, width=8)
    values.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.49)

    tk.Label(root, text="Список погрешностей", anchor="w").place(relheight=0.05, relwidth=0.2, relx=0.02, rely=0.56)
    error = tk.Entry(root, width=8)
    error.place(relheight=0.05, relwidth=0.2, relx=0.2, rely=0.56)

    btncalculate = tk.Button(text="Рассчитать", background="#555", foreground="#ccc",
                             padx="15", pady="6", font="15", command=ErrorCalculate)
    btncalculate.place(relheight=0.1, relwidth=0.2, relx=0.11, rely=0.65)


def start(root):
    """
    Функция генерирует главный экран
    """

    btn1 = tk.Button(text="Построить график", background="#555", foreground="#ccc",
                     padx="15", pady="6", font="15", command=generation_tab_Plots)
    btn1.place(relheight=0.2, relwidth=1.0, relx=0, rely=0)

    btn2 = tk.Button(text="Посчитать МНК", background="#555", foreground="#ccc",
                     padx="15", pady="6", font="15", command=generation_tab_MNK)
    btn2.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.2)

    btn3 = tk.Button(text="Посчитать погрешность методом частных производных", background="#555", foreground="#ccc",
                     padx="15", pady="6", font="15", command=generation_tab_Error_Calculate)
    btn3.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.4)

    btn4 = tk.Button(text="Создать табллицу в LaTex", background="#555", foreground="#ccc",
                     padx="15", pady="6", font="15", command=generation_tab_Table)
    btn4.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.6)

    btn5 = tk.Button(text="...", background="#555", foreground="#ccc",
                     padx="15", pady="6", font="15")
    btn5.place(relheight=0.2, relwidth=0.33, relx=0, rely=0.8)

    btn6 = tk.Button(text="Помощь", background="#555", foreground="#ccc",
                     padx="15", pady="6", font="15", command=help_button)
    btn6.place(relheight=0.2, relwidth=0.33, relx=0.33, rely=0.8)

    btn7 = tk.Button(text="Выход", background="#555", foreground="#ccc",
                     padx="15", pady="6", font="15", command=close)
    btn7.place(relheight=0.2, relwidth=0.34, relx=0.66, rely=0.8)


start(root)

root.mainloop()
