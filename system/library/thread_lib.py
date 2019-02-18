# References - http://code.activestate.com/recipes/203871-a--programming-thread-pool/

import threading
from time import sleep

class controller:

    def __init__(self, register):
        pass


class ThreadPool:

    def __init__(self, numThreads):
        self.__threads = []
        self.__resizeLock = threading.Condition(threading.Lock())
        self.__taskLock = threading.Condition(threading.Lock())
        self.__tasks = []
        self.__isJoining = False
        self.setThreadCount(numThreads)

    def setThreadCount(self, newNumThreads):
        if self.__isJoining:
            return False
        self.__resizeLock.acquire()
        try:
            self.__setThreadCountNolock(newNumThreads)
        finally:
            self.__resizeLock.release()
        return True

    def __setThreadCountNolock(self, newNumThreads):
        while newNumThreads > len(self.__threads):
            newThread = ThreadPoolThread(self)
            self.__threads.append(newThread)
            newThread.start()
        while newNumThreads < len(self.__threads):
            self.__threads[0].goAway()
            del self.__threads[0]

    def getThreadCount(self):
        self.__resizeLock.acquire()
        try:
            return len(self.__threads)
        finally:
            self.__resizeLock.release()

    def queueTask(self, task, args=None, taskCallback=None):
        if self.__isJoining == True:
            return False
        if not callable(task):
            return False

        self.__taskLock.acquire()
        try:
            self.__tasks.append((task, args, taskCallback))
            return True
        finally:
            self.__taskLock.release()

    def getNextTask(self):
        self.__taskLock.acquire()
        try:
            if self.__tasks == []:
                return (None, None, None)
            else:
                return self.__tasks.pop(0)
        finally:
            self.__taskLock.release()

    def joinAll(self, waitForTasks=True, waitForThreads=True):
        self.__isJoining = True

        if waitForTasks:
            while self.__tasks != []:
                sleep(.1)

        self.__resizeLock.acquire()
        try:
            self.__setThreadCountNolock(0)
            self.__isJoining = True

            if waitForThreads:
                for t in self.__threads:
                    t.join()
                    del t

            self.__isJoining = False
        finally:
            self.__resizeLock.release()


class ThreadPoolThread(threading.Thread):

    threadSleepTime = 0.1

    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.__pool = pool
        self.__isDying = False

    def run(self):
        while self.__isDying == False:
            cmd, args, callback = self.__pool.getNextTask()
            # If there's nothing to do, just sleep a bit
            if cmd is None:
                sleep(ThreadPoolThread.threadSleepTime)
            elif callback is None:
                cmd(args)
            else:
                callback(cmd(args))

    def goAway(self):
        self.__isDying = True