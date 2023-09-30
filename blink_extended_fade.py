from machine import Pin
from time import sleep_us

led = Pin( 2, Pin.OUT )
duty = 0
step = 100
while True :
#    print( "on: {}, off {}".format( duty, 10000 - duty ) )        
    for _ in range( 2 ) :
        led.on()
        sleep_us( duty )
        led.off()
        sleep_us( 10000 - duty)
    
    duty += step
    if duty == 10000 or duty == 0:
        step = step * -1
        
    