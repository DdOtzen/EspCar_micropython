from machine import PWM, Pin, Encoder
from micropython import const


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

    def Coast( self ) :
        self.forwardPin.off()
        self.reversePin.off()

    def deinit( self ):
        self.encoder.deinit()


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
