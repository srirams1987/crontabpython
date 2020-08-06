
from pycrontab import *


if __name__ == "__main__":

    #Start the threaded task workers 
    create_threads(taskQueue)

    #create tasks that are to be executed as cron 
    func1 = task("echo 'executed function1'")
    func2 = task("echo 'executed function2'")
    func3 = task("echo 'executed function3'")
    func4 = task("echo 'executed function4'")


    print(datetime.now())
    #create crontasks with the frequency 
    ctask1 = crontask(FREQUENCY.Seconds10, func1, 1)
    ctask1.start()
    ctask2 = crontask(FREQUENCY.Seconds10, func2, 2)
    ctask2.start()
    ctask3 = crontask(FREQUENCY.Seconds10, func3, 3)
    ctask3.start()
    ctask4 = crontask(FREQUENCY.Seconds10, func4, 4)
    ctask4.start()

    # Add all the tasks that are created to a dictioanry that could access the crontask objects for maintanence 
    # and interupting(stop executingz) the task
    d ={}
    d['1'] = ctask1
    d['2'] = ctask2
    d['3'] = ctask3
    d['4'] = ctask4
    
    # Example on how to interurrupt(end cron task)
    start = datetime.now()
    # Wait for 25 seconds and interupt the task 3
    while datetime.now() < start+timedelta(seconds=25):
        pass
    d['3'].set_interupt_flag()

