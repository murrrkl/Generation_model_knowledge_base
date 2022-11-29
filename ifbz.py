from tkinter import *
import tkinter.ttk as ttk
import sqlite3

import random
from   random import randint

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
root.title("Формирование альтернативной базы знаний")
root.geometry("1300x800")
root["bg"] = "AliceBlue"

conn = sqlite3.connect('ifbz.db')
cur = conn.cursor()

conn_mvd = sqlite3.connect('mvd.db')
cur_mvd = conn_mvd.cursor()

def border_creator(id, class_name, feature_name, mas_moments, mas_values):
    n = len(mas_moments)

    count_per = 1

    print()

    print("Count_per ", count_per, end=" - ")
    border = str(mas_moments[n-1])
    print(border)

    count_per = 2

    if n >= 2:
        count_2 = 1

        for gr1 in range(0, n-1):
            a = mas_moments[gr1]
            a_val = mas_values[0:(gr1+1)]
            b = mas_moments[n-1]
            b_val = mas_values[(gr1 + 1):]

            sovp = [x for x in a_val if x in b_val]

            if sovp == []:
                print("Count_per ", count_per, ".", count_2, sep="", end=" - ")
                count_2 += 1
                border = str(a) + "; " + str(b)
                print(border)

    count_per = 3

    if n >= 3:
        count_3 = 1
        gr2 = 1

        for gr1 in range(0, n-2):
            while gr2 != n-2:
                a = mas_moments[gr1]
                a_val = mas_values[0:(gr1 + 1)]
                b = mas_moments[gr2]
                b_val = mas_values[(gr1 + 1):(gr2 + 1)]
                c = mas_moments[n - 1]
                c_val = mas_values[(gr2 + 1):]

                sovp = [x for x in a_val if x in b_val]
                sovp2 = [x for x in c_val if x in b_val]

                if sovp == [] and sovp2 == []:
                    print("Count_per ", count_per, ".", count_3, sep="", end=" - ")
                    count_3 += 1
                    border = str(a) + "; " + str(b) + "; " + str(c)
                    print(border)

                gr2 += 1

            a = mas_moments[gr1]
            a_val = mas_values[0:(gr1 + 1)]
            b = mas_moments[gr2]
            b_val = mas_values[(gr1 + 1):(gr2 + 1)]
            c = mas_moments[n - 1]
            c_val = mas_values[(gr2 + 1):]

            sovp = [x for x in a_val if x in b_val]
            sovp2 = [x for x in c_val if x in b_val]

            if sovp == [] and sovp2 == []:
                print("Count_per ", count_per, ".", count_3, sep="", end=" - ")
                count_3 += 1
                border = str(a) + "; " + str(b) + "; " + str(c)
                print(border)

    count_per = 4
    if n >= 4:
        count_4 = 1
        gr2 = 1
        gr3 = 2

        for gr1 in range(0, n-3):
            while gr3 != n-2:
                a = mas_moments[gr1]
                a_val = mas_values[0:(gr1 + 1)]
                b = mas_moments[gr2]
                b_val = mas_values[(gr1 + 1):(gr2 + 1)]
                c = mas_moments[gr3]
                c_val = mas_values[(gr2 + 1):(gr3 + 1)]
                d = mas_moments[n - 1]
                d_val = mas_values[(gr3 + 1):]

                sovp = [x for x in a_val if x in b_val]
                sovp2 = [x for x in c_val if x in b_val]
                sovp3 = [x for x in c_val if x in d_val]

                if sovp == [] and sovp2 == [] and sovp3 == []:
                    print("Count_per ", count_per, ".", count_4, sep="", end=" - ")
                    count_4 += 1
                    border = str(a) + "; " + str(b) + "; " + str(c) + "; " + str(d)
                    print(border)

                gr3 += 1
            while gr2 != n-3:
                a = mas_moments[gr1]
                a_val = mas_values[0:(gr1 + 1)]
                b = mas_moments[gr2]
                b_val = mas_values[(gr1 + 1):(gr2 + 1)]
                c = mas_moments[gr3]
                c_val = mas_values[(gr2 + 1):(gr3 + 1)]
                d = mas_moments[n - 1]
                d_val = mas_values[(gr3 + 1):]

                sovp = [x for x in a_val if x in b_val]
                sovp2 = [x for x in c_val if x in b_val]
                sovp3 = [x for x in c_val if x in d_val]

                if sovp == [] and sovp2 == [] and sovp3 == []:
                    print("Count_per ", count_per, ".", count_4, sep="", end=" - ")
                    count_4 += 1
                    border = str(a) + "; " + str(b) + "; " + str(c) + "; " + str(d)
                    print(border)

                gr2 += 1

            a = mas_moments[gr1]
            a_val = mas_values[0:(gr1 + 1)]
            b = mas_moments[gr2]
            b_val = mas_values[(gr1 + 1):(gr2 + 1)]
            c = mas_moments[gr3]
            c_val = mas_values[(gr2 + 1):(gr3 + 1)]
            d = mas_moments[n - 1]
            d_val = mas_values[(gr3 + 1):]

            sovp = [x for x in a_val if x in b_val]
            sovp2 = [x for x in c_val if x in b_val]
            sovp3 = [x for x in c_val if x in d_val]

            if sovp == [] and sovp2 == [] and sovp3 == []:
                print("Count_per ", count_per, ".", count_4, sep="", end=" - ")
                count_4 += 1
                border = str(a) + "; " + str(b) + "; " + str(c) + "; " + str(d)
                print(border)

    count_per = 5
    if n >= 5:
        count_5 = 1
        gr2 = 1
        gr3 = 2
        gr4 = 3

        for gr1 in range(0, n-4):
            while gr4 != n-2:
                a = mas_moments[gr1]
                a_val = mas_values[0:(gr1 + 1)]
                b = mas_moments[gr2]
                b_val = mas_values[(gr1 + 1):(gr2 + 1)]
                c = mas_moments[gr3]
                c_val = mas_values[(gr2 + 1):(gr3 + 1)]
                d = mas_moments[gr4]
                d_val = mas_values[(gr3 + 1): (gr4 + 1)]
                e = mas_moments[n - 1]
                e_val = mas_values[(gr4 + 1):]

                sovp = [x for x in a_val if x in b_val]
                sovp2 = [x for x in c_val if x in b_val]
                sovp3 = [x for x in c_val if x in d_val]
                sovp4 = [x for x in e_val if x in d_val]

                if sovp == [] and sovp2 == [] and sovp3 == []  and sovp4 == []:
                    print("Count_per ", count_per, ".", count_5, sep="", end=" - ")
                    count_5 += 1
                    border = str(a) + "; " + str(b) + "; " + str(c) + "; " + str(d) + "; " + str(e)
                    print(border)

                gr4 += 1

            while gr3 != n-3:
                a = mas_moments[gr1]
                a_val = mas_values[0:(gr1 + 1)]
                b = mas_moments[gr2]
                b_val = mas_values[(gr1 + 1):(gr2 + 1)]
                c = mas_moments[gr3]
                c_val = mas_values[(gr2 + 1):(gr3 + 1)]
                d = mas_moments[gr4]
                d_val = mas_values[(gr3 + 1): (gr4 + 1)]
                e = mas_moments[n - 1]
                e_val = mas_values[(gr4 + 1):]

                sovp = [x for x in a_val if x in b_val]
                sovp2 = [x for x in c_val if x in b_val]
                sovp3 = [x for x in c_val if x in d_val]
                sovp4 = [x for x in e_val if x in d_val]

                if sovp == [] and sovp2 == [] and sovp3 == []  and sovp4 == []:
                    print("Count_per ", count_per, ".", count_5, sep="", end=" - ")
                    count_5 += 1
                    border = str(a) + "; " + str(b) + "; " + str(c) + "; " + str(d) + "; " + str(e)
                    print(border)

                gr3 += 1

            while gr2 != n-4:
                a = mas_moments[gr1]
                a_val = mas_values[0:(gr1 + 1)]
                b = mas_moments[gr2]
                b_val = mas_values[(gr1 + 1):(gr2 + 1)]
                c = mas_moments[gr3]
                c_val = mas_values[(gr2 + 1):(gr3 + 1)]
                d = mas_moments[gr4]
                d_val = mas_values[(gr3 + 1): (gr4 + 1)]
                e = mas_moments[n - 1]
                e_val = mas_values[(gr4 + 1):]

                sovp = [x for x in a_val if x in b_val]
                sovp2 = [x for x in c_val if x in b_val]
                sovp3 = [x for x in c_val if x in d_val]
                sovp4 = [x for x in e_val if x in d_val]

                if sovp == [] and sovp2 == [] and sovp3 == [] and sovp4 == []:
                    print("Count_per ", count_per, ".", count_5, sep="", end=" - ")
                    count_5 += 1
                    border = str(a) + "; " + str(b) + "; " + str(c) + "; " + str(d) + "; " + str(e)
                    print(border)

                gr2 += 1



            a = mas_moments[gr1]
            a_val = mas_values[0:(gr1 + 1)]
            b = mas_moments[gr2]
            b_val = mas_values[(gr1 + 1):(gr2 + 1)]
            c = mas_moments[gr3]
            c_val = mas_values[(gr2 + 1):(gr3 + 1)]
            d = mas_moments[gr4]
            d_val = mas_values[(gr3 + 1): (gr4 + 1)]
            e = mas_moments[n - 1]
            e_val = mas_values[(gr4 + 1):]

            sovp = [x for x in a_val if x in b_val]
            sovp2 = [x for x in c_val if x in b_val]
            sovp3 = [x for x in c_val if x in d_val]
            sovp4 = [x for x in e_val if x in d_val]

            if sovp == [] and sovp2 == [] and sovp3 == [] and sovp4 == []:
                print("Count_per ", count_per, ".", count_5, sep="", end=" - ")
                count_5 += 1
                border = str(a) + "; " + str(b) + "; " + str(c) + "; " + str(d) + "; " + str(e)
                print(border)

    print("======================")

