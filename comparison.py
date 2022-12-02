from tkinter import *
import sqlite3
from ast import literal_eval

w = 1

root = Tk()
root.title("Сравнение МБЗ и ИФБЗ")

root.geometry("800x600")
root["bg"] = "AliceBlue"

conn = sqlite3.connect('ifbz.db')
cur = conn.cursor()

conn1 = sqlite3.connect('mbz.db')
cur1 = conn1.cursor()

def comparison():
    global cur
    global conn

    global cur1
    global conn1

    a = []
    b = []
    сlasses_name = []

    cur = cur.execute('SELECT * FROM periods')
    rows = cur.fetchall()

    cur1 = cur1.execute('SELECT * FROM periods_count')
    rows1 = cur1.fetchall()

    count_class  = 1
    for row in rows:
        class_name = row[0]
        count_class = int(class_name[5:])
        сlasses_name.append(int(class_name[5:]))
        a.append(row[2])

    print("Кол-во классов:", count_class)

    for row in rows1:
        b.append(row[2])


    count = 0
    count_err = []

    cl_name = сlasses_name[0]
    for i in range(0, len(a)):
        if cl_name != сlasses_name[i]:
            cl_name = сlasses_name[i]
            count = 0
        if a[i] != b[i]:
            count += 1
        if cl_name == сlasses_name[i]:
            if len(count_err) < cl_name:
                count_err.append(count)
            else:
                count_err[cl_name-1] = count



    for i in range(len(count_err)):
        percent_class = ((len(a) / count_class) - count_err[i]) / ((len(a) / count_class) / 100)
        print("class", i+1, " = ", percent_class, "%")

    percent = (len(a) - count) / (len(a) / 100)
    print("Средний процент совпадения ЧПД = ", percent, "%")
    print("-----------")


def comparison_values():
    global cur
    global conn

    global cur1
    global conn1

    cur = cur.execute('SELECT * FROM final')
    rows = cur.fetchall()

    cur1 = cur1.execute('SELECT * FROM periods_values')
    rows1 = cur1.fetchall()

    a_val = []
    b_val = []
    сlasses_name = []

    for row in rows:
        class_name = row[0]
        сlasses_name.append(int(class_name[5:]))
        a_val.append(literal_eval("[" + row[3] + "]"))

    for row in rows1:
        b_val.append(literal_eval("[" + row[3] + "]"))


    a = []
    count_a = 0
    b = []
    count_b = 0
    c = []
    count_c = 0

    cl_name = сlasses_name[0]

    for i in range(0, len(a_val)):
        if cl_name != сlasses_name[i]:
            cl_name = сlasses_name[i]
            count_a = 0
            count_b = 0
            count_c = 0
        sovp = [x for x in a_val[i] if x in b_val[i]]

        if sovp == []:
            count_c += 1
        if len(sovp) == len(a_val[i]):
            count_a += 1
        else:
            count_b += 1

        if cl_name == сlasses_name[i]:
            if len(a) < cl_name:
                a.append(count_a)
                b.append(count_b)
                c.append(count_c)
            else:
                a[cl_name - 1] = count_a
                b[cl_name - 1] = count_b
                c[cl_name - 1] = count_c

    for i in range(len(a)):
        all_ = a[i] + b[i] + c[i]
        percent_a = round(a[i]  / (all_ / 100))
        percent_b = round(b[i]  / (all_ / 100))
        percent_c = round(c[i]  / (all_ / 100))
        print("class", i+1)
        print("Полное совпадение = ", percent_a, "%")
        print("Частичное совпадение = ", percent_b, "%")
        print("Нет совпадений = ", percent_c, "%")
        print("-----------")

comparison()
comparison_values()

