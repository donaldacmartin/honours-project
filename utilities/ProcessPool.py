#!/usr/bin/env python

# Level 4 Project
# Map of the Internet
# Donald Martin (1101795)

from multiprocessing import Process, Lock

class ProcessPool(object):
    def __init__(self, max_threads):
        self.finished_locks    = [Lock() for _ in range(max_threads)]
        self.processes         = []
        
        self.backlog_functions = []
        self.backlog_arguments = []

    def __start_new_process(self, proc_num):
        func = self.backlog_functions.pop(0)
        args = self.backlog_arguments.pop(0)
        
        lock = self.finished_locks[proc_num]
        
        self.processes[proc_num] = Process(func, args)
        self.processes[proc_num].start()
        
    def __terminate_process(self, proc_num):
        self.processes[proc_num].terminate()
        self.processes[proc_num] = None

    def __sentinel(self):
        for i in range(len(self.finished_locks)):
            lock = self.finished_locks[i]
            
            if lock.acquire(False):
                self.__terminate_process(i)
                lock.release()
                self.__start_new_process()