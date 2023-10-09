from machine import Pin, I2C, Timer
from schedule import Schedule

from lib.carPins import Pins
from lights import Lights
from lib.motor import Motor
from mpu6500 import MPU6500, SF_G, SF_DEG_S


class Car :

    def __init__( self, useRegulator: bool = True ) :
        self.scheduling = Schedule()
        self.light = Lights()
        self.scheduling.addCb500(self.light.blinkingTick)
        self.rightMotor = Motor( Pins.Motor.Right, useRegulator )
        self.leftMotor = Motor( Pins.Motor.Left, useRegulator )
        self.pins = Pins
        self.speed = 0

        self.i2c = I2C( 0, sda=Pin( Pins.I2C.SDA ), scl=Pin( Pins.I2C.SCL ) )
        self.imu = MPU6500( self.i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S )
        self.imu.calibrate()  # Only some kind of offset adjustment
        self.heading = 0;
        self.angularVelocity = 0

        # ligeud controller stuff really ugly names
        self.state = 0
        self.leftDuty = 0
        self.rightDuty = 0
        
        self.scheduling.addCb10(self._tick)

        self.timerPeriod = 10  # milliseconds
#        self.tim1 = Timer(1)
#        self.tim1.init(period=self.timerPeriod, mode=Timer.PERIODIC, callback=self._tick )

    def coast( self ) :
        self.leftMotor.Coast()
        self.rightMotor.Coast()

    def stop( self ) :
        self.leftMotor.Stop()
        self.rightMotor.Stop()
        self.state = 0

    def frem( self ) :
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

    def bak( self ) :
        self.leftMotor.reverse()
        self.rightMotor.reverse()
        self.state = 2

    def _WaitForTargetHeading( self, angle ) :
        if angle is not None :
            self.heading = 0
            actualHeading = self.heading
            done = False
            while not done :
                if 0 < angle < actualHeading :
                    done = True
                if 0 > angle > actualHeading :
                    done = True
                actualHeading = self.heading
            self.coast()

    def drejH( self, angle=None ) :
        self.leftMotor.forward()
        self.rightMotor.Stop()
        self._WaitForTargetHeading( angle )

    def drejV( self, angle=None ) :
        self.leftMotor.Stop()
        self.rightMotor.forward()
        self._WaitForTargetHeading( -angle )

    def roterH( self, angle=None ) :
        self.leftMotor.forward()
        self.rightMotor.reverse()
        self._WaitForTargetHeading( angle )

    def roterV( self, angle=None ) :
        self.leftMotor.reverse()
        self.rightMotor.forward()
        self._WaitForTargetHeading( -angle )

    def set_hastighed( self, speed ) :
        self.speed = speed
        self.leftMotor.SetPower( self.speed )
        self.rightMotor.SetPower( self.speed )

    def deinit( self ) :
        self.coast()
        self.leftMotor.deinit()
        self.rightMotor.deinit()

    def _tick( self ):
        gyro = self.imu.gyro
        self.angularVelocity = gyro[2]

        ref = 0
        ki = 500000 / (self.timerPeriod * 1000)
        if self.state == 2 :
            ki = -ki
        if self.state == 1 or self.state == 2 :
            self.leftDuty = self.leftDuty + (ref - self.angularVelocity) * -ki
            self.rightDuty = self.rightDuty + (ref - self.angularVelocity) * ki
            self.leftDuty = max( min( 65535, self.leftDuty ), 0 )
            self.rightDuty = max( min( 65535, self.rightDuty ), 0 )
            self.leftMotor.PWMPin.duty_u16( int( self.leftDuty ) )
            self.rightMotor.PWMPin.duty_u16( int( self.rightDuty ) )

        self.heading -= gyro[2] * self.timerPeriod / 1000


if __name__ == '__main__' :
    bil = Car()
