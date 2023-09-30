from machine import Pin, ADC, PWM
from time import sleep_ms, sleep
from Car import Car

led = Pin( 2, Pin.OUT )
sensor = ADC( Pin(34 ) )
sensor.atten(ADC.ATTN_11DB)

led.on()
sleep_ms( 300 )
led.off()
sleep_ms( 300 )
led.on()
sleep_ms( 300 )
led.off()

car = Car()
fremad = True
while True :
    dist = sensor.read()
    #print( dist )

    if fremad :
        if dist > 2600 :
            car.setSpeed( 100 )
            car.bak()
            sleep_ms(500)
            car.setSpeed( 40 )
            car.roterH()
            fremad = False
        else :
            speed = int(100-( dist - 690)/40)
            if speed > 100 :
                speed = 100
            print( speed )
            car.setSpeed( speed )
            
    else :
        if dist < 1000  :
            car.frem()
            fremad = True

    sleep_ms(10)
