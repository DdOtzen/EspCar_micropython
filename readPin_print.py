from machine import Pin
from time import sleep_ms

button = Pin( 0, Pin.IN )

while True :
    var = button.value()
    print( var == 0)
    sleep_ms( 300 )