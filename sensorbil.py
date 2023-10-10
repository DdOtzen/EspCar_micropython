#import pycom
from time import sleep, sleep_ms
from machine import Pin
from machine import I2C
import lib.VL53L0X as VL53L0X
from lib.car import Car

led = Pin(2, Pin.OUT)
bil = Car()

#_i2c = I2C(0)
#_i2c = I2C(0, I2C.MASTER)
#_i2c = I2C(0, _pins=('P22','P1'))
#_i2c.init(I2C.MASTER, baudrate=9600)

#_i2c = I2C(0)
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)

# Create a VL53L0X object
afstand = VL53L0X.VL53L0X(i2c)

#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)

#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)

bil.set_hastighed(100)

afstand.start()
i = 0

while 1:
    print(i)
    i +=1
    while afstand.read() > 500:
        bil.frem()

    print("....STOP.....")
    bil.coast()

#for _ in range(5000):
# Start ranging
#    afstand.start()
#    tof.read()
#    print(afstand.read())
#    afstand.stop()






    #q = tof.set_signal_rate_limit(0.1)
    #
    # time.sleep(0.1)


