from machine import Timer
from time import sleep
from lib.car import Car


tim1 = Timer(1)
bil = Car()
speed = 0


# noinspection PyUnusedLocal
def tick(timer):
    print("L enc:", bil.leftMotor.encValue(), "R enc:", bil.rightMotor.encValue(), "power_pct ‰:", speed*10, 3000)
    
try:
    tim1.init(freq=1, mode=Timer.PERIODIC, callback=tick )

    def fb(bil):
        #print('frem')
        bil.frem()
        sleep(2)
        
        #print('bak')
        bil.bak()
        sleep(2)

    for s in range(0, 101, 50):
        speed = s
        bil.set_hastighed(s)
        fb(bil)

    speed = 0
    #bil.set_hastighed(0)
    #bil.frem()
    #sleep(2)
    bil.coast()
    
    sleep(4)
    
    #while True:
        #pass

finally:
    tim1.deinit()
    bil.deinit()
    print("shut down")
    