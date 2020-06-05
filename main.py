import tkinter as tk
from tkinter import ttk
from libs import task


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.tasklist = task.TaskTree()
        self.tasktree = None

        self.showstr = ""
        self.activestr = "None"

        self.root = master
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.createWidgets()

    def createWidgets(self):

        self.button_add = tk.Button(self, text="Add", width=8, command=self.add)
        self.button_add_to = tk.Button(self, text="Add to", width=8, command=self.add_to)
        self.button_start = tk.Button(self, text="Start", width=8, command=self.start)
        self.button_finish = tk.Button(self, text="Finish", width=8, command=self.finish)
        self.button_delete = tk.Button(self, text="Delete", width=8, command=self.delete)
        self.button_stop = tk.Button(self, text="Stop", width=8, command=self.stop)
        #        self.button_exit = tk.Button(self, text="Exit", width=8, command=self.finish)
        self.button_add.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.button_add_to.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.button_start.grid(row=0, column=3, sticky=tk.W, pady=2)
        self.button_stop.grid(row=0, column=4, sticky=tk.W, pady=2)
        self.button_finish.grid(row=0, column=5, sticky=tk.W, pady=2)
        self.button_delete.grid(row=0, column=2, sticky=tk.W, pady=2)

        self.label_id = tk.Label(self, text="ID:", width=8, justify=tk.RIGHT)
        self.label_id.grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_id = ttk.Entry(self, width=8)
        self.entry_id.grid(row=1, column=1, sticky=tk.W, pady=2)

        self.label_task = tk.Label(self, text="Task:", width=8, justify=tk.RIGHT)
        self.label_task.grid(row=1, column=2, sticky=tk.W, pady=2)
        self.entry_task = ttk.Entry(self, width=24)
        self.entry_task.grid(row=1, column=3, columnspan=3, sticky=tk.W, pady=2)

        self.active_reminder = tk.Label(self, text="Active:", width=8, justify=tk.LEFT)
        self.active_reminder.grid(row=2, column=0, columnspan=1, sticky=tk.W, pady=2)

        self.active_text = tk.StringVar()
        self.active_text.set(self.activestr)
        self.active_display = tk.Label(self, textvariable=self.active_text, justify=tk.LEFT)
        self.active_display.grid(row=2, column=1, columnspan=4, sticky=tk.W, pady=2)

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(row=3, column=6, sticky='ns')

        self.task_display = ttk.Treeview(self, columns=('ID', 'Task', 'Created Time'), height=30, yscrollcommand=scrollbar.set)
        for col in ('ID', 'Task', 'Created Time'):
            self.task_display.heading(col, text=col)
        self.task_display.grid(row=3, column=0, columnspan=6)
        self.task_display.column('#0', width=20, anchor='nw')
        self.task_display.column("ID", width=60, anchor='nw')
        self.task_display.column("Task", width=260, anchor='nw')
        self.task_display.column("Created Time", width=130, anchor='center')

        self.statistics_header = tk.Label(self, text="Stat:", width=8, justify=tk.LEFT)
        self.statistics_header.grid(row=4, column=0, columnspan=1, sticky=tk.W, pady=2)

        self.stat_canvas = tk.Canvas(self, width=400, height=20)
        self.stat_canvas.create_rectangle(0, 0, 400, 20, outline="light gray", fill="light gray")
        self.stat_canvas.grid(row=4, column=1, columnspan=5, sticky=tk.W, pady=2)

        self.tasklist.construct_from_log()
        self.refresh()

    # Add a task
    def add(self):
        taskname = self.entry_task.get()
        if taskname:
            self.tasklist.add_task(taskname)
            self.refresh()

    # Add a task
    def add_to(self):
        id = self.entry_id.get()
        taskname = self.entry_task.get()
        if id and taskname:
            self.tasklist.add_task(taskname, id)
            self.refresh()

    # Finish a task
    def finish(self):
        id = self.entry_id.get()
        if id:
            self.tasklist.finish_task(id)
            self.refresh()

    # Delete a task
    def delete(self):
        id = self.entry_id.get()
        if id:
            self.tasklist.finish_task(id, False)
            self.refresh()

    def start(self):
        id = self.entry_id.get()
        if id:
            self.tasklist.start_task(id)
            self.refresh()

    def stop(self):
        id = self.entry_id.get()
        if id:
            self.tasklist.stop_task(id)
            self.refresh()

    def entertain(self):
        pass

    def exercise(self):
        pass

    def cook_eat(self):
        pass

    # Update the self.task_display
    def display(self):
        if self.tasklist.active_task:
            self.activestr = '(' + self.tasklist.active_task.id + ')\t' + self.tasklist.active_task.get_name()
        else:
            self.activestr = "None"
        self.active_text.set(self.activestr)

        self.task_display.delete(*self.task_display.get_children())
        for k in self.tasktree:
            # if isinstance(self.tasktree[k], list):
            root_task, subtask_dict = self.tasktree[k]
            dt = root_task.create_time
            created_time = "{:02d}/{:02d} {:02d}:{:02d}".format(dt.month, dt.day, dt.hour, dt.minute)
            idx = self.task_display.insert('', 'end', value=(k, root_task.get_name(), created_time), open=True)

            # show subtasks
            for k2 in subtask_dict:
                dt = subtask_dict[k2].create_time
                created_time = "{:02d}/{:02d} {:02d}:{:02d}".format(dt.month, dt.day, dt.hour, dt.minute)
                self.task_display.insert(idx, 'end', value=(k2, " |_. " + subtask_dict[k2].get_name(), created_time))

            # if the subtask doesn't exist
            # else:
            #     self.task_display.insert('', 'end', value=(k, self.tasktree[k]))
        # self.stat_canvas.create_rectangle(0, 0, 400, 20, outline="light gray", fill="light gray")

    def refresh(self):
        self.entry_id.delete(0, 'end')
        self.entry_task.delete(0, 'end')
        self.tasktree = self.tasklist.generate_tree_view()
        self.display()

    # Exit the app
    def exit(self):
        self.tasklist.terminate()
        self.root.destroy()


if __name__ == '__main__':
    app = Application(tk.Tk())
    app.mainloop()
