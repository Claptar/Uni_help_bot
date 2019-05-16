import tkinter as tk
import argparse
import math_part
import latex_table
import numpy as np
from tkinter import filedialog as fd
from PIL import Image, ImageTk

root = tk.Tk()
root.title("MNK-Tool")
root.geometry("800x600")


def close():
    root.destroy()


def OK():
    help_window.destroy()


def help():
    global help_window
    help_window = tk.Toplevel(root)
    help_window.geometry("400x400")



    poetry = " НАПИСАТЬ ТЕКСТ ПОДСКАЗКИ.\n Вот мысль, которой весь я предан,\nИтог всего, что ум скопил.\nЛишь тот, кем бой за жизнь изведан,\nЖизнь и свободу заслужил."
    tk.Label(help_window, text=poetry).place(relx=0.2, rely=0.3)

    tk.Button(help_window, text="OK", background="#555", foreground="#ccc", command=OK).place(relheight=0.1,
                        relwidth=0.2, relx=0.4, rely=0.9)


def back():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry("800x600")
    start(root)


def standard_button():
    # настроить кртинку
    tk.Label(root, text="Пожалуйста, сделай таблицу Excel такой", font="Arial 14").place(relheight=0.05, relwidth=0.5, relx=0.43, rely=0)
    img = Image.open("examplegr.png")
    render = ImageTk.PhotoImage(img)
    initil = tk.Label(root, image=render)
    initil.image = render
    initil.place(relheight=0.75, relwidth=0.75, relx=0.3, rely=0.05)

    btnback = tk.Button(text="Назад", background="#555", foreground="#ccc",
                        padx="15", pady="6", font="15", command=back)
    btnback.place(relheight=0.2, relwidth=0.33, relx=0, rely=0.8)

    btnhelp = tk.Button(text="Помощь", background="#555", foreground="#ccc",
                        padx="15", pady="6", font="15", command=help)
    btnhelp.place(relheight=0.2, relwidth=0.33, relx=0.33, rely=0.8)

    btnclose = tk.Button(text="Выход", background="#555", foreground="#ccc",
                         padx="15", pady="6", font="15", command=close)
    btnclose.place(relheight=0.2, relwidth=0.34, relx=0.66, rely=0.8)


def openfileMNK():
    file_name = fd.askopenfilename()
    mnk_calculate_print(file_name)

def mnk_calculate_print(file_name):
    xy_list = math_part.mnk_calc(file_name)
    a = xy_list[0]
    d_a = xy_list[2]
    b = xy_list[1]
    d_b =xy_list[3]
    # исправить подписи
    sigmaX = "Погрешность коэффициента наклона прямой:", a, "+", d_a
    sigmaY = "Погрешность свободного коэффициента:", b, "+", d_b
    tk.Label(root, text=sigmaX).place(relx=0.2, rely=0.7)
    tk.Label(root, text=sigmaY).place(relx=0.2, rely=0.75)

def generation_tab_MNK():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry("800x600")

    standard_button()

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=openfileMNK)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.0, rely=0.3)


def openfileTable():
    file_name = fd.askopenfilename()
    Table(file_name)


def Table(file_name):
    data_array = np.array(math_part.data_conv(file_name))
    name = "table"
    latex_table.table_body_create(data_array, name)


def generation_tab_Table():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry("800x600")

    standard_button()

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=openfileTable)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.0, rely=0.3)


def openfilePlots():
    file_name = fd.askopenfilename()
    x_lb = x1.get()
    y_lb = y1.get()
    tit = Name.get()
    math_part.plot_drawer(file_name, x_lb, y_lb, tit)


def generation_tab_Plots():
    global root, x1, y1, Name
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry("800x600")

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

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=openfilePlots)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.1)









def Table(file_name):
    data_array = np.array(math_part.data_conv(file_name))
    name = "table"
    latex_table.table_body_create(data_array, name)

def start(root):

    btn1 = tk.Button(text="Построить график", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=generation_tab_Plots)
    btn1.place(relheight=0.2, relwidth=1.0, relx=0, rely=0)

    btn2 = tk.Button(text="Посчитать МНК", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=generation_tab_MNK)
    btn2.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.2)

    btn3 = tk.Button(text="Создать PDF Overleaf", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15")
    btn3.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.4)

    btn4 = tk.Button(text="Создать табллицу в LaTex", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=generation_tab_Table)
    btn4.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.6)

    btn5 = tk.Button(text="...", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15")
    btn5.place(relheight=0.2, relwidth=0.33, relx=0, rely=0.8)

    btn6 = tk.Button(text="Помощь", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=help)
    btn6.place(relheight=0.2, relwidth=0.33, relx=0.33, rely=0.8)

    btn7 = tk.Button(text="Выход", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=close)
    btn7.place(relheight=0.2, relwidth=0.34, relx=0.66, rely=0.8)

start(root)

root.mainloop()