from machine import Pin, PWM
try:
    from time import sleep_ms
except ImportError:
    from time import sleep
    def sleep_ms( ms ):
        sleep( ms / 1000 )

from lib.carPins import Pins

class Motor:
    def __init__( self, pins :Pins.Motor.LR ):
        self.duty = 0
        self.calibration = 1.0
        self.PWMPin = PWM( Pin( pins.Speed ), freq=1000, duty_u16=0 )
        self.forwardPin = Pin( pins.Forward, Pin.OUT )
        self.reversePin = Pin( pins.Reverse, Pin.OUT )
        self.currentState = self.Stop
        self.SetSpeed(0)

    def SetSpeed( self, speed ):
        self.duty = speed
        self.currentState()

    def SetCalibration( self, factor ):
        self.calibration = factor

    def forward( self ):
        self.forwardPin.on()
        self.reversePin.off()
        self.PWMPin.duty_u16( self.duty )
        self.currentState = self.forward

    def reverse( self ):
        self.forwardPin.off()
        self.reversePin.on()
        self.PWMPin.duty_u16( self.duty )
        self.currentState = self.reverse

    def Stop( self ):
        self.forwardPin.off()
        self.reversePin.off()
        # self.PWMPin.duty( 0 )
        self.currentState = self.Stop

class Lights:
    class _Light:
        def __init__( self, pins: Pins.Light.FR ):
            self.Left  = Pin( pins.Left, Pin.OUT )
            self.Right = Pin( pins.Right, Pin.OUT )

        def on( self ):
            self.Left.on()
            self.Right.on()

        def off( self ):
            self.Left.off()
            self.Right.off()

    def __init__( self ):

        self.Front = self._Light( Pins.Light.Front )
        self.Rear  = self._Light( Pins.Light.Rear )


class Encoder :

    def __init__( self, pins: Pins.Motor.LR ) :
        self.encA = Pin( pins.Forward, Pin.IN )
        self.reversePin = Pin( pins.Reverse, Pin.IN )
        self.currentState = self.Stop
        self.SetSpeed( 0 )


class Car:

    def __init__( self ):
        self.light = Lights()
        self.leftMotor  = Motor( Pins.Motor.Left )
        self.rightMotor = Motor( Pins.Motor.Right )
        self.pins = Pins
        self.speed = 0


    def coast( self ):
        self.leftMotor.Stop()
        self.rightMotor.Stop()

    def frem( self ):
        self.leftMotor.forward()
        self.rightMotor.forward()

    def bak( self ):
        self.leftMotor.reverse()
        self.rightMotor.reverse()

    def drejH( self ):
        self.leftMotor.forward()
        self.rightMotor.Stop()

    def drejV( self ):
        self.leftMotor.Stop()
        self.rightMotor.forward()

    def roterH( self ):
        self.leftMotor.forward()
        self.rightMotor.reverse()

    def roterV( self ):
        self.leftMotor.reverse()
        self.rightMotor.forward()

    def set_hastighed( self, speed ):
        if speed == 100 :
            self.speed = 65535
        else:
            self.speed = speed * 655
        self.leftMotor.SetSpeed( self.speed )
        self.rightMotor.SetSpeed( self.speed )

    def frem_dist( self, distance ):
        self.leftMotor.forward()
        self.rightMotor.forward()
        print( int( distance / self.speed ) * 100 )
        sleep_ms( int( distance / self.speed ) * 100 )
        self.coast()

if __name__ == '__main__':
    bil = Car()
