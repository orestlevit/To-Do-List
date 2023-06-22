# -------------------Imports---------------------------
from tkinter import *
from tkcalendar import Calendar
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
import calendar
from task import Task
from db_service import DataBaseService
# -------------------Imports---------------------------

# ----------------tkinter configure--------------------
screen = Tk()
screen.title("To-Do-List")
screen.geometry("1000x500")
screen.configure(bg="#4c4d4e")
# ----------------tkinter configure--------------------

# -------------------Widgets---------------------------
l1 = Label(text="To-Do List", font=("system",20),bg="#4c4d4e", fg="White")
l2 = Label(text="Entry task title:", font="system",bg="#4c4d4e", fg="White")
e1 = Entry(width=18, font="Arial")
b1 = Button(text="Add task",width=20,bg="#a5a5a5", fg="white", font="system",command=lambda:add_task())
b2 = Button(text="Delete",width=15,bg="#a5a5a5", fg="white", font="system",command=lambda:del_one())
b3 = Button(text="Delete all",width=15,bg="#a5a5a5", fg="white", font="system",command=lambda:delete_alles_task())
b4 = Button(text="Done/Undone",width=15,bg="#a5a5a5", fg="white", font="system",command=lambda:done())
b5 = Button(text="Sort",width=10,bg="#a5a5a5", fg="white", font="system",command=lambda:sort())
listbox = Listbox(height=12,width=50,selectmode="SINGLE", bd=4,font=("Arial",13),bg="#a5a5a5", fg="white")
combo = Combobox(values=["title","deadline","status"],width=10,font="system",state="readonly")
cal = Calendar(selectmode="day",font="system")
combo.current(0)

#b6 = Button(text="uk",width=10,font="Arial",command=lambda:change_language_uk())
#b7 = Button(text="eng",width=10,font="Arial",command=lambda:change_language_eng())
# -------------------Widgets---------------------------


# ----------------Place geometry-----------------------
l1.place(x=420, y=10)       #To-DO-List-text
l2.place(x=195, y=50)       #Entry task title
e1.place(x=170, y=70)       #EntyTask
b1.place(x=169, y=95)       #Add task
b2.place(x=400, y=390)      #Delete
b3.place(x=400, y=425)      #Delete all
b4.place(x=180, y=415)      #Done/Undone
b5.place(x=26, y=425)       #Sort
cal.place(x=550, y=150)     #Calendar
listbox.place(x=30, y=127)  #TaskMenu
combo.place(x=20, y=400)    #Sort(choice)

#b6.place(x=900, y=0)
#b7.place(x=900, y=30)
# ----------------Place geometry-----------------------

# -------------Functions and Variables-----------------

task_list = list()
db = DataBaseService()
word_for_sort = StringVar()
word_for_sort.set(combo.get())


def get_name_month(
        number):
    return calendar.month_name[number]

def get_format_date(
        date):
    return f"{date.day} {get_name_month(date.month)}, {date.year}"

def list_update():
    task_list.clear()
    for i in db.select_values(word_for_sort.get()):
        item = Task(i[0],i[1],i[2])
        task_list.append(item)
    clear_list()
    for item in task_list:
        row = f"{item.title} | {get_format_date(item.deadline)} | {item.status}"
        listbox.insert(END, row)
        item.choose_color_day(cal)
def sort():
    word_for_sort.set(combo.get())
    list_update()
def clear_list():
    cal.calevent_remove()
    listbox.delete(0,END)
def add_task():
    value = e1.get()
    deadline = cal.selection_get()
    if value == "":
        mb.showwarning("Input warning","Entry the task name")
    else:
        item = Task(value,deadline,False)
        task_list.append(item)
        db.insert_value(value, deadline, False)
        list_update()
        e1.delete(0,END)
def delete_alles_task():
    ask = mb.askyesno("Delete all", "Are you sure?")
    if ask:
        task_list.clear()
        db.delete_all()
        list_update()
def del_one():
    try:
        text = listbox.get(listbox.curselection())
        title = text.split(" | ")[0]
        deadline = text.split(" | ")[1]
        for item in task_list:
            if item.title == title and deadline == get_format_date(item.deadline):
                task_list.remove(item)
                db.delete_one(title,deadline)
                list_update()
    except:
        mb.showerror("Cannot delete", "No task item selected ")
def done():
    try:
        text = listbox.get(listbox.curselection())
        title = text.split(" | ")[0]
        deadline = text.split(" | ")[1]
        for item in task_list:
            if item.title == title and deadline == get_format_date(item.deadline):
                item.status = not item.status
                db.update_value(title, deadline, item.status)
                list_update()
    except:
        mb.showerror("Cannot update", "No task item selected ")

#def change_language_uk():
        #b1.configure(text="Додати завдання")
        #b2.configure(text="Вилучити одне завдання")
        #b3.configure(text="Вилучити всі завдання")
        #b4.configure(text="Виконано/Невиконано")
        #b5.configure(text="Сортувати")

#def change_language_eng():
        #b1.configure(text="Add Task")
        #b2.configure(text="Delete")
        #b3.configure(text="Delete all")
        #b4.configure(text="Done/Undone")
        #b5.configure(text="Sort")


#ButtonDesign------------------------------------------
def set_color(event):
    event.widget.config(bg='#4d4c4d', activebackground='#7b7b7c')


def restore_color(event):
    event.widget.config(bg='#a5a5a5')


b1.bind('<Enter>', set_color)
b1.bind('<Leave>', restore_color)

b2.bind('<Enter>', set_color)
b2.bind('<Leave>', restore_color)

b3.bind('<Enter>', set_color)
b3.bind('<Leave>', restore_color)

b4.bind('<Enter>', set_color)
b4.bind('<Leave>', restore_color)

b5.bind('<Enter>', set_color)
b5.bind('<Leave>', restore_color)
#ButtonDesign------------------------------------------

list_update()
screen.mainloop()
# -------------Functions and Variables-----------------