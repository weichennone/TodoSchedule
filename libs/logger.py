import pickle
from os import path
import json


class Logger:
    def __init__(self):
        self.logpath = "log.log"
        self.historypath = "history/history.log"

    # Append finished tasks to the file
    def write_history(self, finished_list):
        with open(self.historypath, 'a') as f:
            dates = sorted(finished_list.keys())
            for date in dates:
                f.write("////" + date + "////\n")
                for history in finished_list[date]:
                    time, task = history
                    f.write(time + '\t\t' + task + '\n')
                f.write('\n')
                del finished_list[date]

    # Write all the tasks to the file
    def save_log(self, tasklist):
        with open(self.logpath, 'wb') as f:
            pickle.dump(tasklist, f)

    # Read the tasks from the file
    def read_log(self):
        tasklist = None
        if path.exists(self.logpath):
            print("exists")
            with open(self.logpath, 'rb') as f:
                tasklist = pickle.load(f)
                # tasklist = json.load(f) # old logger version v0.2
        return tasklist
