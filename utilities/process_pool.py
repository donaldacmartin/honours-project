#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from multiprocessing import Process, Lock
from sys import exit

class ProcessPool(object):
    def __init__(self, max_processes):
        self.max_processes = max_processes
        self.control_locks = [Lock() for _ in range(max_processes)]
        self.processes     = [None for _ in range(50)]
        self.jobs          = []
        
    def add_job(self, func, args):
        self.jobs.append((func, args))
        
    def run(self):
        self.proc = Process(target=self.__sentinal)
        self.proc.start()
        
    def join(self):
        self.proc.join()
        
    def __wrapper_func(self, proc_num, lock, job_func, args):
        print("Starting BGP " + str(proc_num))
        lock.acquire()
        job_func(*args)
        lock.release()
        print("Finished BGP " + str(proc_num))
        exit()
        
    def __start_new_process(self, proc_num):
        func, args = self.jobs.pop(0)
        lock       = self.control_locks[proc_num]
        proc_args  = (proc_num, lock, func, args,)
        
        proc = Process(target=self.__wrapper_func, args=proc_args)
        proc.start()
        self.processes[proc_num] = proc
        
    def __sentinal(self):
        while len(self.jobs) > 0:
            for i in range(self.max_processes):
                if self.control_locks[i].acquire(False):
                    self.control_locks[i].release()
                    self.__start_new_process(i)