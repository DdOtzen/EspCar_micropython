from machine import Pin, PWM
import math
import time

led_pin = Pin( 2 )
led = PWM( led_pin )
led.freq(1000)
wait = 100
while True :
    for i in range(20):
        duty = int( i / 20 * 1023 )
        print( duty )
        led.duty( duty )
        time.sleep_ms( wait )
    for i in range(20, 0, -1):
        duty = int( i / 20 * 1023 )
        print( duty )
        led.duty( duty )
        time.sleep_ms( wait )
