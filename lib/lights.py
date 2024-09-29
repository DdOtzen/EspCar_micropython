from machine import PWM, Pin
from micropython import const
from time import sleep_ms
from carPins import Pins
import math

# constants
FRONTLIGHT = 12_800
BACKLIGHT = 9_600

FULLLIGHT = 65_535
HALFLIGHT = 32_767
QUATERLIGHT = 16_383
NOLIGHT = 0

class Lights:
    blinking = 0
    blinkState = 0
    OFF = const(0)
    ON = const(1)
    RIGHT = const(1)
    LEFT = const(2)
    LOW_BEAM = const(1)
    HIGH_BEAM = const(2)

    class _LightPair:

        def __init__(self, light_1: type(PWM), light_2: type(PWM)):
            self.L1 = light_1
            self.L2 = light_2

        def on(self):
            self.L1.duty(1023)
            self.L2.duty(1023)

        def off(self):
            self.L1.duty(0)
            self.L2.duty(0)

    def __init__(self):
        self.dutys = [0, 0, 0, 0]
        self.saveDutys = [0, 0, 0, 0]
        self.calibration = 1.0
        self.lightFR = PWM(Pins.Light.Front.Right, freq=1000, duty_u16=self.dutys[0])
        self.lightFL = PWM(Pins.Light.Front.Left, freq=1000, duty_u16=self.dutys[1])
        self.lightRR = PWM(Pins.Light.Rear.Right, freq=1000, duty_u16=self.dutys[2])
        self.lightRL = PWM(Pins.Light.Rear.Left, freq=1000, duty_u16=self.dutys[3])
        self.frontLights = self._LightPair(self.lightFL, self.lightFR)
        self.rearLights = self._LightPair(self.lightRL, self.lightRR)
        self.leftLights = self._LightPair(self.lightFL, self.lightRL)
        self.rightLights = self._LightPair(self.lightFR, self.lightRR)
        self.blinkIdle = 0
    def deinit(self):
        for i in range(762,0,-1):
            d = int( math.sinh( i / 100 ) )*64
            self.setDutys([d, d, d, d])
            sleep_ms(5)
        self.setDutys([0, 0, 0, 0])

    def setDutys(self, dutys):
        self.lightFR.duty_u16(dutys[0])
        self.lightFL.duty_u16(dutys[1])
        self.lightRR.duty_u16(dutys[2])
        self.lightRL.duty_u16(dutys[3])

    def EmergencyBlink(self):
        self.lightFR.duty_u16( FRONTLIGHT )
        self.lightFR.freq(10)
        self.lightFL.duty_u16( FRONTLIGHT )
        self.lightFL.freq(10)
        self.lightRR.duty_u16( BACKLIGHT )
        self.lightRR.freq(10)
        self.lightRL.duty_u16( BACKLIGHT )
        self.lightRL.freq(10)

    def Brake(self, level):
        if level == self.ON:
            self.saveDutys = self.dutys.copy()
            self.dutys[2] = FULLLIGHT
            self.dutys[3] = FULLLIGHT
        else:  # self.OFF
            self.dutys = self.saveDutys.copy()
        self.setDutys(self.dutys)

    def sluk(self):
        self.setLights(self.OFF)

    def kortLys(self):
        self.setLights(self.LOW_BEAM)

    def langLys(self):
        self.setLights(self.HIGH_BEAM)

    def setLights(self, level):
        if level == self.OFF:
            self.dutys[0] = 0
            self.dutys[1] = 0
            self.dutys[2] = 0
            self.dutys[3] = 0
        elif level == self.LOW_BEAM:
            self.dutys[0] = FRONTLIGHT
            self.dutys[1] = FRONTLIGHT
            self.dutys[2] = BACKLIGHT
            self.dutys[3] = BACKLIGHT
        elif level == self.HIGH_BEAM:
            self.dutys[0] = FULLLIGHT
            self.dutys[1] = FULLLIGHT
            self.dutys[2] = BACKLIGHT
            self.dutys[3] = BACKLIGHT
        else:  # Unknown default to off.
            self.dutys[0] = 0
            self.dutys[1] = 0
            self.dutys[2] = 0
            self.dutys[3] = 0
        self.setDutys(self.dutys)

    def blinkingTick(self):
        if self.blinkIdle >= 1:
            self.blinkIdle = 0
        else:
            self.blinkIdle += 1
            return
        
        if self.blinking == Lights.RIGHT:
            if self.blinkState == 0:
                self.blinkState = 1
                self.lightFR.duty_u16(FULLLIGHT)
                self.lightRR.duty_u16(FULLLIGHT)
            else:
                self.blinkState = 0
                self.lightFR.duty_u16(self.dutys[0])
                self.lightRR.duty_u16(self.dutys[1])
        elif self.blinking == Lights.LEFT:
            if self.blinkState == 0:
                self.blinkState = 1
                self.lightFL.duty_u16(FULLLIGHT)
                self.lightRL.duty_u16(FULLLIGHT)
            else:
                self.blinkState = 0
                self.lightFL.duty_u16(0)
                self.lightRL.duty_u16(0)
        else:
            self.setDutys(self.dutys)

    def setBlink(self, direction):
        self.blinking = direction
        #        if (self.blinking == 0):		# restore old levels
        self.setDutys(self.dutys)
        if self.blinking == Lights.RIGHT:  # blink right
            self.lightFR.duty_u16(FULLLIGHT)
            self.lightRR.duty_u16(FULLLIGHT)
        elif self.blinking == Lights.LEFT:
            self.lightFL.duty_u16(FULLLIGHT)
            self.lightRL.duty_u16(FULLLIGHT)


if __name__ == "main":
    # demo code tja
    from time import sleep

    lygter = Lights()

    lygter.setLights(1)
    sleep(4)
    lygter.setLights(2)
    sleep(4)
    lygter.setLights(0)
