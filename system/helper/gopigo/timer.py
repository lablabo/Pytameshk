from threading import Timer,Thread,Event
import time
class timer():

    def __init__(self, registry):
        self.config = registry.get("config")
        self.base_dir = self.config.get('base')
        self.cpu_usage_file = self.base_dir + "/result/cpu_usage.txt"
        self.last_worktime = 0
        self.last_idletime = 0
        self.write_to_file = True
        self.counter = 0

    def clearFile(self, filename):
        if filename == "cpu":
            with open(self.cpu_usage_file, 'w'):pass
    
    def changeWriteFileFlag(self, status):
        self.write_to_file = status
        pass

    def setCounter(self, value):
        self.counter = value
        pass

    def showChart(self,name):
        print "drow"
        pass
    
    def getCpu(self):
        f = open("/proc/stat","r")
        line = ""
        while not "cpu" in line: line =f.readline()
        f.close()
        spl = line.split(" ")
        worktime = int(spl[2])+int(spl[3])+int(spl[4])
        idletime = int(spl[5])
        dworktime = (worktime-self.last_worktime)
        didletime = (idletime-self.last_idletime)
        if dworktime == 0:
            rate = 0
        else:
            rate=float(dworktime)/(didletime+dworktime)
        self.last_worktime = worktime
        self.last_idletime = idletime
        if self.write_to_file:
            self.counter += 1
            with open(self.cpu_usage_file, "a") as cpuFile:
                if self.last_worktime == 0:
                    cpuFile.write(str(self.counter) + " 0\n")
                else:
                    cpuFile.write(str(self.counter) + " " + str(int(rate*100))+"\n")
        

    def wait(self, timer_):
        time.sleep(timer_)
        pass
