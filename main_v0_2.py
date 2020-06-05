import tkinter as tk
from tkinter import ttk
from os import path
from datetime import datetime
import json


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        
        self.tasklist = {} # key: serial number, value: (task name, dict for sub tasks) or task name
        self.finished_list = {}
        self.parent_task = {}
        
        dt = datetime.now()
        self.current_date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
        
        self._serial_num = 0
        self._idset = set()
        
        self.logpath = "log.log"
        self.historypath = "history/history.log"
        self.showstr = ""
        
        self.root = master
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        
        self.createWidgets()
        
    def createWidgets(self):
    
        self.button_add = tk.Button(self, text="Add", width=8, command=self.add)
        self.button_add_to = tk.Button(self, text="Add to", width=8, command=self.add_to)
#        self.button_start = tk.Button(self, text="Start", width=8)
        self.button_finish = tk.Button(self, text="Finish", width=8, command=self.finish)
#        self.button_delete = tk.Button(self, text="Delete", width=8, command=self.delete)
#        self.button_exit = tk.Button(self, text="Exit", width=8, command=self.finish)
        self.button_add.grid(row = 0, column = 1, sticky = tk.W, pady = 2)
        self.button_add_to.grid(row = 0, column = 3, sticky = tk.W, pady = 2)
#        self.button_start.grid(row = 0, column = 2, sticky = tk.W, pady = 2)
        self.button_finish.grid(row = 0, column = 4, sticky = tk.W, pady = 2)
#        self.button_delete.grid(row = 0, column = 1, sticky = tk.W, pady = 2)

        self.label_id = tk.Label(self, text="ID:", width=8, justify=tk.RIGHT)
        self.label_id.grid(row = 1, column = 0, sticky = tk.W, pady = 2)
        self.entry_id = ttk.Entry(self, width=8)
        self.entry_id.grid(row = 1, column = 1, sticky = tk.W, pady = 2)
        
        self.label_task = tk.Label(self, text="Task:", width=8, justify=tk.RIGHT)
        self.label_task.grid(row = 1, column = 2, sticky = tk.W, pady = 2)
        self.entry_task = ttk.Entry(self, width=16)
        self.entry_task.grid(row = 1, column = 3, columnspan=2, sticky = tk.W, pady = 2)
        
        self.text = tk.StringVar()
        self.text.set(self.showstr)
        self.task_display = tk.Label(self, textvariable=self.text, justify=tk.LEFT)
        
        self.task_display.grid(row = 2, column = 0, columnspan=5, sticky = tk.W, pady = 2)
        
        self.readlog()
        self.display()
    
    def _assign_id(self):
        
        while str(self._serial_num) in self._idset:
            self._serial_num += 1
            self._serial_num %= 1024
        
        self._idset.add(str(self._serial_num))
        return str(self._serial_num)
        
    def _collect_id(self, id):
        self._idset.remove(id)
    
    # Add a task
    def add(self):
        taskname = self.entry_task.get()
        self.entry_task.delete(0, 'end')
        if taskname != "":
#            self.serial_num += 1
            sid = self._assign_id()
            self.tasklist[sid] = taskname
#            self.tasklist[str(self.serial_num)] = taskname
            
            self.display()
            
    # Add a task
    def add_to(self):
        id = self.entry_id.get()
        taskname = self.entry_task.get()
        self.entry_id.delete(0, 'end')
        self.entry_task.delete(0, 'end')
        if taskname != "":
#            self.serial_num += 1
            sid = self._assign_id()
            
            # if the subtask exists, add a new subtask to the dict
            if isinstance(self.tasklist[id], list):
                root_task, subtask_dict = self.tasklist[id]
                subtask_dict[sid] = taskname
#                subtask_dict[str(self.serial_num)] = taskname
            
            # if the subtask doesn't exist, create a dict and add a new subtask
            else:
                root_task = self.tasklist[id]
                subtask_dict = {sid: taskname}
#                subtask_dict = {str(self.serial_num): taskname}
            self.tasklist[id] = [root_task, subtask_dict]
            
            # add link from subtask to parent task
            self.parent_task[sid] = id
