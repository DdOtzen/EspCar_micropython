from machine import PWM
from micropython import const
from time import sleep_ms

# constants
FRONTLIGHT = 200
BACKLIGHT = 150
FULLLIGHT = 1023

from carPins import Pins


class Lights :
    blinking = 0
    blinkState = 0
    OFF = const(0)
    ON = const(1)
    RIGHT = const(1)
    LEFT = const(2)
    LOW_BEAM = const(1)
    HIGH_BEAM = const(2)

    class _LightPair :

        def __init__( self, light_1: type(PWM), light_2: type(PWM) ) :
            self.L1 = light_1
            self.L2 = light_2

        def on( self ):
            self.L1.duty(1023)
            self.L2.duty(1023)
        def off( self ):
            self.L1.duty(0)
            self.L2.duty(0)

    def __init__( self ) :
        self.dutys = [0, 0, 0, 0]
        self.saveDutys = [0, 0, 0, 0]
        self.calibration = 1.0
        self.lightFR = PWM( Pins.Light.Front.Right, freq=1000, duty=self.dutys[0] )
        self.lightFL = PWM( Pins.Light.Front.Left, freq=1000, duty=self.dutys[1] )
        self.lightRR = PWM( Pins.Light.Rear.Right, freq=1000, duty=self.dutys[2] )
        self.lightRL = PWM( Pins.Light.Rear.Left, freq=1000, duty=self.dutys[3] )
        self.frontLights = self._LightPair( self.lightFL, self.lightFR )
        self.rearLights  = self._LightPair( self.lightRL, self.lightRR )
        self.leftLights  = self._LightPair( self.lightFL, self.lightRL )
        self.rightLights = self._LightPair( self.lightFR, self.lightRR )

    def deinit( self ) :
        for d in range(1023, 0, -102) :
            self.setDutys( [d, d, d, d] )
            sleep_ms(100)
        self.setDutys( [0, 0, 0, 0] )


    def setDutys( self, dutys ) :
        self.lightFR.duty( dutys[0] )
        self.lightFL.duty( dutys[1] )
        self.lightRR.duty( dutys[2] )
        self.lightRL.duty( dutys[3] )

    def Brake( self, level ) :
        if level == self.ON :
            self.saveDutys = self.dutys.copy()
            self.dutys[2] = FULLLIGHT
            self.dutys[3] = FULLLIGHT
        else :  # self.OFF
            self.dutys = self.saveDutys.copy()
        self.setDutys( self.dutys )

    def setLights( self, level ) :
        if level == Lights.OFF :
            self.dutys[0] = 0
            self.dutys[1] = 0
            self.dutys[2] = 0
            self.dutys[3] = 0
        elif level == Lights.LOW_BEAM :
            self.dutys[0] = FRONTLIGHT
            self.dutys[1] = FRONTLIGHT
            self.dutys[2] = BACKLIGHT
            self.dutys[3] = BACKLIGHT
        else : # Lights.HIGH_BEAM
            self.dutys[0] = FULLLIGHT
            self.dutys[1] = FULLLIGHT
            self.dutys[2] = BACKLIGHT
            self.dutys[3] = BACKLIGHT
        self.setDutys( self.dutys )

    def blinkingTick( self ) :
        if self.blinking == Lights.RIGHT :
            if self.blinkState == 0 :
                self.blinkState = 1
                self.lightFR.duty( FULLLIGHT )
                self.lightRR.duty( FULLLIGHT )
            else :
                self.blinkState = 0
                self.lightFR.duty( 0 )
                self.lightRR.duty( 0 )
        elif self.blinking == Lights.LEFT :
            if self.blinkState == 0 :
                self.blinkState = 1
                self.lightFL.duty( FULLLIGHT )
                self.lightRL.duty( FULLLIGHT )
            else :
                self.blinkState = 0
                self.lightFL.duty( 0 )
                self.lightRL.duty( 0 )
        else :
            self.setDutys( self.dutys )

    def setBlink( self, direction ) :
        self.blinking = direction
        #        if (self.blinking == 0):		# restore old levels
        self.setDutys( self.dutys )
        if self.blinking == Lights.RIGHT :  # blink right
            self.lightFR.duty( FULLLIGHT )
            self.lightRR.duty( FULLLIGHT )
        elif self.blinking == Lights.LEFT :
            self.lightFL.duty( FULLLIGHT )
            self.lightRL.duty( FULLLIGHT )

# demo code tja
# lygter = Lights(18, 19, 15, 4)

# lygter.setLights(1)
# sleep(4)
# lygter.setLights(2)
# sleep(4)
# lygter.setLights(0)
