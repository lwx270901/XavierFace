# SuperFastPython.com
# example of terminating a process
from time import sleep
from multiprocessing import Process
from testcam import task
 

 
# entry point
if __name__ == '__main__':
    # create a process
    process = Process(target=task)
    # run the process
    process.start()
    # wait for a moment
    sleep(20)
    # terminate the process
    process.terminate()
    # continue on...
    print('Parent is continuing on...')