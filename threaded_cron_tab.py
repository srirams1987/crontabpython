from queue import Queue
import time 
from threading  import Thread
from datetime import datetime,timedelta
import os
from enum import Enum

taskQueue = Queue()


class task:
    def __init__(self, cmd_str):
        self._cmd_str = cmd_str
    
    def get_cmd_str(self):
        return self._cmd_str

    def eval(self, name, id):
        print((datetime.now(), name, id))
        os.system(self._cmd_str)

class FREQUENCY(Enum) :
    Daily = 0
    Monthly = 1
    Yearly = 2 
    Hourly = 3
    Minute = 4
    Minute10 = 5
    Seconds10 = 6

class crontask(Thread):
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
    for r in range(0, 10):
        t = ThreadedProcessor(taskQueue, "name_"+str(r))
        t.daemon = True
        t.start()

def add_task_to_run_queue(ctask, id):
    global taskQueue
    taskQueue.put((ctask, id))



if __name__ == "__main__":

    create_threads(taskQueue)

    func1 = task("echo 'executed function1'")
    func2 = task("echo 'executed function2'")
    func3 = task("echo 'executed function3'")
    func4 = task("echo 'executed function4'")


    print(datetime.now())
    ctask1 = crontask(FREQUENCY.Seconds10, func1, 1)
    ctask1.start()
    ctask2 = crontask(FREQUENCY.Seconds10, func2, 2)
    ctask2.start()
    ctask3 = crontask(FREQUENCY.Seconds10, func3, 3)
    ctask3.start()
    ctask4 = crontask(FREQUENCY.Seconds10, func4, 4)
    ctask4.start()

    d ={}
    d['1'] = ctask1
    d['2'] = ctask2
    d['3'] = ctask3
    d['4'] = ctask4
    start = datetime.now()
    while datetime.now() < start+timedelta(seconds=25):
        pass
    d['3'].set_interupt_flag()




