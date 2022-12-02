from tkinter import *
import tkinter.ttk as ttk
import sqlite3

from ast import literal_eval
import random
from   random import randint

w = 1
COUNT_CLASS = 2
COUNT_FEATURES = 2

class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        global w
        for head in headings:

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
root.geometry("1000x800")
root["bg"] = "AliceBlue"

conn = sqlite3.connect('ifbz.db')
cur = conn.cursor()

conn_mvd = sqlite3.connect('mvd.db')
cur_mvd = conn_mvd.cursor()

def border_creator(id, class_name, feature_name, mas_moments, mas_values):
    global cur
    global conn
    n = len(mas_moments)

    count_per = 1

    print()
    print("Count_per ", count_per, end=" - ")
    border = str(mas_moments[n-1])
    print(border, end=" ")
    print("     I период:", "НГ = ", border, "ВГ = ", border, end=" ")
    print("ЗДП = ", str(list(set(mas_values))).strip('[]'))
    cur.execute(
        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
        (id, class_name, feature_name, count_per, border, border, str(list(set(mas_values))).strip('[]')))

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
                ng1 = mas_moments[0]
                vg1 = a
                ng2 = mas_moments[gr1+1] - a
                vg2 = b - a
                #ng2 = vg2
                print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                cur.execute('INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                            (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))


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
                    ng1 = mas_moments[0]
                    vg1 = a
                    ng2 = mas_moments[gr1+1] - a
                    vg2 = b - a
                    ng3 = mas_moments[gr2+1] - b
                    vg3 = c - b
                    #ng2 = vg2
                    #ng3 = vg3
                    print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                    print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                    print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                    print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                    print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                    print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))

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
                ng1 = mas_moments[0]
                vg1 = a
                ng2 = mas_moments[gr1 + 1] - a
                vg2 = b - a
                ng3 = mas_moments[gr2 + 1] - b
                vg3 = c - b
                #ng2 = vg2
                #ng3 = vg3
                print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))

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
                    ng1 = mas_moments[0]
                    vg1 = a
                    ng2 = mas_moments[gr1 + 1] - a
                    vg2 = b - a
                    ng3 = mas_moments[gr2 + 1] - b
                    vg3 = c - b
                    ng4 = mas_moments[gr3 + 1] - c
                    vg4 = d - c
                    #ng2 = vg2
                    #ng3 = vg3
                    #ng4 = vg4
                    print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                    print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                    print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                    print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                    print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                    print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                    print("     IV период:", "НГ = ", ng4, "ВГ = ", vg4, end=" ")
                    print("ЗДП = ", str(list(set(d_val))).strip('[]'))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng4, vg4, str(list(set(d_val))).strip('[]')))

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
                    ng1 = mas_moments[0]
                    vg1 = a
                    ng2 = mas_moments[gr1 + 1] - a
                    vg2 = b - a
                    ng3 = mas_moments[gr2 + 1] - b
                    vg3 = c - b
                    ng4 = mas_moments[gr3 + 1] - c
                    vg4 = d - c
                    #ng2 = vg2
                    #ng3 = vg3
                    #ng4 = vg4
                    print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                    print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                    print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                    print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                    print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                    print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                    print("     IV период:", "НГ = ", ng4, "ВГ = ", vg4, end=" ")
                    print("ЗДП = ", str(list(set(d_val))).strip('[]'))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng4, vg4, str(list(set(d_val))).strip('[]')))

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
                ng1 = mas_moments[0]
                vg1 = a
                ng2 = mas_moments[gr1 + 1] - a
                vg2 = b - a
                ng3 = mas_moments[gr2 + 1] - b
                vg3 = c - b
                ng4 = mas_moments[gr3 + 1] - c
                vg4 = d - c
                #ng2 = vg2
                #ng3 = vg3
                #ng4 = vg4
                print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                print("     IV период:", "НГ = ", ng4, "ВГ = ", vg4, end=" ")
                print("ЗДП = ", str(list(set(d_val))).strip('[]'))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng4, vg4, str(list(set(d_val))).strip('[]')))

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
                    ng1 = mas_moments[0]
                    vg1 = a
                    ng2 = mas_moments[gr1 + 1] - a
                    vg2 = b - a
                    ng3 = mas_moments[gr2 + 1] - b
                    vg3 = c - b
                    ng4 = mas_moments[gr3 + 1] - c
                    vg4 = d - c
                    ng5 = mas_moments[gr4 + 1] - d
                    vg5 = e - d
                    #ng2 = vg2
                    #ng3 = vg3
                    #ng4 = vg4
                    #ng5 = vg5

                    print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                    print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                    print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                    print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                    print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                    print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                    print("     IV период:", "НГ = ", ng4, "ВГ = ", vg4, end=" ")
                    print("ЗДП = ", str(list(set(d_val))).strip('[]'))
                    print("      V период:", "НГ = ", ng5, "ВГ = ", vg5, end=" ")
                    print("ЗДП = ", str(list(set(e_val))).strip('[]'))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng4, vg4, str(list(set(d_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng5, vg5, str(list(set(e_val))).strip('[]')))

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
                    vg1 = a
                    ng1 = mas_moments[0]
                    ng2 = mas_moments[gr1 + 1] - a
                    vg2 = b - a
                    ng3 = mas_moments[gr2 + 1] - b
                    vg3 = c - b
                    ng4 = mas_moments[gr3 + 1] - c
                    vg4 = d - c
                    ng5 = mas_moments[gr4 + 1] - d
                    vg5 = e - d
                    #ng2 = vg2
                    #ng3 = vg3
                    #ng4 = vg4
                    #ng5 = vg5
                    print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                    print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                    print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                    print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                    print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                    print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                    print("     IV период:", "НГ = ", ng4, "ВГ = ", vg4, end=" ")
                    print("ЗДП = ", str(list(set(d_val))).strip('[]'))
                    print("      V период:", "НГ = ", ng5, "ВГ = ", vg5, end=" ")
                    print("ЗДП = ", str(list(set(e_val))).strip('[]'))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng4, vg4, str(list(set(d_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng5, vg5, str(list(set(e_val))).strip('[]')))

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
                    vg1 = a
                    ng1 = mas_moments[0]
                    ng2 = mas_moments[gr1 + 1] - a
                    vg2 = b - a
                    ng3 = mas_moments[gr2 + 1] - b
                    vg3 = c - b
                    ng4 = mas_moments[gr3 + 1] - c
                    vg4 = d - c
                    ng5 = mas_moments[gr4 + 1] - d
                    vg5 = e - d
                    #ng2 = vg2
                    #ng3 = vg3
                    #ng4 = vg4
                    #ng5 = vg5
                    print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                    print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                    print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                    print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                    print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                    print("ЗДП = ", str(list(set(c_val))).strip('[]'))
                    print("     IV период:", "НГ = ", ng4, "ВГ = ", vg4, end=" ")
                    print("ЗДП = ", str(list(set(d_val))).strip('[]'))
                    print("      V период:", "НГ = ", ng5, "ВГ = ", vg5, end=" ")
                    print("ЗДП = ", str(list(set(e_val))).strip('[]'))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng4, vg4, str(list(set(d_val))).strip('[]')))
                    cur.execute(
                        'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                        (id, class_name, feature_name, count_per, ng5, vg5, str(list(set(e_val))).strip('[]')))

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
                vg1 = a
                ng1 = mas_moments[0]
                ng2 = mas_moments[gr1 + 1] - a
                vg2 = b - a
                ng3 = mas_moments[gr2 + 1] - b
                vg3 = c - b
                ng4 = mas_moments[gr3 + 1] - c
                vg4 = d - c
                ng5 = mas_moments[gr4 + 1] - d
                vg5 = e - d

                #ng2 = vg2
                #ng3 = vg3
                #ng4 = vg4
                #ng5 = vg5
                print("     I период:", "НГ = ", ng1, "ВГ = ", vg1, end=" ")
                print("ЗДП = ", str(list(set(a_val))).strip('[]'))
                print("     II период:", "НГ = ", ng2, "ВГ = ", vg2, end=" ")
                print("ЗДП = ", str(list(set(b_val))).strip('[]'))
                print("     III период:", "НГ = ", ng3, "ВГ = ", vg3, end=" ")
                print("ЗДП = ",str(list(set(c_val))).strip('[]'))
                print("     IV период:", "НГ = ", ng4, "ВГ = ", vg4, end=" ")
                print("ЗДП = ", str(list(set(d_val))).strip('[]'))
                print("      V период:", "НГ = ", ng5, "ВГ = ", vg5, end=" ")
                print("ЗДП = ", str(list(set(e_val))).strip('[]'))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng1, vg1, str(list(set(a_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng2, vg2, str(list(set(b_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng3, vg3, str(list(set(c_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng4, vg4, str(list(set(d_val))).strip('[]')))
                cur.execute(
                    'INSERT INTO borders(ibz, name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES(?, ?, ?, ?, ?, ?, ?)',
                    (id, class_name, feature_name, count_per, ng5, vg5, str(list(set(e_val))).strip('[]')))

    conn.commit()
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

    cur.execute("SELECT * FROM borders")
    data = (row for row in cur.fetchall())

    global w
    w = 100
    table = Table(root, headings=('ID', 'Класс','Признак', '№ периода', 'НГ', 'ВГ', 'ЗДП'), rows=data)
    table.grid(row=3, column=0, columnspan=5, pady=5)

def merge_one_periods(count_ib, count_class, count_features):
    global conn
    global cur

    conn1 = sqlite3.connect('ifbz.db')
    cur1 = conn1.cursor()

    cur = conn.execute('SELECT * FROM borders')
    rows = cur.fetchall()

    for i in range(1, count_class + 1):
        for j in range(1, count_features + 1):
            for row in rows:
                if row[1] == "class" + str(i) and row[2] == "feature" + str(j) and row[3] == 1:
                    if row[0] == (count_ib // count_class) * i - (count_ib // count_class - 1):
                        ng = row[4]
                        vg = row[5]
                        val = literal_eval("[" + row[6] + "]")
                    else:
                        ng = min(ng, row[4])
                        vg = max(vg, row[5])
                        val.extend(literal_eval("[" + row[6] + "]"))


            class_name = "class" + str(i)
            feature_name = "feature" + str(j)
            val = list(set(val))
            val = sorted(val)

            cur1.execute('INSERT INTO merge_(name_class, name_feature, count_periods, ng, vg_per, values_per) VALUES( ?, ?, ?, ?, ?, ?)',
                (class_name, feature_name, 1, ng, vg, str(val).strip('[]')))

    conn1.commit()

def two(class_name, feature_name, i, n1,v1, va1, n2, v2, va2):

    conn1 = sqlite3.connect('ifbz.db')
    cur1 = conn1.cursor()

    id = i.copy()
    ng1 = n1.copy()
    vg1 = v1.copy()
    val1 = va1.copy()
    ng2 = n2.copy()
    vg2 = v2.copy()
    val2 = va2.copy()

    merge_id = []
    merge_id.append(id[0])
    merge_ng1 = []
    merge_vg1 = []
    merge_val1 = []
    merge_ng2 = []
    merge_vg2 = []
    merge_val2 = []


    count = 0



    for i in range(0, len(id)):

        if id[i] == merge_id[0]:
            merge_ng1.append(ng1[i])
            merge_vg1.append(vg1[i])
            merge_val1.append(val1[i])
            merge_ng2.append(ng2[i])
            merge_vg2.append(vg2[i])
            merge_val2.append(val2[i])
        else:
            count = i
            break

    if len(id) != 1:
        flag = True
    else:
        flag = False
    #print(merge_val1)
    #print(merge_val2)


    while flag:

        flag = False
        m_ng1 = []
        m_vg1 = []
        m_val1 = []
        m_ng2 = []
        m_vg2 = []
        m_val2 = []
        index = 0
        n = 0

        for i in range(0, len(merge_val1)):
            for j in range(count, len(id)):
                if j == count:
                    index = id[j]
                if id[j] == index:

                    v1 = merge_val1[i].copy()
                    v1.extend(val1[j])
                    v2 = merge_val2[i].copy()
                    v2.extend(val2[j])

                    #print(merge_val1)
                    #print(merge_val2)
                    '''
                    print("id = ",id[j])
                    print("1-1 = ",merge_vg1[i])
                    print("1.2 ", vg1[j])
                    print("2.1 ", merge_vg2[i])
                    print("2.2 ", vg2[j])
                    '''


                    v1 = list(set(v1))
                    v2 = list(set(v2))
                    v1.sort()
                    v2.sort()
                    #print(v1)
                    #print(v2)

                    sovp = [x for x in v1 if x in v2]


                    if sovp == []:
                        m_ng1.append(min(merge_ng1[i], ng1[j]))
                        m_vg1.append(max(merge_vg1[i], vg1[j]))
                        m_val1.append(v1)
                        m_ng2.append(min(merge_ng2[i], ng2[j]))
                        m_vg2.append(max(merge_vg2[i], vg2[j]))
                        m_val2.append(v2)
                        n = j + 1
                        flag = True
                    #print("-----")
                else:
                    n = j
                    break

        count = n
        if flag == True:
            merge_ng1 = m_ng1
            merge_vg1 = m_vg1
            merge_val1 = m_val1
            merge_ng2 = m_ng2
            merge_vg2 = m_vg2
            merge_val2 = m_val2

    if len(id) != 1:
        ng1 = merge_ng1[0]
        vg1 = merge_vg1[0]
        val1 = merge_val1[0]
        ng2 = merge_ng2[0]
        vg2 = merge_vg2[0]
        val2 = merge_val2[0]

        val1 = list(set(val1))
        val2 = list(set(val2))
        val1 = sorted(val1)
        val2 = sorted(val2)

        sovp = [x for x in val1 if x in val2]

        if sovp != []:
            id = []
        else:
            id = [1]

        if len(id) != 0:
            cur1.execute(
                'INSERT INTO merge_(name_class, name_feature, count_periods,values_per, ng, vg_per) VALUES( ?, ?, ?, ?, ?, ?)',
                (class_name, feature_name, 1, str(val1).strip('[]'), ng1, vg1 ))
            cur1.execute(
                'INSERT INTO merge_(name_class, name_feature, count_periods,values_per, ng, vg_per) VALUES( ?, ?, ?, ?, ?, ?)',
                (class_name, feature_name, 2, str(val2).strip('[]'),  ng2, vg2))
            conn1.commit()


def merge_two_periods(count_ib, count_class, count_features):
    global conn
    global cur

    conn1 = sqlite3.connect('ifbz.db')
    cur1 = conn1.cursor()

    cur = conn.execute('SELECT * FROM borders')
    rows = cur.fetchall()

    for i in range(1, count_class + 1):
        for j in range(1, count_features + 1):
            count_per = 1
            class_name = "class" + str(i)
            feature_name = "feature" + str(j)
            id = []
            ng1 = []
            vg1 = []
            val1 = []

            ng2 = []
            vg2 = []
            val2 = []
            count = 0
            for row in rows:
                if row[1] == "class" + str(i) and row[2] == "feature" + str(j) and row[3] == 2:
                    if count_per == 1:
                        id.append(row[0])
                        ng1.append(row[4])
                        vg1.append(row[5])
                        val1.append(literal_eval("[" + row[6] + "]"))
                        count_per = 2
                    else:
                        ng2.append(row[4])
                        vg2.append(row[5])
                        val2.append(literal_eval("[" + row[6] + "]"))
                        count_per = 1

            for k in range(1, len(id)):
                if id[k] != id[k-1]:
                    count += 1



            if id != [] and count > (count_ib / count_class) // 2:
                #print("Класс = ", class_name)
                #print("Признак = ", feature_name)
                two("class" + str(i), "feature" + str(j), id, ng1, vg1, val1, ng2, vg2, val2)







def merge():
    global conn
    global cur
    global COUNT_CLASS
    global COUNT_FEATURES

    cur = conn.execute('SELECT * FROM borders')
    rows = cur.fetchall()

    count_ib = 1
    count_class = 1
    count_features = 1

    for row in rows:
        class_name = row[1]
        feature_name = row[2]

        if int(class_name[5:]) > count_class:
            count_class += 1

        if int(feature_name[7:]) > count_features:
            count_features += 1

        if row[0] > count_ib:
            count_ib += 1


    COUNT_CLASS = count_class
    COUNT_FEATURES = count_features

    merge_one_periods(count_ib, count_class, count_features)
    merge_two_periods(count_ib, count_class, count_features)

    cur.execute("SELECT * FROM merge_")
    data = (row for row in cur.fetchall())

    global w
    w = 120
    table = Table(root, headings=('Класс', 'Признак', '№ периода', 'ЗДП', 'НГ', 'ВГ'), rows=data)
    table.grid(row=4, column=0, columnspan=7, pady=5)

def create_final():
    global conn
    global cur
    global COUNT_CLASS
    global COUNT_FEATURES

    cur = conn.execute('SELECT * FROM merge_')
    rows = cur.fetchall()

    cl = []
    pr = []


    for i in range(1, COUNT_CLASS + 1):
        for j in range(1, COUNT_FEATURES + 1):
            cl.append(i)
            pr.append(j)


    for i in range(0, len(cl)):
        ng1 = 0
        vg1 = 0
        val1 = []
        ng2 = 0
        vg2 = 0
        val2 = []
        ng3 = 0
        vg3 = 0
        val3 = []
        ng4 = 0
        vg4 = 0
        val4 = []
        ng5 = 0
        vg5 = 0
        val5 = []

        for row in rows:
            if row[0] == "class" + str(cl[i]) and row[1] == "feature" + str(pr[i]):
                if row[2] == 1:
                    val1 = row[3]
                    ng1 = row[4]
                    vg1 = row[5]
                elif row[2] == 2:
                    val2 = row[3]
                    ng2 = row[4]
                    vg2 = row[5]
                elif row[2] == 3:
                    val3 = row[3]
                    ng3 = row[4]
                    vg3 = row[5]
                elif row[2] == 4:
                    val4 = row[3]
                    ng4 = row[4]
                    vg4 = row[5]
                else:
                    val5 = row[3]
                    ng5 = row[4]
                    vg5 = row[5]


        cur.execute(
            'INSERT INTO final (name_class, name_feature, count_periods,values_per, ng, vg_per) VALUES( ?, ?, ?, ?, ?, ?)',
            ("class" + str(cl[i]), "feature" + str(pr[i]), 1, str(val1), ng1, vg1))

        if vg2 != 0:
            cur.execute('INSERT INTO final (name_class, name_feature, count_periods,values_per, ng, vg_per) VALUES( ?, ?, ?, ?, ?, ?)',
            ("class" + str(cl[i]), "feature" + str(pr[i]), 2, str(val2), ng2, vg2))


        if vg3 != 0:
            cur.execute(
                'INSERT INTO final (name_class, name_feature, count_periods,values_per, ng, vg_per) VALUES( ?, ?, ?, ?, ?, ?)',
                ("class" + str(cl[i]), "feature" + str(pr[i]), 3, str(val3), ng3, vg3))

        if vg4 != 0:
            cur.execute(
                'INSERT INTO final (name_class, name_feature, count_periods,values_per, ng, vg_per) VALUES( ?, ?, ?, ?, ?, ?)',
                ("class" + str(cl[i]), "feature" + str(pr[i]), 4, str(val4), ng4, vg4))

        if vg5 != 0:
            cur.execute('INSERT INTO final (name_class, name_feature, count_periods,values_per, ng, vg_per) VALUES( ?, ?, ?, ?, ?, ?)',
            ("class" + str(cl[i]), "feature" + str(pr[i]), 5, str(val5), ng5, vg5))

        conn.commit()

    cur.execute("SELECT * FROM final")
    data = (row for row in cur.fetchall())

    global w
    w = 120
    table = Table(root, headings=('Класс', 'Признак', '№ периода', 'ЗДП', 'НГ', 'ВГ'), rows=data)
    table.grid(row=6, column=0, columnspan=7, pady=5)



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
    cur.execute("CREATE TABLE borders (ibz integer, name_class text, name_feature text, count_periods integer, ng integer, vg_per integer, values_per text)")

    # Удаление и повторное создание ЧПД признаков
    cur.execute('DROP table if exists merge_')
    cur.execute(
        "CREATE TABLE merge_ (name_class text, name_feature text, count_periods integer, values_per text, ng integer, vg_per)")

    # Удаление и повторное создание ЧПД признаков
    cur.execute('DROP table if exists final')
    cur.execute(
        "CREATE TABLE final (name_class text, name_feature text, count_periods integer, values_per text, ng integer, vg_per)")

    Borders()
    merge()
    create_final()


b_fibz = Button(root, text = "Сформировать", bg = "white", command = click_FIBZ)

b_fibz.grid(row = 0, column=3, padx = 600)

root.mainloop()
