import tkinter as tk
from tkinter import ttk
from libs import task_v0_4
from libs import dialogs


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.tasklist = task_v0_4.TaskTree()
        self.tasktree = None
        # self.today_schedule = {}
        self.viewid2list = {}
        self.scheduleviewid2list = {}

        # self.showstr = ""
        self.activestr = "None"

        self.root = master
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.color_dict = {'rest': 'dim gray',
                           'work': 'deep sky blue',
                           'creative': 'DarkOrchid1',
                           'labor': 'orange',
                           'exercise': 'red',
                           'entertain': 'green2',
                           'eating': 'white smoke',
                           'misc': 'cyan'}

        self.createWidgets()

    def createWidgets(self):
        """
        Define the display of the main window
        :return:
        """
        # Control button
        self.button_add = tk.Button(self, text="Add", width=8, command=self.add)
        self.button_assign = tk.Button(self, text="Assign", width=8, command=self.assign)
        self.button_start = tk.Button(self, text="Start", width=8, command=self.start)
        self.button_finish = tk.Button(self, text="Finish", width=8, command=self.finish)
        self.button_delete = tk.Button(self, text="Delete", width=8, command=self.delete)
        self.button_stop = tk.Button(self, text="Stop", width=8, command=self.stop)
        self.button_add.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.button_assign.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.button_start.grid(row=0, column=3, sticky=tk.W, pady=2)
        self.button_stop.grid(row=0, column=4, sticky=tk.W, pady=2)
        self.button_finish.grid(row=0, column=5, sticky=tk.W, pady=2)
        self.button_delete.grid(row=0, column=2, sticky=tk.W, pady=2)

        # self.label_id = tk.Label(self, text="ID:", width=8, justify=tk.RIGHT)
        # self.label_id.grid(row=1, column=0, sticky=tk.W, pady=2)
        # self.entry_id = ttk.Entry(self, width=8)
        # self.entry_id.grid(row=1, column=1, sticky=tk.W, pady=2)

        # self.label_task = tk.Label(self, text="Task:", width=8, justify=tk.RIGHT)
        # self.label_task.grid(row=1, column=2, sticky=tk.W, pady=2)
        # self.entry_task = ttk.Entry(self, width=24)
        # self.entry_task.grid(row=1, column=3, columnspan=3, sticky=tk.W, pady=2)

        # Highlight
        self.active_reminder = tk.Label(self, text="Active:", width=8, justify=tk.LEFT)
        self.active_reminder.grid(row=1, column=0, columnspan=1, sticky=tk.W, pady=2)

        self.active_text = tk.StringVar()
        self.active_text.set(self.activestr)
        self.active_display = tk.Label(self, textvariable=self.active_text, justify=tk.LEFT, bg='ivory2')
        self.active_display.grid(row=1, column=1, columnspan=4, sticky=tk.W, pady=2)

        # Tab Control
        self.tabControl = ttk.Notebook(self)
        self.tabControl.grid(row=2, column=0, columnspan=6)
        self.tab_task_pool = ttk.Frame(self.tabControl)
        self.tab_schedule = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_task_pool, text='Task Pool')
        self.tabControl.add(self.tab_schedule, text='Schedule')

        # Task pool tab
        scrollbar = tk.Scrollbar(self.tab_task_pool)
        scrollbar.grid(row=0, column=6, sticky='ns')

        self.task_display = ttk.Treeview(self.tab_task_pool, columns=('ID', 'Task', 'Created Time'), height=30, yscrollcommand=scrollbar.set)
        for col in ('ID', 'Task', 'Created Time'):
            self.task_display.heading(col, text=col)
        self.task_display.grid(row=0, column=0, columnspan=6)
        self.task_display.column('#0', width=20, anchor='nw')
        self.task_display.column("ID", width=60, anchor='nw')
        self.task_display.column("Task", width=260, anchor='nw')
        self.task_display.column("Created Time", width=130, anchor='center')

        # Schedule tab
        scrollbar_schedule = tk.Scrollbar(self.tab_schedule)
        scrollbar_schedule.grid(row=0, column=6, sticky='ns')

        self.schedule_display = ttk.Treeview(self.tab_schedule, columns=('Task', 'Priority'), height=30,
                                         yscrollcommand=scrollbar_schedule.set)
        for col in ('Task', 'Priority'):
            self.schedule_display.heading(col, text=col)
        self.schedule_display.grid(row=0, column=0, columnspan=6)
        self.schedule_display.column('#0', width=20, anchor='nw')
        self.schedule_display.column("Task", width=350, anchor='nw')
        self.schedule_display.column("Priority", width=100, anchor='center')

        # Statistics
        self.statistics_header = tk.Label(self, text="Stat:", width=8, justify=tk.LEFT)
        self.statistics_header.grid(row=3, column=0, columnspan=1, sticky=tk.W, pady=2)

        self.stat_canvas = tk.Canvas(self, width=400, height=20)
        self.stat_canvas.create_rectangle(0, 0, 400, 20, outline="light gray", fill="light gray")
        self.stat_canvas.grid(row=3, column=1, columnspan=5, sticky=tk.W, pady=2)

        # self.frame = tk.Frame(self, width=200, height=30)
        # self.frame.grid(row=4, column=0)

        self.tasklist.construct_from_log()
        self.refresh()

    # Add a task
    def add(self):
        # taskname = self.entry_task.get()

        d = dialogs.AddTask(self)
        self.wait_window(d.top)
        # print(d.result)
        if d.result:
            taskname, pid, priority, task_type = d.result

            # input check
            if taskname:
                self.tasklist.add_task(taskname, pid, priority, task_type)
                self.refresh()

    # Add a task
    def assign(self):
        # d = dialogs.AssignTask(self)
        # self.wait_window(d.top)
        item = self.task_display.focus()
        if item:
            id = self.viewid2list[item]
            # print(id)
        # if d.result:
        #     pid = d.result

            if id:
                # print("has item")
                self.tasklist.schedule[id] = self.tasklist.get_task(id)
                print(self.tasklist.schedule)
                self.refresh()
        # item = self.task_display.focus()
        # id = self.viewid2list[item]
        # task = self.tasklist.get_task(id)
        # print(task.priority, task.task_type, task.name)
        # id = self.entry_id.get()
        # taskname = self.entry_task.get()
        #
        # # input check
        # if id and taskname:
        #     self.tasklist.add_task(taskname, id)
        #     self.refresh()

    # Finish a task
    def finish(self):
        item = self.task_display.focus()
        if item:
            id = self.viewid2list[item]
            self.tasklist.finish_task(id)
            self.refresh()
        item = self.schedule_display.focus()
        if item:
            id = self.scheduleviewid2list[item]
            self.tasklist.finish_task(id)
            self.refresh()

    # Delete a task
    def delete(self):
        item = self.task_display.focus()
        if item:
            id = self.viewid2list[item]
            self.tasklist.finish_task(id, False)
            self.refresh()
        item = self.schedule_display.focus()
        if item:
            id = self.scheduleviewid2list[item]
            self.tasklist.finish_task(id, False)
            self.refresh()

    def start(self):
        item = self.task_display.focus()
        if item:
            id = self.viewid2list[item]
            self.tasklist.start_task(id)
            self.refresh()
        item = self.schedule_display.focus()
        if item:
            id = self.scheduleviewid2list[item]
            self.tasklist.start_task(id)
            self.refresh()

    def stop(self):
        item = self.task_display.focus()
        if item:
            id = self.viewid2list[item]
            self.tasklist.stop_task(id)
            self.refresh()
        item = self.schedule_display.focus()
        if item:
            id = self.scheduleviewid2list[item]
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

        # show active task
        if self.tasklist.active_task:
            self.activestr = '(' + self.tasklist.active_task.id + ') ' + self.tasklist.active_task.get_name()
        else:
            self.activestr = "None"
        self.active_text.set(self.activestr)

        # display all tasks
        self.task_display.delete(*self.task_display.get_children())
        self.viewid2list = {}
        for k in self.tasktree:
            # if isinstance(self.tasktree[k], list):
            root_task, subtask_dict = self.tasktree[k]
            dt = root_task.create_time
            created_time = "{:02d}/{:02d} {:02d}:{:02d}".format(dt.month, dt.day, dt.hour, dt.minute)
            idx = self.task_display.insert('', 'end', value=(k, root_task.get_name(), created_time), open=True)
            # print(idx, root_task.get_name())
            self.viewid2list[idx] = k

            # show subtasks
            for k2 in subtask_dict:
                dt = subtask_dict[k2].create_time
                created_time = "{:02d}/{:02d} {:02d}:{:02d}".format(dt.month, dt.day, dt.hour, dt.minute)
                idx2 = self.task_display.insert(idx, 'end', value=(k2, " |_. " + subtask_dict[k2].get_name(), created_time))
                self.viewid2list[idx2] = k2
        # print(self.viewid2list)

        # display schedule
        self.schedule_display.delete(*self.schedule_display.get_children())
        self.scheduleviewid2list = {}
        for k in self.tasklist.schedule:
            # if isinstance(self.tasktree[k], list):
            schedule = self.tasklist.schedule[k]
            if hasattr(schedule, 'priority'):
                priority = schedule.priority
            else:
                priority = 'medium'

            if schedule.is_root:
                show_name = schedule.get_name()
            else:
                pid = schedule.parent
                p_task = self.tasklist.get_task(pid)
                show_name = p_task.get_name() + ": " + schedule.get_name()
            idx = self.schedule_display.insert('', 'end',
                                               value=(show_name, priority),
                                               open=True)
            # print(idx, root_task.get_name())
            self.scheduleviewid2list[idx] = k

        # display daily stats
        start_p = 0
        # self.tasklist.task_stat = [('rest', 5000), ('creative', 2000), ('labor', 3000), ('exercise', 4000), ('entertain', 5000),
        #                            ('misc', 6000), ('eating', 2000)]
        # print("here")
        for stat in self.tasklist.task_stat:
            length = int(stat[1] / 216)
            self.stat_canvas.create_rectangle(start_p, 0, start_p + length, 20, outline=self.color_dict[stat[0]], fill=self.color_dict[stat[0]])
            start_p += length
        if start_p < 400:
            self.stat_canvas.create_rectangle(start_p, 0, 400, 20, outline="light gray", fill="light gray")

    def refresh(self):
        # self.entry_id.delete(0, 'end')
        # self.entry_task.delete(0, 'end')
        self.tasktree = self.tasklist.generate_tree_view()
        self.display()

    # Exit the app
    def exit(self):
        self.tasklist.terminate()
        self.root.destroy()


if __name__ == '__main__':
    window = tk.Tk()
    window.title("TodoSchedule")
    app = Application(window)
    app.mainloop()
