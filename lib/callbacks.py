from machine import Timer
from machine import Pin

led = Pin(2, Pin.OUT) # enable onboard led as output to drive the LED
status = 0

taskList = []

def tick(timer):
    results = [f() for f in taskList]
    

def addCb(rutine):
    taskList.append(rutine)


def cb1():
    global status
    global led
    if status == 1 :
        led.off()
        status = 0
    else:
        led.on()
        status = 1
 
tim1 = Timer(1)
tim1.init(period=500, mode=Timer.PERIODIC, callback=tick )
addCb(cb1)