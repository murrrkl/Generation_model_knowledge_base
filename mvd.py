# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.ttk as ttk
import sqlite3


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

conn = sqlite3.connect('mbz.db')
cur = conn.cursor()


COUNT_IBZ = 0
COUNT_CLASS = 0
COUNT_IBZ_CLASS = 0
ID = 1

conn = sqlite3.connect('mvd.db')
cur = conn.cursor()

conn_mbz = sqlite3.connect('mbz.db')
cur_mbz = conn_mbz.cursor()

# Функции
def generation_IBZ():
    global COUNT_IBZ_CLASS
    global COUNT_CLASS
    global ID

    print(COUNT_CLASS)

    for i in range(1, COUNT_CLASS + 1):

        for j in range(1, COUNT_IBZ_CLASS + 1):
            conn3 = sqlite3.connect('mbz.db')
            cur3 = conn3.cursor()
            cur3 = cur3.execute('SELECT * FROM periods_values')
            rows = cur3.fetchall()
            class_name = "class" + str(i)
            feature_name = ""
            num_period = 0

            for row in rows:
                if row[0] == class_name:
                    feature_name = row[1]
                    num_period = row[2]
                    print("ID =", ID, end=" ")
                    print("Класс =", class_name, end=" ")
                    print("Признак =", feature_name, end=" ")
                    print("Период =", num_period)



            ID += 1



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
        "CREATE TABLE ibz (id integer, name_class text, name_feature text, num_periods integer, time_per integer)")

    conn.commit()

    generation_IBZ()

l_ibz = Label(root, text = "Количество историй болезней:", bg = "AliceBlue", font = "Arial 14")
e_ibz = Entry(root, width = 30)
b_ibz = Button(root, text = "Сгенерировать", bg = "white", command = click_gen_IBZ)

l_ibz.grid(row = 0, column=0, pady = 10)
e_ibz.grid(row = 0, column=1, pady = 10)
b_ibz.grid(row = 0, column=2, pady = 10)



root.mainloop()
