from gopigo import *

class servoMotor:
    def __init__(self, registry):
        self.config = registry.get("config")
        self.centerPos = 90
        self.NextPos = 10
        self.servo_pos = self.centerPos
        self.distance = 0
        pass
    def read(self):
        while True:
            self.distance = us_dist(15)
    def getDistance(self):
        return self.distance
    
    def valid(self):
        if self.servo_pos>180:
            self.servo_pos=180
	if self.servo_pos<0:
	    self.servo_pos=0
	pass
    
    def right(self):
        self.servo_pos = self.servo_pos + self.NextPos
        self.valid()
        servo(self.servo_pos)
        pass
    
    def left(self):
        self.servo_pos = self.servo_pos - self.NextPos
        self.valid()
        servo(self.servo_pos)
        pass
    
    def center(self):
        self.servo_pos = self.centerPos
        servo(self.servo_pos)
        pass

	
