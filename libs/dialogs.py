import tkinter as tk
from tkinter import ttk


class AddTask:

    def __init__(self, parent):

        top = self.top = tk.Toplevel(parent)

        label_taskname = tk.Label(top, text="Task Name:", width=8, justify=tk.LEFT)
        label_to = tk.Label(top, text="To:", width=8, justify=tk.LEFT)
        self.e_task = tk.Entry(top, width=24)
        self.e_task_to = tk.Entry(top, width=8)

        label_taskname.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.e_task.grid(row=0, column=1, columnspan=3, sticky=tk.W, pady=2)
        label_to.grid(row=4, column=0, sticky=tk.W, pady=2)
        self.e_task_to.grid(row=4, column=1, sticky=tk.W, pady=2)

        label_priority = tk.Label(top, text="Priority:", width=8, justify=tk.LEFT)
        self.priority = tk.StringVar()
        self.priority.set('medium')
        high = ttk.Radiobutton(top, text='High', variable=self.priority, value='high', width=8)
        medium = ttk.Radiobutton(top, text='Medium', variable=self.priority, value='medium', width=8)
        low = ttk.Radiobutton(top, text='Low', variable=self.priority, value='low', width=8)

        label_priority.grid(row=1, column=0, sticky=tk.W, pady=2)
        high.grid(row=1, column=1, sticky=tk.W, pady=2)
        medium.grid(row=1, column=2, sticky=tk.W, pady=2)
        low.grid(row=1, column=3, sticky=tk.W, pady=2)

        label_type = tk.Label(top, text="Type:", width=8, justify=tk.LEFT)
        self.type = tk.StringVar()
        self.type.set('misc')
        creative_task = ttk.Radiobutton(top, text='Creative', variable=self.type, value='creative', width=8)
        labor_task = ttk.Radiobutton(top, text='Labor', variable=self.type, value='labor', width=8)
        exercise = ttk.Radiobutton(top, text='Exercise', variable=self.type, value='exercise', width=8)
        entertain = ttk.Radiobutton(top, text='Entertain', variable=self.type, value='entertain', width=8)
        misc = ttk.Radiobutton(top, text='Misc', variable=self.type, value='misc', width=8)
        eating = ttk.Radiobutton(top, text='Eating', variable=self.type, value='eating', width=8)

        label_type.grid(row=2, column=0, sticky=tk.W, pady=2)
        creative_task.grid(row=2, column=1, sticky=tk.W, pady=2)
        labor_task.grid(row=2, column=2, sticky=tk.W, pady=2)
        misc.grid(row=2, column=3, sticky=tk.W, pady=2)
        exercise.grid(row=3, column=1, sticky=tk.W, pady=2)
        entertain.grid(row=3, column=2, sticky=tk.W, pady=2)
        eating.grid(row=3, column=3, sticky=tk.W, pady=2)

        b_add = tk.Button(top, text="Add", command=self.add, width=8)
        b_cancel = tk.Button(top, text="Cancel", command=self.cancel, width=8)

        b_add.grid(row=4, column=2, sticky=tk.W, pady=2)
        b_cancel.grid(row=4, column=3, sticky=tk.W, pady=2)

        self.result = None

    def add(self):

        self.result = (self.e_task.get(), self.e_task_to.get(), self.priority.get(), self.type.get())

        self.top.destroy()

    def cancel(self):
        self.top.destroy()


class AssignTask:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        label_id = tk.Label(top, text="Task ID:", width=8, justify=tk.LEFT)
        self.e_id = tk.Entry(top, width=8)
        label_id.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.e_id.grid(row=0, column=1, sticky=tk.W, pady=2)

        b_add = tk.Button(top, text="Assign", command=self.assign, width=8)
        b_cancel = tk.Button(top, text="Cancel", command=self.cancel, width=8)

        b_add.grid(row=1, column=0, sticky=tk.W, pady=2)
        b_cancel.grid(row=1, column=1, sticky=tk.W, pady=2)

        self.result = None

    def assign(self):
        self.result = self.e_id.get()
        self.top.destroy()

    def cancel(self):
        self.top.destroy()


class ShowHistoryTimeStat:
    def __init__(self, parent, time_stats):
        top = self.top = tk.Toplevel(parent)

        self.stat_canvas = tk.Canvas(top, width=400, height=20)
        self.stat_canvas.create_rectangle(0, 0, 400, 20, outline="light gray", fill="light gray")
        self.stat_canvas.grid(row=4, column=1, columnspan=5, sticky=tk.W, pady=2)

