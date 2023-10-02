from machine import Pin
from time import sleep_ms, sleep
from lib.car import Car

led = Pin(2, Pin.OUT)
bil = Car()


#Vent lidt med at starte, så vi kan nå st stille bilen ;-)
sleep(5)

#Blinke lidt før vi kører
for _ in range(7):
    led.on()
    sleep_ms(300)
    led.off()
    sleep_ms(300)


#Køre bil
bil.set_fart(100)

bil.frem()
sleep_ms(500)
bil.coast()
