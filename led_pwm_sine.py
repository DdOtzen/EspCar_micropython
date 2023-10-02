from machine import Pin, PWM
import math
import time

led_pin = Pin( 2 )
led = PWM( led_pin )
led.freq(1000)
wait = 100
while True :
    for i in range(40):
        duty = int( math.sin( i / 20 * math.pi) * 512 + 512 - 0.5 )
        print( duty )
        led.duty( duty )
        time.sleep_ms( wait )
