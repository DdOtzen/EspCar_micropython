from machine import Pin, I2C
from micropython import const
from time import sleep_ms

from schedule import Schedule

from lib.carPins import Pins
from lights import Lights
from lib.motor import Motor
from mpu6500 import MPU6500, SF_G, SF_DEG_S
from vl53l0x import VL53L0X


class Car :
    _STATE_STOP : int = const( 0 )
    _STATE_FREM : int = const( 1 )
    _STATE_BAK  : int = const( 2 )


    def __init__( self ) :
        self._scheduling = Schedule()

        self._i2c = I2C( 0, sda=Pin( Pins.I2C.SDA ), scl=Pin( Pins.I2C.SCL ) )
        # Pulling up the lights interface to the car instance. Can be done more dynamic, but for now we use the brute force method.
        # And at the same time translate to danish TODO: forget this danish interface crap and  go full english [MAO].
        self.light = Lights()  # Old way of access, kept for compatibility.
        self.lys = lambda : None  # Do nothing, until EnableBlinkRelay() is called.
        self.bremselys = lambda : None  # Do nothing, until EnableBlinkRelay() is called.
        self.blinklys =  lambda : None  # Do nothing, until EnableBlinkRelay() is called.
        self.forlygter = self.light.frontLights
        self.baglygter = self.light.rearLights
        self.venstreLys = self.light.leftLights
        self.hoejreLys = self.light.rightLights
        self.SLUK_LYS = self.light.OFF
        self.TAEND_LYS = self.light.ON
        self.KORT_LYS = self.light.LOW_BEAM
        self.LANGT_LYS = self.light.HIGH_BEAM
        self.VENSTRE_BLINK = self.light.LEFT
        self.HOEJRE_BLINK = self.light.RIGHT

        self._rightMotor = Motor( Pins.Motor.Right )
        self._leftMotor = Motor( Pins.Motor.Left )
        self._pins = Pins
        self._speed = 0

        
        self.tofSensor = VL53L0X(self._i2c)
        self.tofSensor.start()
        self._scheduling.addCb100(self._tofTick)
        self.distance = 0
        
        self._imu = MPU6500( self._i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S )
        self._imu.calibrate()  # Only some kind of offset adjustment
        self._heading = 0
        self._angularVelocity = 0

        # ligeud controller stuff really ugly names
        self._state = Car._STATE_STOP
        self._leftDuty = 0
        self._rightDuty = 0
        
        self._scheduling.addCb10(self._DriveStraightCtrlTick)
        self._timerPeriod = 10  # milliseconds
        self.dbgCount = 0
        # self._scheduling.addCb500( self.Dprint )
    def deinit( self ) :
        self.coast()
        self._leftMotor.deinit()
        self._rightMotor.deinit()
        self._scheduling.deinit()
        self.light.deinit()
    # Alias method of deinit.
    sluk = deinit

    def EnableBlinkRelay( self ):
        self._scheduling.addCb500( self.light.blinkingTick )
        self.blinklys = self.light.setBlink
        self.lys = self.light.setLights
        self.bremselys = self.light.Brake

    def Dprint( self ):
        self.dbgCount += 1
        if self.dbgCount >= 10 :
            print(f"{self._heading=}")
            print(f"{self._leftDuty=}  {self._leftMotor.duty=}")
            self.dbgCount=0

    def coast( self ) :
        self._leftMotor.Coast()
        self._rightMotor.Coast()
        self._state = Car._STATE_STOP

    def stop( self ) :
        self._leftMotor.Stop()
        self._rightMotor.Stop()
        self._state = Car._STATE_STOP

    def frem( self ) :
        self._leftMotor.forward()
        self._rightMotor.forward()
        # initialize I-part of controller
        self._leftDuty = self._leftMotor.duty
        self._rightDuty = self._rightMotor.duty
        self._state = Car._STATE_FREM

    def bak( self ) :
        self._leftMotor.reverse()
        self._rightMotor.reverse()
        # initialize I-part of controller
        self._leftDuty = self._leftMotor.duty
        self._rightDuty = self._rightMotor.duty
        self._state = Car._STATE_BAK

    def _WaitForTargetHeading( self, angle ) :
        if angle is not None :
            self._heading = 0
            actualHeading = self._heading
            done = False
            while not done :
                if -30 < (angle - actualHeading) < 30 :
                    self._leftMotor.PWMPin.duty_u16( int( 20 * 655 ) )
                    self._rightMotor.PWMPin.duty_u16( int( 20 * 655 ) )
                elif -45 < (angle - actualHeading) < 45 :
                    self._leftMotor.PWMPin.duty_u16( int( 30 * 655 ) )
                    self._rightMotor.PWMPin.duty_u16( int( 30 * 655 ) )
                if 0 < angle < actualHeading :
                    done = True
                if 0 > angle > actualHeading :
                    done = True
                actualHeading = self._heading
            self.stop()
            self.set_hastighed( self._speed )
            sleep_ms( 100 )

    def drejH( self, angle=None ) :
        self._state = Car._STATE_STOP
        self._leftMotor.forward()
        self._rightMotor.Stop()
        if angle is not None :
            self._WaitForTargetHeading( angle )

    def drejV( self, angle=None ) :
        self._state = Car._STATE_STOP
        self._leftMotor.Stop()
        self._rightMotor.forward()
        if angle is not None :
            self._WaitForTargetHeading( -angle )

    def roterH( self, angle=None ) :
        self._state = Car._STATE_STOP
        self.set_hastighed( self._speed )
        self._leftMotor.forward()
        self._rightMotor.reverse()
        if angle is not None :
            self._WaitForTargetHeading( angle )

    def roterV( self, angle=None ) :
        self._state = Car._STATE_STOP
        self.set_hastighed( self._speed )
        self._leftMotor.reverse()
        self._rightMotor.forward()
        if angle is not None :
            self._WaitForTargetHeading( -angle )

    def set_hastighed( self, speed ) :
        self._speed = speed
        self._leftMotor.SetPower( self._speed )
        self._rightMotor.SetPower( self._speed )

    def __del__(self):
        self.deinit()
        
    def Distance( self ):
        return self.distance

    def _DriveStraightCtrlTick( self ):
        gyro = self._imu.gyro
        self._angularVelocity = gyro[2]

        ref = 0
        ki = 500000 / (self._timerPeriod * 1000)
        if self._state == Car._STATE_BAK :
            ki = -ki
        if self._state == Car._STATE_FREM or self._state == Car._STATE_BAK :
            self._leftDuty = self._leftDuty + (ref - self._angularVelocity) * -ki
            self._rightDuty = self._rightDuty + (ref - self._angularVelocity) * ki
            self._leftDuty = max( min( 65535, self._leftDuty ), 0 )
            self._rightDuty = max( min( 65535, self._rightDuty ), 0 )
            self._leftMotor.PWMPin.duty_u16( int( self._leftDuty ) )
            self._rightMotor.PWMPin.duty_u16( int( self._rightDuty ) )

        self._heading -= gyro[2] * self._timerPeriod / 1000

    def _tofTick( self ):
        self.distance = self.tofSensor.read()

if __name__ == '__main__' :
    bil = Car()
