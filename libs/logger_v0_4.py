import pickle
from os import path
import json
from datetime import datetime
from datetime import timedelta


class Logger:
    def __init__(self):
        self.logpath = "log_test/log_test1.log"
        self.historypath = "log_test/history_test.log"
        self.timestatpath = "log_test/time_stat.log"

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

    def save_time_stat(self, time_stat):
        dt = datetime.now()
        date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
        with open(self.timestatpath, 'a') as f:
            # pickle.dump((date, time_stat), f)
            f.write(date + '\t\t')
            f.write(' | '.join([':'.join([str(ele[0]), str(ele[1])]) for ele in time_stat]))
            f.write('\n')

    def read_time_stat(self):
        all_time_stat = {}
        if path.exists(self.timestatpath):
            print("exists")
            with open(self.timestatpath) as f:
                for line in f:
                    info = line.strip().split('\t\t')
                    assert len(info) == 2
                    all_time_stat[info[0]] = []
                    for ele in info[1].split(' | '):
                        task, t = ele.split(':')
                        all_time_stat[info[0]].append((task, float(t)))
        #         while True:
        #             try:
        #                 time_stat = pickle.load(f)
        #                 if isinstance(time_stat, tuple):
        #                     all_time_stat[time_stat[0]] = time_stat[1]
        #             except EOFError:
        #                 break
                # tasklist = json.load(f) # old logger version v0.2
        return all_time_stat

    def read_today_time_stat(self):
        time_stat = []
        dt = datetime.now()
        date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
        if path.exists(self.timestatpath):
            print("exists")
            with open(self.timestatpath) as f:
                for line in f:
                    info = line.strip().split('\t\t')
                    assert len(info) == 2
                    if date == info[0]:
                        for ele in info[1].split(' | '):
                            task, t = ele.split(':')
                            time_stat.append((task, timedelta(seconds=float(t)).total_seconds()))
        return time_stat
