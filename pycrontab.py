from queue import Queue
import time 
from threading  import Thread
from datetime import datetime,timedelta
import os
from enum import Enum

taskQueue = Queue()


class task:
    """
    Class that encapsulate the command string. The command string will be executed in the terminal or the command prompt
    TODO: add specific eval for specific eval-enviroment. MATLAB, terminal, python, etc

    """
    def __init__(self, cmd_str):
        self._cmd_str = cmd_str
    
    def get_cmd_str(self):
        return self._cmd_str

    def eval(self, name, id):
        print((datetime.now(), name, id))
        os.system(self._cmd_str)

class FREQUENCY(Enum) :
    """
    Enum for various frequency that the cron task is required to run 
    TODO: Make this more dynamic 
    """
    Daily = 0
    Monthly = 1
    Yearly = 2 
    Hourly = 3
    Minute = 4
    Minute10 = 5
    Seconds10 = 6

class crontask(Thread):
    """
    A thread class that will encapsulates the id, task and frequency for the cron task. 
    This class will wait will the task is ready to be executed and add the task to the task-execution-queue
    Also has the feature to interrupt the thread and stop execution.
    TODO: Make use of threadpool and employ life cycle management of the thread. What happens after thread is inturrupted ?
    """
    def __init__(self, frequency, task, id):
        Thread.__init__(self)
        self.__freq = frequency
        self.__task = task
        self.__id = id
        self.end_time = self._get_end_time()
        self._interupted = False
    
    def run(self):
        while True:
            while datetime.now() <= self.end_time:
                time.sleep(.1)
                if self._interupted:
                    break
            if self._interupted:
                break
            self.end_time = self._get_end_time()
            
            add_task_to_run_queue(self.__task, self.__id)
        
        if(self._interupted):
            print("{0} task interupped".format(self.__id))

    
    def set_interupt_flag(self):
        self._interupted = True
    
    
    def is_interuppted(self):
        return self._interupted


    def _get_end_time(self):
        if self.__freq == FREQUENCY.Daily:
            end_time = datetime.now() + timedelta(days=1)
        elif self.__freq ==  FREQUENCY.Monthly:
            end_time = datetime.now() + timedelta(days=30)
        elif self.__freq ==  FREQUENCY.Minute:
            end_time = datetime.now()+timedelta(minutes=10)
        else :
            end_time = datetime.now()+timedelta(seconds=10)

        return end_time


    
class ThreadedProcessor(Thread) :
    """
    The threaded worker that waits on the execution queue and execuets that cron task
    """
    def __init__(self, taskQueue, name ):
        Thread.__init__(self)
        self.task_queue = taskQueue
        self._name = name
    def run(self):
        while True:
            try: 
                task,id = self.task_queue.get()
                task.eval(self._name, id)
                time.sleep(10)
            finally:
                self.task_queue.task_done()

def create_threads(taskQueue):
    """
    Create all the threads that will wait on the execution task-queue
    TODO: Right now the number of threads are set to 10. Update to use threadpool and dynamically increase the number of threads based on the demand.
    """
    for r in range(0, 10):
        t = ThreadedProcessor(taskQueue, "name_"+str(r))
        t.daemon = True
        t.start()

def add_task_to_run_queue(ctask, id):
    """
    Add the task to the executed to the queue
    """
    global taskQueue
    taskQueue.put((ctask, id))





