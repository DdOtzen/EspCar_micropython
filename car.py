from machine import Pin, PWM

class Motor():
    def __init__( self, pinForward, pinReverse ):
        self.duty = 0
        self.forwardPin = PWM( Pin( pinForward ), freq=1000, duty=0 )
        self.reversePin = PWM( Pin( pinReverse ), freq=1000, duty=0 )
        self.currentState = self.stop
        
    def setSpeed( self, speed ):
        self.duty = speed * 10
        self.currentState()
    
    def forward( self ):
        self.reversePin.duty( 0 )
        self.forwardPin.duty( self.duty )
        self.currentState = self.forward

    def reverse( self ):
        self.forwardPin.duty( 0 )
        self.reversePin.duty( self.duty )
        self.currentState = self.reverse

    def stop( self ):
        self.reversePin.duty( 0 )
        self.forwardPin.duty( 0 )
        self.currentState = self.stop


class Car():
    
    def __init__(self, leftFowardPin=15, leftReversePin=4, rightFowardPin=18, rightReversePin=5 ):
        self.leftMotor = Motor( leftFowardPin, leftReversePin )
        self.rightMotor = Motor( rightFowardPin, rightReversePin )


    def coast( self ):
        self.leftMotor.stop()
        self.rightMotor.stop()
    
    def frem( self ):
        self.leftMotor.forward()
        self.rightMotor.forward()

    def bak( self ):
        self.leftMotor.reverse()
        self.rightMotor.reverse()

    def drejH( self ):
        self.leftMotor.forward()
        self.rightMotor.stop()

    def drejV( self ):
        self.leftMotor.stop()
        self.rightMotor.forward()

    def roterH( self ):
        self.leftMotor.forward()
        self.rightMotor.reverse()

    def roterV( self ):
        self.leftMotor.reverse()
        self.rightMotor.forward()

    def setSpeed( self, speed ):
        self.leftMotor.setSpeed( speed )
        self.rightMotor.setSpeed( speed )
        