from machine import Pin, PWM, Encoder
from lib.carPins import Pins
from machine import Pin, PWM, I2C, Timer
from mpu6500 import MPU6500, SF_G, SF_DEG_S

try:
    from time import sleep_ms, time_ns
except ImportError:
    from time import sleep
    def sleep_ms( ms ):
        sleep( ms / 1000 )

try:
    from micropython import const
except ImportError:
    # we get here if running cPython on host.
    def const( x ):
        return x

class Motor:
    # Encoder steps pr. rotation when using x124 = 1
    ENCODER_STEPS_PR_ROTATION = const(200) # Based on manual measure, not very precise.

    def __init__( self, pins, useRegulator=True ):
        self.current_rps = 0
        self.duty = 0
        self.calibration = 1.0
        self.PWMPin = PWM( Pin( pins.Speed ), freq=1000, duty_u16=0 )
        self.forwardPin = Pin( pins.Forward, Pin.OUT )
        self.reversePin = Pin( pins.Reverse, Pin.OUT )
        self.useEnc = useRegulator
        self.encPinA = Pin( pins.enc_1, Pin.IN )
        self.encPinB = Pin( pins.enc_2, Pin.IN )
        self.encoder = Encoder( -1, phase_a=self.encPinA, phase_b=self.encPinB, filter_ns=0, x124=1 )
        if self.useEnc:
            self.regulator = DCMotorController(self)
        self.SetPower( 0 )

    def motor_100ms_tick( self ) -> float:
        # Calculate current speed (rotations per 100ms or 0.1s)
        enc_steps_100ms = self._encDeltaValue()
        enc_steps_1s = enc_steps_100ms * 10
        self.current_rps = enc_steps_1s / self.ENCODER_STEPS_PR_ROTATION

        if self.useEnc :
            self.regulator.regulate_speed( enc_steps_1s )
        return self.current_rps

    def encValue( self ):
        return self.encoder.value()

    def _encDeltaValue( self ):
        return self.encoder.value(0)

    def SetPower( self, power_pct ):
        self._SetPower(power_pct)
        self.regulator.SetSpeed( power_pct * 13, power_pct )

    def _SetPower( self, power_pct ):
        if power_pct == 100 :
            self.duty = 65535
        else:
            self.duty = power_pct * 655
        self.PWMPin.duty_u16( self.duty )
        self.power_pct = power_pct

    def forward( self ):
        self.forwardPin.on()
        self.reversePin.off()

    def reverse( self ):
        self.forwardPin.off()
        self.reversePin.on()

    def Stop( self ):
        self.forwardPin.on()
        self.reversePin.on()

    def Coast( self ):

    def deinit( self ):
        self.encoder.deinit()

class Lights:
    class _Light:
        def __init__( self, pins ):
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



class DCMotorController :

    def __init__( self, motor: Motor ) :
        self.targetRps :float = 0.0
        self.prev_error = 0.0
        self.prev_enc_value = 0.0
        self.integral = 0.0
        self.motor = motor
        self.current_rpm = 0

        # PID coefficients
        self.ff_power = 0
        self.Kp = 0.1
        self.Ki = 0.000001
        self.Kd = 0.0

    def SetSpeed( self, rps : float, feed_forward_power : float ):
        self.targetRps = rps
        self.ff_power = feed_forward_power

    def regulate_speed( self, current_rps ) :

        # PID calculations
        error = self.targetRps - current_rps

        proportional = self.Kp * error
        self.integral += error * self.Ki
        derivative = ( self.prev_error - error ) * self.Kd

        # Calculate output
        powerDelta = proportional + self.integral + derivative

        # Constrain power to [0, 100]
        power = max( 0, min( 100, self.ff_power + powerDelta ) )

        # Update motor power
        self.motor._SetPower( int( power ) )

        # Update previous values
        self.prev_error = error


class Car:

    def __init__( self, useRegulator: bool = True ):
        self.light = Lights()
        self.rightMotor = Motor( Pins.Motor.Right, useRegulator )
        self.leftMotor  = Motor( Pins.Motor.Left, useRegulator )
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
        self.leftMotor.Coast()
        self.rightMotor.Coast()

    def stop( self ):
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
        self.speed = speed
        self.leftMotor.SetPower( self.speed )
        self.rightMotor.SetPower( self.speed )

    def deinit( self ):
        self.coast()
        self.leftMotor.deinit()
        self.rightMotor.deinit()

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
