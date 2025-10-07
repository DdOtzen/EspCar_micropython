from machine import Pin, Encoder
from time import sleep, sleep_ms
from lib.car import Car



bil = Car()

a1=Pin( bil._pins.Motor.Right.enc_2, Pin.IN )
a2=Pin( bil._pins.Motor.Right.enc_1, Pin.IN )

enc = Encoder( 0, a1, a2 )


bil._rightMotor.SetPower(100)
print( enc.value() )

bil._rightMotor.forward()
while(enc.value() < 2000 ):
    pass
bil._rightMotor.Stop()
sleep_ms(100)
#print( enc.value() )

bil._rightMotor.reverse()
while(enc.value() > 0 ):
    pass
bil._rightMotor.Stop()
print( enc.value() )
for x in range(20):
    sleep_ms(10)
    print( enc.value() )

bil._rightMotor.SetPower(5)
for x in range(2000):
    val = enc.value()
    if x%10 == 0:
        print("  ",val)
    if val > 0:
        bil._rightMotor.reverse()
        sleep_ms(10)
        bil._rightMotor.Stop()
    elif val < 0:
        bil._rightMotor.forward()
        sleep_ms(10)
        bil._rightMotor.Stop()
    else:
        print("  ",val)
        break
print( enc.value() )


def find_min_pow():
    bil._rightMotor.forward()
    for pow in range( 0, 15):
        bil._rightMotor.SetPower( pow )
        sleep_ms(100)
        if enc.value() > 1:
            break

        print("P:",pow)
    
