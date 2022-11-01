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

        global w
        i = 0
        for head in headings:
            if i > 0 and w != 30:
                w = 130

            i += 1
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, width=w, anchor=CENTER)

        for row in rows:

            table.insert('', END, values=tuple(row))

        scrolltable = Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)

root = Tk()
root.title("Генерация модельной базы знаний")
root.geometry("1300x800")
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

    COUNT_CLASS = int(e1.get())

    for i in range(1, COUNT_CLASS + 1):
        name_class = "class" + str(i)
        cur.execute('INSERT INTO classes(ID, name_class) VALUES(?, ?)', (str(i), name_class,))
        conn.commit()


    cur.execute("SELECT * FROM classes")
    data = (row for row in cur.fetchall())

    global w
    w = 31
    table = Table(root, headings=('ID', 'Название класса'), rows=data)
    table.grid(row = 2, columnspan = 2, padx = 2, pady = 20)

def gen_features():
    global COUNT_FEATURES
    global conn
    global cur

    COUNT_FEATURES = int(e2.get())

    for i in range(1, COUNT_FEATURES + 1):
        name_features = "feature" + str(i)
        cur.execute('INSERT INTO features(ID, name_features) VALUES(?, ?)', (str(i), name_features,))
        conn.commit()


    cur.execute("SELECT * FROM features")
    data = (row for row in cur.fetchall())

    global w
    w = 31
    table = Table(root, headings=('ID', 'Название признака'), rows=data)
    table.grid(row = 2, column = 2, columnspan = 2, padx = 2, pady = 20)

def generate_all_features_value():
    global COUNT_FEATURES
    global cur
    global conn

    cur = cur.execute('SELECT * FROM features_count')
    rows = cur.fetchall()

    for row in rows:
        count_all = row[1]
        count_normal = row[2]
        for j in range(1, count_all + 1):
            name_feature = "feature" + str(row[0])
            name_value = "value" + str(j)
            cur1 = conn.cursor()
            cur1.execute('INSERT INTO features_all_value(name_features, feature_value) VALUES(?, ?)', (name_feature, name_value,))
            conn.commit()

        for i in range(1, count_normal + 1):
            name_feature = "feature" + str(row[0])
            name_value = "value" + str(i)
            cur1 = conn.cursor()
            cur1.execute('INSERT INTO features_normal_value(name_features, feature_value) VALUES(?, ?)', (name_feature, name_value,))
            conn.commit()

    conn.commit()

    cur.execute("SELECT * FROM features_all_value")
    data = (row for row in cur.fetchall())

    global w
    w = 120
    table = Table(root, headings=('Название признака', 'ВЗ'), rows=data)
    table.grid(row=2, column=5, columnspan=2, padx=2, pady=20)


    cur.execute("SELECT * FROM features_normal_value")
    data = (row for row in cur.fetchall())

    table = Table(root, headings=('Название признака', 'НЗ'), rows=data)
    table.grid(row=2, column=7, columnspan=2, padx=2, pady=20)

def generate_features_value():
    global COUNT_FEATURES
    global MIN_COUNT_VALUES_FEATURES
    global MAX_COUNT_VALUES_FEATURES
    global cur
    global conn

    MAX_COUNT_VALUES_FEATURES = int(e3.get())

    for i in range(1, COUNT_FEATURES + 1):
        all = randint(MIN_COUNT_VALUES_FEATURES, MAX_COUNT_VALUES_FEATURES)
        normal = randint(1, all - 1)
        cur.execute('INSERT INTO features_count(ID, all_features, normal_features_count) VALUES(?, ?, ?)', (str(i), all, normal,))
        conn.commit()


    cur.execute("SELECT * FROM features_count")
    data = (row for row in cur.fetchall())

    global w
    w = 30
    table = Table(root, headings=('ID', 'ВЗ', 'НЗ'), rows=data)
    table.grid(row = 2, column = 3, columnspan = 2, padx = 2, pady = 20)

    generate_all_features_value()

def generate_periods():
    global cur
    global conn
    global MAX_COUNT_PERIOD
    global COUNT_CLASS
    global COUNT_FEATURES

    MAX_COUNT_PERIOD = int(e4.get())

    for i in range(1, COUNT_CLASS + 1):
        class_name = "class" + str(i)
        for j in range(1, COUNT_FEATURES + 1):
            feature_name = "feature" + str(j)
            periods = randint(MIN_COUNT_PERIOD, MAX_COUNT_PERIOD)
            cur.execute('INSERT INTO periods_count(name_class, name_feature, count) VALUES(?, ?, ?)', (class_name, feature_name, periods,))

    conn.commit()

    cur.execute("SELECT * FROM periods_count")
    data = (row for row in cur.fetchall())

    global w
    w = 120
    table = Table(root, headings=('Название класса', 'Название признака', 'ЧПД'), rows=data)
    table.grid(row = 3, column = 0, columnspan = 4, pady = 10)


def Generate():
    global cur
    global conn

    # Удаление и повторное создание таблицы c классами
    cur.execute('DROP table if exists classes')
    cur.execute("CREATE TABLE classes(ID integer, name_class text)")

    # Удаление и повторное создание таблицы c признаками
    cur.execute('DROP table if exists features')
    cur.execute("CREATE TABLE features (ID integer, name_features text)")

    # Удаление и повторное создание количества возможных и нормальных значений
    cur.execute('DROP table if exists features_count')
    cur.execute("CREATE TABLE features_count (ID integer, all_features integer, normal_features_count integer)")

    # Удаление и повторное создание возможных значений
    cur.execute('DROP table if exists features_all_value')
    cur.execute("CREATE TABLE features_all_value (name_features text, feature_value text)")

    # Удаление и повторное создание нормальных значений
    cur.execute('DROP table if exists features_normal_value')
    cur.execute("CREATE TABLE features_normal_value (name_features text, feature_value text)")

    # Удаление и повторное создание ЧПД признаков
    cur.execute('DROP table if exists periods_count')
    cur.execute("CREATE TABLE periods_count (name_class text, name_feature text, count integer)")

    conn.commit()

    gen_classes()
    gen_features()
    generate_features_value()
    generate_periods()






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

l4 = Label(text="Ограничение на число \n периодов динамики:", font="Times 12", bg="AliceBlue")
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
