from machine import Pin, PWM, I2C, Timer
from mpu6500 import MPU6500, SF_G, SF_DEG_S
try:
    from time import sleep_ms, time_ns
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
        self.forwardPin.on()
        self.reversePin.on()
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

        self.i2c = I2C(0, sda=Pin(Pins.I2C.SDA), scl=Pin(Pins.I2C.SCL))
        self.imu = MPU6500(self.i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
        self.imu.calibrate()  # Only some kind of offset adjustment
        self.heading = 0;
        self.angularVelocity = 0

        # ligeud controller stuff really ugly names
        self.state = 0
        self.leftDuty = 0
        self.rightDuty = 0
        

        self.timerPeriod = 10  # milliseconds
        self.tim1 = Timer(1)
        self.tim1.init(period=self.timerPeriod, mode=Timer.PERIODIC, callback=self._tick )
        


    def coast( self ):
        self.leftMotor.Stop()
        self.rightMotor.Stop()
        self.state = 0

    def frem( self ):
        self.leftMotor.forward()
        self.rightMotor.forward()
        # initialize I-part of controller
        self.leftDuty = self.leftMotor.duty
        self.rightDuty = self.rightMotor.duty

        self.state = 1
#         ref = 0
#         startTime = time_ns()
#         actDuty = self.leftMotor.duty
#         leftDuty = actDuty
#         rightDuty = actDuty
#         while (time_ns() - startTime) < 8_000_000_000:
#             sleep_ms(10)
# #            print("Time: ", time() - startTime, "AV: ", self.angularVelocity, "actDuty: ", actDuty)
#             leftDuty = leftDuty + (ref-self.angularVelocity) * -50
#             if leftDuty < 0:
#                 forRight = 0 - leftDuty
#                 leftDuty = 0
#             elif leftDuty > 65535:
#                 forRight = leftDuty - 65535
#                 leftDuty = 65535
#             else:
#                 forRight = 0
#                     
#             rightDuty = rightDuty + (ref-self.angularVelocity) * 50
#             if rightDuty < 0:
#                 forLeft = 0 - rightDuty
#                 rightDuty = 0
#             elif rightDuty > 65535:
#                 forLeft = rightDuty - 65535
#                 rightDuty = 65535
#             else:
#                 forLeft = 0
# 
#             leftDuty = leftDuty+forLeft
#             rightDuty = rightDuty+forRight
# 
#             leftDuty = max(min(65535, leftDuty), 0)
#             rightDuty = max(min(65535, rightDuty), 0)
# 
#             self.leftMotor.PWMPin.duty_u16( int(leftDuty) )
#             self.rightMotor.PWMPin.duty_u16( int(rightDuty) )
#             sleep_ms(40)

    def bak( self ):
        self.leftMotor.reverse()
        self.rightMotor.reverse()
        self.state = 2

    def _WaitForTargetHeading( self, angle ):
        if angle != None:
            self.heading = 0
            actualHeading = self.heading
            done = False
            while done == False:
                if angle > 0 and actualHeading > angle:
                    done = True
                if angle < 0 and actualHeading < angle:
                    done = True
                actualHeading = self.heading
            self.coast()

    def drejH( self, angle=None ):
        self.leftMotor.forward()
        self.rightMotor.Stop()
        self._WaitForTargetHeading( angle )

    def drejV( self, angle=None ):
        self.leftMotor.Stop()
        self.rightMotor.forward()
        self._WaitForTargetHeading( -angle )

    def roterH( self, angle=None ):
        self.leftMotor.forward()
        self.rightMotor.reverse()
        self._WaitForTargetHeading( angle )

    def roterV( self, angle=None ):
        self.leftMotor.reverse()
        self.rightMotor.forward()
        self._WaitForTargetHeading( -angle )

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

    def _tick( self, timer ):
        gyro = self.imu.gyro
        self.angularVelocity = gyro[2]
        
        ref = 0
        ki = 500000/(self.timerPeriod * 1000)
        if self.state == 2:
            ki = -ki
        if self.state == 1 or self.state == 2:
            self.leftDuty = self.leftDuty + (ref-self.angularVelocity) * -ki
            self.rightDuty = self.rightDuty + (ref-self.angularVelocity) * ki
            self.leftDuty = max(min(65535, self.leftDuty), 0)
            self.rightDuty = max(min(65535, self.rightDuty), 0)
            self.leftMotor.PWMPin.duty_u16( int(self.leftDuty) )
            self.rightMotor.PWMPin.duty_u16( int(self.rightDuty) )

        self.heading -= gyro[2] * self.timerPeriod / 1000
        

if __name__ == '__main__':
    bil = Car()
