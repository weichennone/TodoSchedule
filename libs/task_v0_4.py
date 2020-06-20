from datetime import datetime
from datetime import timedelta
import libs.logger_v0_4 as logger


class Task:
    def __init__(self, name, id, priority='medium', task_type='misc'):
        self.name = name
        self.id = id

        self.task_type = task_type
        self.priority = priority

        self.create_time = datetime.now()
        self.start_time = []
        self.stop_end_time = []
        self.elapsed_time = 0

        self.is_root = True
        self.parent = None
        self.successors = set()

        self.done = False
        self.running = False

    def start(self):
        if not self.running:
            self.start_time.append(datetime.now())
            self.running = True

    def stop(self):
        # problem: if the task is not running, it can also be stopped/finished?
        if self.running:
            self.stop_end_time.append(datetime.now())
            self.running = False
            duration = (self.stop_end_time[-1] - self.start_time[-1]).total_seconds()
            self.elapsed_time += duration
            return duration
        return 0

    def finish(self):
        if self.have_successor():
            # print(self.successors)
            return -2  # have successor, cannot terminate
        if self.running:
            self.stop_end_time.append(datetime.now())
            self.running = False
            duration = (self.stop_end_time[-1] - self.start_time[-1]).total_seconds()
            self.elapsed_time += duration

        if self.have_parent():
            return self.parent
        else:
            return -1  # root task, directly terminate

    def get_name(self):
        return self.name

    def get_parent_id(self):
        return self.parent

    def get_successors(self):
        return self.successors

    def add_parent(self, id):
        self.is_root = False
        self.parent = id

    def add_successor(self, id):
        self.successors.add(id)

    def have_parent(self):
        return not self.is_root

    def have_successor(self):
        return len(self.successors) > 0

    def finish_successor(self, id):
        if id in self.successors:
            self.successors.remove(id)

    def generate_log(self):
        pass


class TaskTree:
    def __init__(self):
        self._serial_num = 0
        self._idset = set()

        self.task_dict = {}
        self.finished_list = {}
        self.logger = logger.Logger()

        dt = datetime.now()
        self.current_date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)

        self.active_task = None

        self.task_stat = []
        self.last_update = None

        self.schedule = {}

    def add_task(self, name, id=None, priority='medium', task_type='misc'):
        if name != "":
            sid = self._assign_id()
            task = Task(name, sid, priority, task_type)
            if id:
                task.add_parent(id)
                parent_task = self.get_task(id)
                parent_task.add_successor(sid)
            self.task_dict[sid] = task

    def get_task(self, id):
        return self.task_dict[id]

    def start_task(self, id):
        if self.active_task:
            self.active_task.stop()
        task = self.get_task(id)
        self.active_task = task
        task.start()
        self.time_manager()

    def stop_task(self, id):
        task = self.get_task(id)
        if task == self.active_task:
            self.active_task = None
        task.stop()
        self.time_manager(start=False)

    def finish_task(self, id, done=True):
        task = self.get_task(id)
        parent_id = task.finish()

        dt = datetime.now()
        date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
        time = "{:2d}:{:02d}:{:02d}".format(dt.hour, dt.minute, dt.second)

        # print(parent_id, time)
        if parent_id == -2:
            return None
        else:
            taskname = task.get_name()
            if parent_id != -1:
                parent_task = self.get_task(parent_id)
                parent_task.finish_successor(id)
                taskname = parent_task.get_name() + ": " + taskname
            if date in self.finished_list:
                self.finished_list[date].append((time, taskname))
            else:
                self.finished_list[date] = [(time, taskname)]
            del self.task_dict[id]
            # print(self.schedule)
            if id in self.schedule:
                del self.schedule[id]
            task.done = done
            if task == self.active_task:
                self.active_task = None
            self.time_manager(start=False)
            return task
        # if parent_id == -1:
        #     del self.task_dict[id]
        #     if date in self.finished_list:
        #         self.finished_list[date].append((time, task.get_name()))
        #     else:
        #         self.finished_list[date] = [(time, task.get_name())]
        #     task.done = done
        #     if task == self.active_task:
        #         self.active_task = None
        #     self.time_manager(start=False)
        #     return task
        # elif parent_id == -2:
        #     return None
        # else:
        #     del self.task_dict[id]
        #     parent_task = self.get_task(parent_id)
        #     parent_task.finish_successor(id)
        #     if date in self.finished_list:
        #         self.finished_list[date].append((time, parent_task.get_name() + ": " + task.get_name()))
        #     else:
        #         self.finished_list[date] = [(time, parent_task.get_name() + ": " + task.get_name())]
        #     task.done = done
        #     if task == self.active_task:
        #         self.active_task = None
        #     self.time_manager(start=False)
        #     return task

    def reset(self):
        dt = datetime.now()
        date = "{:4d}{:02d}{:02d}".format(dt.year, dt.month, dt.day)
        if date != self.current_date:
            self.logger.write_history(self.finished_list)
            self.current_date = date
            self.task_stat = []
            self.last_update = None
            self.schedule = {}

    def generate_tree_view(self):
        task_tree = {}
        self.reset()
        for k in self.task_dict:
            task = self.task_dict[k]
            if not task.have_parent():
                subtask = {}
                for k2 in task.get_successors():
                    subtask[k2] = self.task_dict[k2]
                task_tree[k] = [task, subtask]
        return task_tree

    def construct_from_log(self):
        self.task_dict = self.logger.read_log()
        # sth = self.logger.read_time_stat()
        # print(sth)
        if not self.task_dict: self.task_dict = {}

        # re-allocate task id
        for k in self.task_dict:
            self._idset.add(k)

    def time_manager(self, start=True):
        # what if finish stopped task, and then finish a regular task??
        # what if a task in running and finish another task? It'll change the last update
        # It gets stuck, after change a day?
        dt = datetime.now()
        if not self.last_update:
            duration = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
            self.task_stat.append(("rest", duration.total_seconds()))
            self.last_update = ("work", dt, start)
        else:
            activity, time, state = self.last_update
            duration = dt - time
            curr_activity = "rest" if not state and duration.total_seconds() > 300 else "work"
            self.last_update = ("work", dt, start)
            if len(self.task_stat) > 0:
                last_activity, last_duration = self.task_stat[-1]
                if last_activity == curr_activity:
                    self.task_stat[-1] = (curr_activity, last_duration + duration.total_seconds())
                else:
                    self.task_stat.append((curr_activity, duration.total_seconds()))
        # print(self.last_update, self.task_stat)

    def terminate(self):
        if self.active_task:
            self.active_task.stop()
        self.logger.save_log(self.task_dict)
        self.logger.write_history(self.finished_list)
        self.logger.save_time_stat(self.task_stat)

    def _assign_id(self):
        while str(self._serial_num) in self._idset:
            self._serial_num += 1
            self._serial_num %= 1024

        self._idset.add(str(self._serial_num))
        return str(self._serial_num)

    def _collect_id(self, id):
        self._idset.remove(id)


class TimeManager:
    def __init__(self):
        pass

