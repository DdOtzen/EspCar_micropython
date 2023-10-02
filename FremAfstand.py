from machine import Pin, I2C
from time import sleep_ms, sleep
from lib.car import Car
import vl53l0x as VL53L0X

led = Pin(2, Pin.OUT)
bil = Car()
i2c = I2C(0)
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)

afstand = VL53L0X.VL53L0X(i2c)

led.on()
#while True:
for _ in [8]:
    sleep(1)

    #blinke
    for _ in range(7):
        led.on()
        sleep_ms(300)
        led.off()
        sleep_ms(300)


    bil.set_hastighed(50)

    print('frem')
#    while afstand < 500:
#        bil.frem()
#    sleep_ms(5000)
    
    bil.coast()
