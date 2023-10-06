from machine import Pin
from time import sleep_ms, sleep
from lib.car import Car

bil = Car()

led = Pin(2, Pin.OUT)

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
bil.frem()
#sleep(8)
bil.coast()