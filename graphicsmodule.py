import tkinter as tk
from math_module import math_part
import latex_table
import pandas as pd
import Overleaf_connection
from tkinter import filedialog as fd
from PIL import Image, ImageTk

root = tk.Tk()

root.title("MNK-Tool")
characteristic = "900x600"
root.geometry(characteristic)


def close():
    root.destroy()


def OK():
    help_window.destroy()


def help():
    global help_window
    help_window = tk.Toplevel(root)
    help_window.geometry("400x400")



    poetry = "ОПИСАТЬ ПОМОЩЬ"
    tk.Label(help_window, text=poetry).place(relx=0.2, rely=0.3)

    tk.Button(help_window, text="OK", background="#555", foreground="#ccc", command=OK).place(relheight=0.1,
                        relwidth=0.2, relx=0.4, rely=0.9)


def back():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)
    start(root)


def help_image_mnk_plot():
    # настроить кртинку
    tk.Label(root, text="Пожалуйста, сделай таблицу Excel такой", font="Arial 14").place(relheight=0.05, relwidth=0.5,
                                                                                         relx=0.43, rely=0)
    img = Image.open("examplegr.png")
    render = ImageTk.PhotoImage(img)
    initil = tk.Label(root, image=render)
    initil.image = render
    initil.place(relheight=0.75, relwidth=0.75, relx=0.3, rely=0.05)

def help_image_table():
    # настроить кртинку
    tk.Label(root, text="Пожалуйста, сделай таблицу Excel такой", font="Arial 14").place(relheight=0.05, relwidth=0.5,
                                                                                         relx=0.43, rely=0)
    img = Image.open("exampletb.png")
    render = ImageTk.PhotoImage(img)
    initil = tk.Label(root, image=render)
    initil.image = render
    initil.place(relheight=0.75, relwidth=0.75, relx=0.3, rely=0.05)

def standard_button():

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
    a = round(xy_list[0][0], 4)
    d_a = round(xy_list[2][0], 4)
    b = round(xy_list[1][0], 4)
    d_b = round(xy_list[3][0], 4)

    sigma = tk.Text(width=12, height=12)
    sigma.place(relheight=0.1, relwidth=0.4, relx=0, rely=0.4)
    sigma.insert(1.0, f'Погрешность коэффициента наклона прямой: \n{a} + {d_a}'
                          f' \nПогрешность коэффициента наклона прямой: \n{b} + {d_b} ')


def generation_tab_MNK():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)

    standard_button()
    help_image_mnk_plot()

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=openfileMNK)
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

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=openfilePlots)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.1)


def openfileTable():
    file_name = fd.askopenfilename()
    Table(file_name)


def generation_tab_Table():
    global root, TableName
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)

    standard_button()
    help_image_table()

    btnfile = tk.Button(text="Выбрать файл", background="#555", foreground="#ccc",
                        padx="15", pady="6", font="15", command=openfileTable)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.1)

    tk.Label(root, text="Название графика:").place(relheight=0.05, relwidth=0.15, relx=0, rely=0.33)
    TableName = tk.Entry(root, width=8)
    TableName.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.33)


def Table(file_name):
    file = pd.read_excel(file_name, header=None)
    name = TableName.get()
    string = latex_table.create_data_array(file, name)
    sigma = tk.Text(width=12, height=12)
    sigma.place(relheight=0.6, relwidth=0.4, relx=0, rely=0.4)

    sigma.insert(1.0, string)



def openfileOverleaf():
    e_mail = email.get()
    passw_ord = password.get()
    file = fd.askopenfilename()
    file = open(file, 'r')
    file_lines = file.read()
    print(file_lines)
    Overleaf_connection.ol_open(file_lines, e_mail, passw_ord)

def generation_tab_Overleaf_connection():
    global root, email, password
    root.destroy()
    root = tk.Tk()
    root.title("MNK-Tool")
    root.geometry(characteristic)

    standard_button()

    tk.Label(root, text="E-mail").place(relheight=0.05, relwidth=0.15, relx=0, rely=0.33)
    email = tk.Entry(root, width=8)
    email.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.33)

    tk.Label(root, text="Пароль:").place(relheight=0.05, relwidth=0.15, relx=0, rely=0.4)
    password = tk.Entry(root, width=8)
    password.place(relheight=0.05, relwidth=0.2, relx=0.15, rely=0.4)



    btnfile = tk.Button(text="Выбрать текстовый файл", background="#555", foreground="#ccc",
                        padx="15", pady="6", font="15", command=openfileOverleaf)
    btnfile.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.1)

def start(root):

    btn1 = tk.Button(text="Построить график", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=generation_tab_Plots)
    btn1.place(relheight=0.2, relwidth=1.0, relx=0, rely=0)

    btn2 = tk.Button(text="Посчитать МНК", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=generation_tab_MNK)
    btn2.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.2)

    btn3 = tk.Button(text="Создать PDF Overleaf", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=generation_tab_Overleaf_connection)
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