def Borders():
    global conn
    global cur
    global conn_mvd
    global cur_mvd

    id = 1
    class_name = ""
    feature_name = ""

    mas_moments = []
    mas_values = []

    cur_mvd = conn_mvd.execute('SELECT * FROM mvd')
    rows = cur_mvd.fetchall()

    index = 0

    for row in rows:
        if index == 0:
            id = row[0]
            class_name = row[1]
            feature_name = row[2]
            index = 1

        if feature_name != row[2]:
            print("id = ", id)
            print(class_name)
            print(feature_name)

            n = len(mas_values)

            for i in range(n):
                print("    ", mas_values[i], end=" ")

            print()

            for i in range(n):
                print("-------", end="")

            print(">")

            for i in range(n):
                print("   ", mas_moments[i], end=" ")

            print()

            border_creator(id, class_name, feature_name, mas_moments, mas_values)




            id = row[0]
            class_name = row[1]
            feature_name = row[2]
            mas_moments = []
            mas_values = []

        if feature_name == row[2]:
            mas_moments.append(row[3])
            mas_values.append(row[4])

    print("id = ", id)
    print(class_name)
    print(feature_name)

    n = len(mas_values)

    for i in range(n):
        print("    ", mas_values[i], end=" ")

    print()

    for i in range(n):
        print("-------", end="")

    print(">")

    for i in range(n):
        print("   ", mas_moments[i], end=" ")

    print()

    border_creator(id, class_name, feature_name, mas_moments, mas_values)




def click_FIBZ():
    global conn
    global cur

    # Удаление и повторное создание таблицы c классами
    cur.execute('DROP table if exists classes')
    cur.execute("CREATE TABLE classes(ID integer, name_class text)")

    # Удаление и повторное создание таблицы c признаками
    cur.execute('DROP table if exists features')
    cur.execute("CREATE TABLE features (ID integer, name_features text)")

    # Удаление и повторное создание ЧПД признаков
    cur.execute('DROP table if exists borders')
    cur.execute("CREATE TABLE borders (ibz integer, name_class text, name_feature text, count_periods integer, borders text, values_m text)")

    # Удаление и повторное создание ЧПД признаков
    cur.execute('DROP table if exists periods_values')
    cur.execute(
        "CREATE TABLE periods_values (name_class text, name_feature text, num_periods integer, per_values text, ng integer, vg integer)")

    Borders()


b_fibz = Button(root, text = "Сформировать", bg = "white", command = click_FIBZ)

b_fibz.grid(row = 0, column=3, padx = 600)

root.mainloop()
