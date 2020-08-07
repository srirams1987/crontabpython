
from pycrontab import *


if __name__ == "__main__":

    #Start the threaded task workers 
    create_threads(taskQueue)

    #create tasks that are to be executed as cron 
    func1 = Task_Factory.create_task(Runner_Type.MATLAB, "echo 'executed function1'")
    func2 = Task_Factory.create_task(Runner_Type.MATLAB, "echo 'executed function2'")
    func3 = Task_Factory.create_task(Runner_Type.PYTHON_SCRIPT, "echo 'executed function3'")
    func4 = Task_Factory.create_task(Runner_Type.TERMINAL, "echo 'executed function4'")


    print(datetime.now())
    #create crontasks with the frequency 
    ctask1 = Cron_Task(FREQUENCY.Seconds10, func1, 1)
    ctask1.start()
    ctask2 = Cron_Task(FREQUENCY.Seconds10, func2, 2)
    ctask2.start()
    ctask3 = Cron_Task(FREQUENCY.Seconds10, func3, 3)
    ctask3.start()
    ctask4 = Cron_Task(FREQUENCY.Seconds10, func4, 4)
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

