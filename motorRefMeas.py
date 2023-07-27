from machine import Pin
try:
    from time import sleep_ms
except ImportError:
    from time import sleep
    def sleep_ms( ms ):
        sleep( ms / 1000 )

from lib.car import Car
from lib.carPins import Pins

from machine import time_pulse_us

bil = Car()
led = Pin(2, Pin.OUT)

cmd1 = Pin( Pins.Spi.SCL, Pin.IN )
cmd2 = Pin( Pins.Spi.SDA, Pin.IN )

def updateBil( frem:bool, hastighed:int ):
    global bil
    if frem:
        print('frem ', end='')
        bil.frem()
    else :
        print('bak ', end='')
        bil.bak()

    bil.set_hastighed( hastighed )
    print(f'{hastighed}%')

frem = True
oldFrem = False
hastighed = 100
oldHastighed = 50
a1=Pin( 35, Pin.IN )

while True:

    if (frem != oldFrem ) or (hastighed != oldHastighed ):
        updateBil( frem, hastighed )
        oldFrem = frem
        oldHastighed = hastighed

    frem = True if cmd1() else False
    hastighed = 100 if cmd2() else 50
    sleep_ms(500)
    time_pulse_us( a1, 1, 1000000 )
    pp = time_pulse_us( a1, 1, 1000000 )
    fr = 1/pp * 1000
    print(f'{pp} uS')
    #print(f'{fr} Khz')
    #print(f'{fr*1000/208} rps')
    
