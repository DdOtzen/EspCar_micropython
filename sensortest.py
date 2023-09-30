#import pycom
import time
from machine import Pin
from machine import I2C
#import VL53L0X
import vl53l0x as VL53L0X

#i2c = I2C(0)
#i2c = I2C(0, I2C.MASTER)
#i2c = I2C(0, pins=('P22','P1'))
#i2c.init(I2C.MASTER, baudrate=9600)

i2c = I2C(0)
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)

print(i2c.scan())

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)

#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)

#tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)


while True:
# Start ranging
    tof.start()
    tof.read()
    print(tof.read())
    tof.stop()
    time.sleep(1)






    #q = tof.set_signal_rate_limit(0.1)
    #
    # time.sleep(0.1)


