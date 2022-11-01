from tkinter import *
import tkinter.ttk as ttk
import sqlite3

import random
from   random import randint
from   random import choice

w = 1

class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, width = w, anchor=CENTER)

        for row in rows:
            table.insert('', END, values=tuple(row))

        scrolltable = Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)

root = Tk()
root.title("Генерация модельной базы знаний")
root.geometry("1200x800")
root["bg"] = "AliceBlue"

conn = sqlite3.connect('mbz.db')
cur = conn.cursor()

# Входные параметры
COUNT_CLASS = 2
COUNT_FEATURES = 2

MIN_COUNT_VALUES_FEATURES = 2
MAX_COUNT_VALUES_FEATURES = 2

MIN_COUNT_PERIOD = 1
MAX_COUNT_PERIOD = 5

MIN_DURATION_PERIOD = 1
MAX_DURATION_PERIOD = 24




# Функции
def gen_classes():
    global COUNT_CLASS
    global conn
    global cur

    for i in range(1, COUNT_CLASS + 1):
        name_class = "class" + str(i)
        cur.execute('INSERT INTO classes(ID, name_class) VALUES(?, ?)', (str(i), name_class,))
        conn.commit()

        with sqlite3.connect('mbz.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM classes")
            data = (row for row in cursor.fetchall())

        global w
        w = 100
        table = Table(root, headings=('ID', 'Название класса'), rows=data)
        table.grid(row = 2, columnspan = 2, padx = 2, pady = 20)

def gen_features():
    global COUNT_FEATURES
    global conn
    global cur

    for i in range(1, COUNT_FEATURES + 1):
        name_features = "feature" + str(i)
        cur.execute('INSERT INTO features(ID, name_features) VALUES(?, ?)', (str(i), name_features,))
        conn.commit()

        with sqlite3.connect('mbz.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM features")
            data = (row for row in cursor.fetchall())

        global w
        w = 120
        table = Table(root, headings=('ID', 'Название признака'), rows=data)
        table.grid(row = 2, column = 2, columnspan = 2, padx = 2, pady = 20)



def Generate():
    global COUNT_CLASS
    global COUNT_FEATURES
    global cur
    global conn

    COUNT_CLASS = int(e1.get())
    COUNT_FEATURES = int(e2.get())

    # Удаление и повторное создание таблицы c классами
    cur.execute('DROP table if exists classes')
    conn.commit()

    cur.execute("CREATE TABLE classes(ID integer, name_class text)")
    conn.commit()

    # Удаление и повторное создание таблицы c признаками
    cur.execute('DROP table if exists features')
    conn.commit()

    cur.execute("CREATE TABLE features (ID integer, name_features text)")
    conn.commit()

    gen_classes()
    gen_features()





# Интерфейс

l1 = Label(text="Количество классов:", font="Times 12", bg="AliceBlue")
e1 = Entry(width=5, font="Times 12")

l1.grid(row=0, column=0)
e1.grid(row=0, column=1, pady=10, padx=10)

l2 = Label(text="Количество признаков:", font="Times 12", bg="AliceBlue")
e2 = Entry(width=5, font="Times 12")

l2.grid(row=0, column=2)
e2.grid(row=0, column=3, pady=10, padx=10)


l3 = Label(text="Кол-во возможных \n значений признаков:", font="Times 12", bg="AliceBlue")
e3 = Entry(width=5, font="Times 12")

l3.grid(row=0, column=4)
e3.grid(row=0, column=5, pady=10, padx=10)

l4 = Label(text="Ограничение на число \n периодов в динамики:", font="Times 12", bg="AliceBlue")
e4 = Entry(width=5, font="Times 12")

l4.grid(row=0, column=6)
e4.grid(row=0, column=7, pady=10, padx=10)

l5 = Label(text="Ограничение на нижнюю \n границу периода:", font="Times 12", bg="AliceBlue")
e5 = Entry(width=5 , font="Times 12")

l5.grid(row=0, column=8)
e5.grid(row=0, column=9, pady=10, padx=10)


button_gen = Button(text="Генерация МБЗ", font="Times 12", bg="white", command = Generate)
button_gen.grid(row=1, column=4, columnspan=2, pady=30)

root.mainloop()
