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
        bil.light.Front.Left.on()
        sleep_ms(300)
        bil.light.Front.Right.off()
        bil.light.Front.Left.off()

    bil.set_hastighed(30)

#     bil.frem()
#     sleep_ms(2000)
#     bil.coast()

#     sleep_ms(5000)
#     bil.coast()
#     bil.bak()
#     sleep_ms(5000)
#     bil.coast()

#     for _ in range(24):
#         print('roterH')
#         bil.roterH(180)
#     for _ in range(24):
#         print('roterV')
#         bil.roterV(180)


    for _ in range(5):
        print('drejH')
        bil.drejH(90)

        print('drejV')
        bil.drejV(90)

    for _ in range(5):
        print('roterH')
        bil.roterH(180)

        print('roterV')
        bil.roterV(180)

    print('roterH')
    bil.roterH(180)

    for _ in range(5):
        print('drejH')
        bil.drejH(90)

        print('drejV')
        bil.drejV(90)

    
    print('coast')
    bil.coast()

