from machine import Pin
from time import sleep_ms, sleep
from lib.car import Car

bil = Car()
led = Pin(2, Pin.OUT)

SPEED = 30
PAUSE_MS = 1_000

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
    sleep_ms( PAUSE_MS )
    
    print('bak')
    bil.bak()
    sleep_ms(PAUSE_MS)

    print('drejH')
    bil.drejH()
    sleep_ms(PAUSE_MS)

    print('drejV')
    bil.drejV()
    sleep_ms(PAUSE_MS)

    print('roterH')
    bil.roterH()
    sleep_ms(PAUSE_MS * 2)

    print('roterV')
    bil.roterV()
    sleep_ms(PAUSE_MS * 2)
    
    print('Stop')
    bil.stop()
