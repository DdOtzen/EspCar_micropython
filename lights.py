from machine import Pin, PWM
from time import sleep_ms, sleep

class Lights():
    def __init__( self, pinFR, pinFL, pinRR, pinRL ):
        self.blinkRight = 0
        self.blinkLeft = 0
        self.calibration = 1.0
        self.lightFR = PWM( Pin( pinFR ), freq=1000, duty=0 )
        self.lightFL = PWM( Pin( pinFL ), freq=1000, duty=0 )
        self.lightRR = PWM( Pin( pinRR ), freq=1000, duty=0 )
        self.lightRL = PWM( Pin( pinRL ), freq=1000, duty=0 )
        
    def LightsOn( self ):
        self.duty = 400
        self.lightFR.duty(self.duty)
        self.lightFL.duty(self.duty)
        self.lightRR.duty(self.duty)
        self.lightRL.duty(self.duty)
        self.lightsOn = 1
    
    def LightsOff( self ):
        self.duty = 0
        self.lightFR.duty(self.duty)
        self.lightFL.duty(self.duty)
        self.lightRR.duty(self.duty)
        self.lightRL.duty(self.duty)
        self.lightsOn = 0


lygter = Lights(18, 19, 15, 4)    
lygter.LightsOn()
sleep(10)
lygter.LightsOff()

