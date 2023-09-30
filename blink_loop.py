from machine import Pin
from time import sleep_ms

led = Pin( 2, Pin.OUT )

while True :
    led.off()
    sleep_ms(500)
    led.on()
    sleep_ms(500)
    