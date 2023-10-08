from machine import Timer
from time import sleep
from lib.car import Car


tim1 = Timer(1)
bil = Car()


# noinspection PyUnusedLocal
def tick(timer):
    print("L enc:", bil.leftMotor.encValue(), "R enc:", bil.rightMotor.encValue(), 3000)
    
try:
    #tim1.init(freq=1, mode=Timer.PERIODIC, callback=tick )

    def foo( du, ff, rr ):
        print("duty:", du/32000, "FF", ff, "RR", rr)
        bil.leftMotor.PWMPin.duty_u16(65535)
        bil.leftMotor.forwardPin.value(1)
        bil.leftMotor.reversePin.value(0)
        sleep(2)
        bil.leftMotor.PWMPin.duty_u16(du*65535)
        bil.leftMotor.forwardPin.value(ff)
        bil.leftMotor.reversePin.value(rr)
        sleep(4)
        
    bil.set_hastighed(100)

    foo(0,0,0)
    foo(0,0,1)
    foo(0,1,0)
    foo(0,1,1)
    foo(1,0,0)
    foo(1,1,1)
    
    bil.coast()
    
    sleep(4)
    
    #while True:
        #pass

finally:
    tim1.deinit()
    bil.deinit()
    print("shut down")
    