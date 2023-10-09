from machine import Pin, PWM

# constants
FRONTLIGHT = 200
BACKLIGHT = 150
FULLLIGHT = 1023

from carPins import Pins


class Lights :
    blinking = 0
    blinkState = 0

    class _Light :

        def __init__( self, pins: Pins.Light.FR ) :
            self.Left = 22  # Pin( pins.Left, Pin.OUT )
            self.Right = 23  # Pin( pins.Right, Pin.OUT )

    def __init__( self, pinFR=18, pinFL=19, pinRR=15, pinRL=4 ) :
        self.dutys = [0, 0, 0, 0]
        self.saveDutys = [0, 0, 0, 0]
        self.calibration = 1.0
        self.lightFR = PWM( Pin( pinFR ), freq=1000, duty=self.dutys[0] )
        self.lightFL = PWM( Pin( pinFL ), freq=1000, duty=self.dutys[1] )
        self.lightRR = PWM( Pin( pinRR ), freq=1000, duty=self.dutys[2] )
        self.lightRL = PWM( Pin( pinRL ), freq=1000, duty=self.dutys[3] )
        self.Front = self._Light( Pins.Light.Front )
        self.Rear = self._Light( Pins.Light.Rear )

    def setDutys( self, dutys ) :
        self.lightFR.duty( dutys[0] )
        self.lightFL.duty( dutys[1] )
        self.lightRR.duty( dutys[2] )
        self.lightRL.duty( dutys[3] )

    def Brake( self, level ) :
        if level == 1 :
            self.saveDutys = self.dutys.copy()
            self.dutys[2] = FULLLIGHT
            self.dutys[3] = FULLLIGHT
        else :
            self.dutys = self.saveDutys.copy()
        self.setDutys( self.dutys )

    def setLights( self, level ) :
        if level == 0 :
            self.dutys[0] = 0
            self.dutys[1] = 0
            self.dutys[2] = 0
            self.dutys[3] = 0
        elif level == 1 :
            self.dutys[0] = FRONTLIGHT
            self.dutys[1] = FRONTLIGHT
            self.dutys[2] = BACKLIGHT
            self.dutys[3] = BACKLIGHT
        else :
            self.dutys[0] = FULLLIGHT
            self.dutys[1] = FULLLIGHT
            self.dutys[2] = BACKLIGHT
            self.dutys[3] = BACKLIGHT
        self.setDutys( self.dutys )
        self.lightsOn = 1

    def blinkingTick( self ) :

        if self.blinking == 1 :
            if self.blinkState == 0 :
                self.blinkState = 1
                self.lightFR.duty( FULLLIGHT )
                self.lightRR.duty( FULLLIGHT )
            else :
                self.blinkState = 0
                self.lightFR.duty( 0 )
                self.lightRR.duty( 0 )
        elif self.blinking == 2 :
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

    def setBlink( self, direction ) :  # direction = 0: off, = 1: right, = 2: left
        self.blinking = direction
        #        if (self.blinking == 0):		# restore old levels
        self.setDutys( self.dutys )
        if self.blinking == 1 :  # blink right
            self.lightFR.duty( FULLLIGHT )
            self.lightRR.duty( FULLLIGHT )
        elif self.blinking == 2 :
            self.lightFL.duty( FULLLIGHT )
            self.lightRL.duty( FULLLIGHT )

# demo code tja
# lygter = Lights(18, 19, 15, 4)

# lygter.setLights(1)
# sleep(4)
# lygter.setLights(2)
# sleep(4)
# lygter.setLights(0)
