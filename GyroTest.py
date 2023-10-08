from machine import Pin
from time import sleep_ms, sleep
from lib.car import Car

"""
D25 pwmB
D33 B12
D32 B11
stby 3.3V
D26 A11
D27 A12
D14 pwmA
"""
bil = Car()

led = Pin(2, Pin.OUT)

#while True:
for _ in [8]:
    sleep(1)

    #blinke
    for _ in range(3):
        led.on()
        sleep_ms(300)
        led.off()

        bil.light.Front.Right.on()
        sleep_ms(300)
        bil.light.Front.Right.off()

        bil.light.Front.Left.on()
        sleep_ms(300)
        bil.light.Front.Left.off()

        bil.light.Rear.Left.on()
        sleep_ms(300)
        bil.light.Rear.Left.off()

        bil.light.Rear.Right.on()
        sleep_ms(300)
        bil.light.Rear.Right.off()

    bil.set_hastighed(30)

    print('frem')
    bil.frem()
    sleep_ms(5000)
    
    print('bak')
    bil.bak()
    sleep_ms(5000)

    print('drejH')
    bil.drejH()
    sleep_ms(5000)

    print('drejV')
    bil.drejV()
    sleep_ms(5000)

    print('roterH')
    bil.roterH()
    sleep_ms(10000)

    print('roterV')
    bil.roterV()
    sleep_ms(10000)
    
    print('coast')
    bil.coast()
