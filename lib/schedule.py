from machine import Timer
from machine import Pin

led = Pin(2, Pin.OUT) # enable onboard led as output to drive the LED
status = 0

taskList = []

class Scheduler:
    def __init__(self) -> None:
        tim1 = Timer(1)
        tim1.init(period=500, mode=Timer.PERIODIC, callback=tick ) 


    def cb1(self):
        global status
        global led
        if (status == 1):
            led.off()
            status = 0
        else:
            led.on()
            status = 1
    
    
def tick(timer):
    results = [f() for f in taskList]
    

def addCb(rutine):
    taskList.append(rutine)


addCb(cb1)