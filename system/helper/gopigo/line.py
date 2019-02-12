import line_sensor
import time
import subprocess
from timeit import default_timer as timer

class line:
    def __init__(self, registry):
        self.report = registry.get("log")
        self.debug = True
        self.check_line_sensorcheck()
        file_b="/black_line.txt"
        file_w="/home/pi/Desktop/GoPiGo/Software/Python/line_follower/white_line.txt"
        file_r="/range_line.txt"
        pass

    def check_line_sensorcheck(self):
        output = subprocess.check_output(['i2cdetect', '-y','1'])
	if output.find('06') >=0:
	    print "Line Sensor       :  Start"
	else:
	    print "Line Sensor       :  Error"
	    self.report.error("file", "Line Sensor Not Found", "engine/static/line", True)

    def read(self):
        val = line_sensor.read_sensor()
        while val[0] == -1:
            val = line_sensor.read_sensor()
        return val

    def readColor(self):
	threshold=[900, 900, 900, 900, 900]
	line_pos = [0]*5
        raw_vals = self.read()
	for i in range(5):
	    if raw_vals[i]>threshold[i]:
		line_pos[i]=1
            else:
		line_pos[i]=0
	flag = True
	for a in line_pos:
            if not a:
                flag = False
        return flag
    
    def finish(self):
        val = self.scratch()
        end = [1,1,1,1,1]
        if val == end:
            return True
        else:
            return False
        pass  

    def scratch(self):
	threshold=[950, 950, 950, 950, 950]
	line_pos = [0]*5
        raw_vals = self.read()
	for i in range(5):
	    if raw_vals[i]>threshold[i]:
		line_pos[i]=1
            else:
		line_pos[i]=0
	return line_pos
        pass

    def position(self):
        pos = []
        scr = self.scratch()
        scr = self.scratch()
        if scr == [0,1,1,1,0]:
            pos = ["center","normal"]
        elif scr == [0,0,1,1,1] :
            pos = ["right","normal"]
        elif scr == [0,0,0,1,1]:
            pos = ["right","low"]
        elif scr == [0,0,0,0,1]:
            pos = ["right","bad"]
        elif scr == [1,1,1,0,0]:
            pos = ["left","normal"]
        elif scr == [1,1,0,0,0]:
            pos = ["left","low"]
        elif scr == [1,0,0,0,0]:
            pos = ["left","bad"]
        elif scr == [1,1,1,1,1]:
            pos = ["finish","finish"]
        elif scr == [1,1,1,1,0]:
            pos = ["left","high"]
        elif scr == [0,1,1,1,1]:
            pos = ["right","high"]
        elif scr == [1,0,1,0,0]:
            pos = ["left","normal"]
        elif scr == [0,0,1,0,1]:
            pos = ["right","normal"]
        else:
            pos = ["undefind","undefind"] + scr
        return pos

    def readAsString(self):
        pos = []
        scr = self.scratch()
        scr = self.scratch()
        scr = self.scratch()
        scr = self.scratch()
        scr = self.scratch()
        scr = self.scratch()
        scr = self.scratch()
        string = ""
        for i in range(5):
            string = string + str(scr[i])
        return string
