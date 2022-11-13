# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.ttk as ttk
import sqlite3
from random import randint
from random import choice

w = 120

class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        global w
        i = 0
        for head in headings:
            if i > 0 and w != 30 and w != 100:
                w = 60

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
root.title("Генерация модельной выборки данных")
root.geometry("1300x800")
root["bg"] = "AliceBlue"

COUNT_IBZ = 0
COUNT_CLASS = 0
COUNT_IBZ_CLASS = 0
ID = 1

conn = sqlite3.connect('mvd.db')
cur = conn.cursor()

conn_mbz = sqlite3.connect('mbz.db')
cur_mbz = conn_mbz.cursor()

# Функции
def random_choice(mas, mas_zn, count):
    result = mas
    flag = False

    if count <= len(mas_zn):
        while len(result) != count:
            while flag != True:
                n = int(choice(mas_zn))
                flag = True
                for p in range(len(result)):
                    if n == result[p]:
                        flag = False

            result.append(n)
            flag = False
    else:
        while len(result) != count:
            result.append(int(choice(mas_zn)))

    return result


def generation_IBZ():
    global conn
    global cur
    global COUNT_IBZ_CLASS
    global COUNT_CLASS
    global ID

    ID = 1

    for i in range(1, COUNT_CLASS + 1):

        for j in range(1, COUNT_IBZ_CLASS + 1):
            conn3 = sqlite3.connect('mbz.db')
            cur3 = conn3.cursor()
            cur3 = cur3.execute('SELECT * FROM periods_values')
            rows = cur3.fetchall()
            class_name = "class" + str(i)

            for row in rows:
                if row[0] == class_name:
                    feature_name = row[1]
                    num_period = row[2]
                    time_period = randint(row[4], row[5])
                    zpd = row[3]
                    zpd_array = zpd.split(', ')
                    mn = []
                    zmn = []
                    count_mn = 1
                    n = 0
                    flag = False

                    if time_period > 2:
                        count_mn = 3
                    elif time_period == 2:
                        count_mn = 2

                    mn.append(randint(1, time_period))
                    zmn.append(int(choice(zpd_array)))

                    while len(mn) != count_mn:
                        while flag != True:
                            n = randint(1, time_period)
                            flag = True
                            for p in range(len(mn)):
                                if n == mn[p]:
                                    flag = False

                        mn.append(n)
                        flag = False

                    mn.sort()
                    zmn = random_choice(zmn, zpd_array, count_mn)

                    for k in range (0, len(mn)):
                        cur.execute(
                            'INSERT INTO ibz(id, name_class, name_feature, num_mn, ng_per, vg_per, time_per, mn, zpd, zmn) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (ID, class_name, feature_name, k + 1, row[4], row[5], time_period, mn[k], zpd, zmn[k]))
                        conn.commit()

            ID += 1
    cur.execute("SELECT * FROM ibz")
    data = (row for row in cur.fetchall())

    global w
    w = 100
    table = Table(root, headings=('ID', 'Класс', 'Признак', '№ МН', 'НГ', 'ВГ', 'ДПД', 'МН', 'ЗПД', 'ЗМН'), rows=data)
    table.grid(row=2, column=0, columnspan=10, pady=5)


def click_gen_IBZ():
    global COUNT_IBZ
    global COUNT_CLASS
    global COUNT_IBZ_CLASS
    global conn
    global cur
    global conn_mbz
    global cur_mbz

    cur_mbz.execute("SELECT * FROM  classes")


    COUNT_IBZ = int(e_ibz.get())
    COUNT_CLASS = len(cur_mbz.fetchall())

    COUNT_IBZ_CLASS = COUNT_IBZ // COUNT_CLASS

    # Удаление и повторное создание ЧПД признаков
    cur.execute('DROP table if exists ibz')
    cur.execute(
        "CREATE TABLE ibz (id integer, name_class text, name_feature text, num_mn integer, ng_per integer, vg_per integer, time_per integer, mn integer, zpd text, zmn integer)")

    conn.commit()

    generation_IBZ()

l_ibz = Label(root, text = "Количество историй болезней:", bg = "AliceBlue", font = "Arial 14")
e_ibz = Entry(root, width = 30)
b_ibz = Button(root, text = "Сгенерировать", bg = "white", command = click_gen_IBZ)

l_ibz.grid(row = 0, column=0, pady = 10)
e_ibz.grid(row = 0, column=1, pady = 10)
b_ibz.grid(row = 0, column=2, pady = 10)

root.mainloop()
