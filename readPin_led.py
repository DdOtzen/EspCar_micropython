from machine import Pin

button = Pin( 0, Pin.IN )
led = Pin( 2, Pin.OUT )

while True :
    if button.value() == 0 :
        led.on()
    else:
        led.off()
        