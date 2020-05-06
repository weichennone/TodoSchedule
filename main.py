import tkinter as tk
from tkinter import ttk
from os import path
import json

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        
        self.tasklist = {}
        self.serial_num = 0
        self.finished_list = []
        
        self.logpath = "log.log"
        self.historypath = "history.log"
        self.showstr = ""
        
        self.root = master
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        
        self.createWidgets()
        
    def createWidgets(self):
    
        self.button_add = tk.Button(self, text="Add", width=8, command=self.add)
#        self.button_add_to = tk.Button(self, text="Add to", width=8)
#        self.button_start = tk.Button(self, text="Start", width=8)
        self.button_finish = tk.Button(self, text="Finish", width=8, command=self.finish)
#        self.button_delete = tk.Button(self, text="Delete", width=8, command=self.delete)
#        self.button_exit = tk.Button(self, text="Exit", width=8, command=self.finish)
        self.button_add.grid(row = 0, column = 0, sticky = tk.W, pady = 2)
#        self.button_add_to.grid(row = 0, column = 1, sticky = tk.W, pady = 2)
#        self.button_start.grid(row = 0, column = 2, sticky = tk.W, pady = 2)
        self.button_finish.grid(row = 0, column = 1, sticky = tk.W, pady = 2)
#        self.button_delete.grid(row = 0, column = 1, sticky = tk.W, pady = 2)
        
        self.entry = ttk.Entry(self, width=16)
        self.entry.grid(row = 1, column = 0, columnspan=2, sticky = tk.W, pady = 2)
        
        self.text = tk.StringVar()
        self.text.set(self.showstr)
        self.task_display = tk.Label(self, textvariable=self.text)
        
        self.task_display.grid(row = 2, column = 0, columnspan=2, sticky = tk.W, pady = 2)
        
        self.readlog()
        self.display()
    
    # Add a task
    def add(self):
        taskname = self.entry.get()
        self.entry.delete(0, 'end')
        if taskname != "":
            self.tasklist[str(self.serial_num)] = taskname
            self.serial_num += 1
            
            self.display()
    
    # Finish a task
    def finish(self):
        id = self.entry.get()
        self.entry.delete(0, 'end')
        if id != "":
            
            try:
#                id = int(id)
                task_item = self.tasklist[id]
            except ValueError:
                return
            
            self.finished_list.append(task_item)
            del self.tasklist[id]
            
            self.display()
    
    # Delete a task
    def delete(self):
        id = self.entry.get()
        if id != "":
            pass # check id is integer
    
    # Update the self.task_display
    def display(self):
        self.showstr = ""
        for k in self.tasklist:
            self.showstr += "\t".join([k, self.tasklist[k]])
            self.showstr += "\n"
            self.serial_num = max(self.serial_num, int(k))
        self.serial_num += 1
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
    
    # Append finished tasks to the file
    def writehistory(self):
        with open(self.historypath, 'a') as f:
            for history in self.finished_list:
                f.write(history)
                f.write('\n')
        
if __name__ == '__main__':
    app = Application(tk.Tk())
    app.mainloop()
