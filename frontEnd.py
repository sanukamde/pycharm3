from backEnd import *
from tkinter import *

# creating threads
thread_list = []
for i in range(1, 7):
    thread = GreenhouseGas(i)
    thread_list.append(thread)
for thread in thread_list:
    thread.start()
    thread.scrape_page()
    thread.join()
sql_table = MySQLite()
sql_table.build_SQLite_table()
sql_table.update_data_SQLite_table(thread_list)


def sel():
    if var.get() == 1:
        selection = "You selected the CO2 graph"
        label.config(text=selection)
        sql_table.graph_builder(0)
    elif var.get() == 2:
        selection = "You selected the CH4 graph"
        label.config(text=selection)
        sql_table.graph_builder(1)
    elif var.get() == 3:
        selection = "You selected the NO2 graph"
        label.config(text=selection)
        sql_table.graph_builder(2)
    elif var.get() == 4:
        selection = "You selected the CFC12 graph"
        label.config(text=selection)
        sql_table.graph_builder(3)
    elif var.get() == 5:
        selection = "You selected the CFC12 graph"
        label.config(text=selection)
        sql_table.graph_builder(4)
    elif var.get() == 6:
        selection = "You selected the 15-minor graph"
        label.config(text=selection)
        sql_table.graph_builder(5)


root = Tk()
root.geometry("300x200")
w = Label(root, text="Choose a graph to view:")
w.pack()
var = IntVar()

co2 = Radiobutton(root, text="CO2 Graph", variable=var, value=1, command=sel)
co2.pack(anchor=W)

ch4 = Radiobutton(root, text="CH4 Graph", variable=var, value=2, command=sel)
ch4.pack(anchor=W)

no2 = Radiobutton(root, text="NO2 Graph", variable=var, value=3, command=sel)
no2.pack(anchor=W)

cfc12 = Radiobutton(root, text="CFC12 Graph", variable=var, value=4, command=sel)
cfc12.pack(anchor=W)

cfc11 = Radiobutton(root, text="CFC11 Graph", variable=var, value=5, command=sel)
cfc11.pack(anchor=W)

minor15 = Radiobutton(root, text="15-minor Graph", variable=var, value=6, command=sel)
minor15.pack(anchor=W)

label = Label(root)
label.pack()

button = Button(root, text='Quit', command=root.destroy)
button.pack()

root.mainloop()
sql_table.close_SQLite_table()
