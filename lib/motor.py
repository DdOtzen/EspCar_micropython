from machine import PWM, Pin
from micropython import const


class Motor:
    # Encoder steps pr. rotation when using x124 = 1
    ENCODER_STEPS_PR_ROTATION = const(200) # Based on manual measure, not very precise.

    def __init__( self, pins, useRegulator=False ):
        self.current_rps = 0
        self.duty = 0
        self.calibration = 1.0
        self.PWMPin = PWM( Pin( pins.Speed ), freq=1000, duty_u16=0 )
        self.forwardPin = Pin( pins.Forward, Pin.OUT )
        self.reversePin = Pin( pins.Reverse, Pin.OUT )
        self.useEnc = useRegulator
        self.encPinA = Pin( pins.enc_1, Pin.IN )
        self.encPinB = Pin( pins.enc_2, Pin.IN )
        self.SetPower( 0 )

    def SetPower( self, power_pct ):
        self._SetPower(power_pct)

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
        self.Stop()
