from machine import Timer
from machine import Pin


class Schedule:
    def __init__(self):
        self.led = Pin(2, Pin.OUT) # enable onboard led as output to drive the LED
        self.status = 0
        self.count = 0
        self.taskList10 = []		# 10 msec tasks
        self.taskList100 = []		# 100 msec tasks
        self.taskList500 = []		#500 ms tasks
        
        self.tim1 = Timer(1)
        self.tim1.init(period=10, mode=Timer.PERIODIC, callback=self.tick )
        
        self.addCb500(self.cb1)
    def deinit( self ):
        self.tim1.deinit()
        self.led.off()

    def addCb10(self, rutine):
        if rutine not in self.taskList10 :
            self.taskList10.append(rutine)

    def addCb100(self, rutine):
        self.taskList100.append(rutine)

    def addCb500(self, rutine):
        if rutine not in self.taskList500 :
            self.taskList500.append(rutine)

    def cb1(self):
        if self.status == 1 :
            self.led.off()
            self.status = 0
        else:
            self.led.on()
            self.status = 1
    
    
    def tick(self, timer):
        self.results = [f() for f in self.taskList10]
        self.count += 1
        if self.count % 10 == 0:
            self.results = [f() for f in self.taskList100]
        if self.count == 50:
            self.count = 0
            self.results = [f() for f in self.taskList500]
            
    



