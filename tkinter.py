from tkinter import *

root = Tk()
root.title("MNK-Tool")
root.geometry("800x600")




def OK():
    help_window.destroy()

def close():
    root.destroy()

def help():
    global help_window
    help_window = Toplevel(root)
    help_window.geometry("400x400")



    poetry = " НАПИСАТЬ ТЕКСТ ПОДСКАЗКИ.\n Вот мысль, которой весь я предан,\nИтог всего, что ум скопил.\nЛишь тот, кем бой за жизнь изведан,\nЖизнь и свободу заслужил."
    Label(help_window, text=poetry).place(relx=0.2, rely=0.3)

    Button(help_window, text="OK", background="#555", foreground="#ccc", command=OK).place(relheight=0.1,
                        relwidth=0.2, relx=0.4, rely=0.9)



def back():
    global root
    root.destroy()
    root = Tk()
    root.title("MNK-Tool")
    root.geometry("800x600")
    start(root)


def MNK():
    global root
    root.destroy()
    root = Tk()
    root.title("MNK-Tool")
    root.geometry("800x600")


    btn = Button(text="Назад", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=back)
    btn.place(relheight=0.2, relwidth=0.33, relx=0, rely=0.8)

    btnhelp = Button(text="Помощь", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=help)
    btnhelp.place(relheight=0.2, relwidth=0.33, relx=0.33, rely=0.8)

    btn7 = Button(text="Выход", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=close)
    btn7.place(relheight=0.2, relwidth=0.34, relx=0.66, rely=0.8)







def start(root):

    # Построить график
    btn1 = Button(text="Clicks 0", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15")
    btn1.place(relheight=0.2, relwidth=1.0, relx=0, rely=0)

    btn2 = Button(text="Посчитать МНК", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15",  command=MNK)
    btn2.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.2)

    btn3 = Button(text="Создать PDF Overleaf", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15")
    btn3.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.4)

    btn4 = Button(text="TOP", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15")
    btn4.place(relheight=0.2, relwidth=1.0, relx=0, rely=0.6)

    btn5 = Button(text="...", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15")
    btn5.place(relheight=0.2, relwidth=0.33, relx=0, rely=0.8)

    btn6 = Button(text="Помощь", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=help)
    btn6.place(relheight=0.2, relwidth=0.33, relx=0.33, rely=0.8)

    btn7 = Button(text="Выход", background="#555", foreground="#ccc",
                  padx="15", pady="6", font="15", command=close)
    btn7.place(relheight=0.2, relwidth=0.34, relx=0.66, rely=0.8)

start(root)

root.mainloop()