#            self.parent_task[str(self.serial_num)] = id
            
            self.display()
    
    # Finish a task
    def finish(self):
        id = self.entry_id.get()
        self.entry_id.delete(0, 'end')
        
        dt = datetime.now()
        date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
        time = "{:2d}:{:02d}:{:02d}".format(dt.hour, dt.minute, dt.second)
        
        if date != self.current_date:
            self.writehistory()
            self.current_date = date
        
        # if finish a parent task
        if id != "" and id in self.tasklist:
#            print("root")
        
            if isinstance(self.tasklist[id], list):
                if len(self.tasklist[id][1]) > 0:
                    return
                else:
                    task_item = self.tasklist[id][0]
            
            else:
                task_item = self.tasklist[id]
            
            if date in self.finished_list:
                self.finished_list[date].append((time, task_item))
            else:
                self.finished_list[date] = [(time, task_item)]
            
            del self.tasklist[id]
            self._collect_id(id)
            
            self.display()
        
        # if finish a subtask
        elif id in self.parent_task and self.parent_task[id] in self.tasklist:
#            print("sub")
            
            pid = self.parent_task[id]
            root_task, subtask_dict = self.tasklist[pid]
            task_item = subtask_dict[id]
            
#            dt = datetime.now()
#            date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
#            time = "{:2d}:{:02d}:{:02d}".format(dt.hour, dt.minute, dt.second)
            
            if date in self.finished_list:
                self.finished_list[date].append((time, root_task + ": " + task_item))
            else:
                self.finished_list[date] = [(time, root_task + ": " + task_item)]
#            print(root_task + ": " + task_item)
            
            del subtask_dict[id]
            del self.parent_task[id]
            self._collect_id(id)
            self.tasklist[pid] = [root_task, subtask_dict]
            
            self.display()
    
    # Delete a task
    def delete(self):
        id = self.entry.get()
        if id != "":
            pass # check id is integer
    
    # Update the self.task_display
    def display(self):
        self.showstr = "\t".join(["ID", "TODO"])
        self.showstr += "\n"
        self.showstr += "\t".join(["----", "--------"])
        for k in self.tasklist:
            self.showstr += "\n\n"
            
            # if the subtask exists
            if isinstance(self.tasklist[k], list):
                root_task, subtask_dict = self.tasklist[k]
                self.showstr += "\t".join([k, root_task])
                
                # show subtasks
                for k2 in subtask_dict:
                    self.showstr += "\n"
                    self.showstr += "\t".join([k2, "|_. " + subtask_dict[k2]])
            
            # if the subtask doesn't exist
            else:
                self.showstr += "\t".join([k, self.tasklist[k]])
            
#            self.serial_num = max(self.serial_num, int(k))
#        self.serial_num += 1
        self.text.set(self.showstr)
            
    # Exit the app
    def exit(self):
        self.writelog()
        self.writehistory()
        self.root.destroy()
    
    # Write all the tasks to the file
    def writelog(self):
        with open(self.logpath, 'w') as f:
            json.dump(self.tasklist, f)
    
    # Read the tasks from the file
    def readlog(self):
        if path.exists(self.logpath):
            with open(self.logpath, 'r') as f:
                self.tasklist = json.load(f)
#        print(self.tasklist)
        
        # re-create parent dict
        for k in self.tasklist:
            self._idset.add(k)
            if isinstance(self.tasklist[k], list):
                root_task, subtask_dict = self.tasklist[k]
                for k2 in subtask_dict:
                    self._idset.add(k2)
                    self.parent_task[k2] = k
    
    # Append finished tasks to the file
    def writehistory(self):
        with open(self.historypath, 'a') as f:
            dates = self.finished_list.keys()
            dates = sorted(dates)
            for date in dates:
                f.write("////" + date + "////\n")
                for history in self.finished_list[date]:
                    time, task = history
                    f.write(time + '\t\t' + task + '\n')
                f.write('\n')
                del self.finished_list[date]


if __name__ == '__main__':
    app = Application(tk.Tk())
    app.mainloop()
