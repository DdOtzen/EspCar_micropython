from machine import Pin
from micropython import const, schedule
from time import sleep_ms
from neopixel import NeoPixel
from carPins import Pins

FRONTLIGHT = 12_800
BACKLIGHT = 9_600

FULLLIGHT = 65_535

class Lights:
    OFF = const(0)
    ON = const(1)
    RIGHT = const(1)
    LEFT = const(2)
    LOW_BEAM = const(1)
    HIGH_BEAM = const(2)
    LED_COUNT = const(12)

    CHANNEL_PIXELS = ((3, 4, 5), (0, 1, 2), (6, 7, 8), (9, 10, 11))
    LEFT_PIXELS = (0, 1, 2, 9, 10, 11)
    RIGHT_PIXELS = (3, 4, 5, 6, 7, 8)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    AMBER = (255, 80, 0)

    class _LightPair:

        def __init__(self, light_1, light_2):
            self.L1 = light_1
            self.L2 = light_2

        def on(self):
            self.L1.duty_u16(FULLLIGHT)
            self.L2.duty_u16(FULLLIGHT)

        def off(self):
            self.L1.duty_u16(0)
            self.L2.duty_u16(0)

    class _LightChannel:

        def __init__(self, lights, index):
            self.lights = lights
            self.index = index

        def duty_u16(self, duty=None):
            if duty is None:
                return self.lights.dutys[self.index]
            self.lights._setChannelDuty(self.index, duty)

        def duty(self, duty=None):
            if duty is None:
                return self.duty_u16() * 1023 // FULLLIGHT
            duty = max(0, min(1023, int(duty)))
            self.duty_u16(duty * FULLLIGHT // 1023)

        def on(self):
            self.duty_u16(FULLLIGHT)

        def off(self):
            self.duty_u16(0)

    def __init__(self):
        self.dutys = [0, 0, 0, 0]
        self.saveDutys = [0, 0, 0, 0]
        self.calibration = 1.0
        self.pixels = NeoPixel(Pin(Pins.Light.Data), self.LED_COUNT)
        self.blinking = self.OFF
        self.blinkState = 0
        self.blinkIdle = 0
        self._emergencyBlink = False
        self.lightFR = self._LightChannel(self, 0)
        self.lightFL = self._LightChannel(self, 1)
        self.lightRR = self._LightChannel(self, 2)
        self.lightRL = self._LightChannel(self, 3)
        self.frontLights = self._LightPair(self.lightFL, self.lightFR)
        self.rearLights = self._LightPair(self.lightRL, self.lightRR)
        self.leftLights = self._LightPair(self.lightFL, self.lightRL)
        self.rightLights = self._LightPair(self.lightFR, self.lightRR)

    def deinit(self):
        for i in range(762, 0, -1):
            d = i * FULLLIGHT // 761
            self.setDutys([d, d, d, d])
            sleep_ms(5)
        self.setDutys([0, 0, 0, 0])

    def setDutys(self, dutys):
        self.dutys[:] = [max(0, min(FULLLIGHT, int(duty))) for duty in dutys]
        self._render()

    def _setChannelDuty(self, index, duty):
        self.dutys[index] = max(0, min(FULLLIGHT, int(duty)))
        self._render()

    def _renderScheduled(self, _unused):
        self._render()

    def _render(self):
        for channel, indices in enumerate(self.CHANNEL_PIXELS):
            is_front = channel < 2
            color = self.WHITE if is_front else self.RED
            duty = self.dutys[channel]

            if self._emergencyBlink:
                duty = (FRONTLIGHT if is_front else BACKLIGHT) if self.blinkState else 0
            elif self.blinkState and self._channelIsBlinking(channel):
                color = self.AMBER
                duty = FULLLIGHT

            level = duty * 255 // FULLLIGHT
            pixel_color = tuple(component * level // 255 for component in color)
            for index in indices:
                self.pixels[index] = pixel_color

        self.pixels.write()

    def _channelIsBlinking(self, channel):
        if self.blinking == self.RIGHT:
            return channel in (0, 2)
        if self.blinking == self.LEFT:
            return channel in (1, 3)
        return False

    def EmergencyBlink(self):
        self._emergencyBlink = True
        self.blinking = self.OFF
        self.blinkState = 1
        self.blinkIdle = 0
        self._render()

    def Brake(self, level):
        if level == self.ON:
            self.saveDutys[:] = self.dutys
            self.dutys[2] = FULLLIGHT
            self.dutys[3] = FULLLIGHT
        else:  # self.OFF
            self.dutys[:] = self.saveDutys
        self.setDutys(self.dutys)

    def sluk(self):
        self.setLights(self.OFF)

    def kortLys(self):
        self.setLights(self.LOW_BEAM)

    def langLys(self):
        self.setLights(self.HIGH_BEAM)

    def setLights(self, level):
        if level == self.OFF:
            dutys = [0, 0, 0, 0]
        elif level == self.LOW_BEAM:
            dutys = [FRONTLIGHT, FRONTLIGHT, BACKLIGHT, BACKLIGHT]
        elif level == self.HIGH_BEAM:
            dutys = [FULLLIGHT, FULLLIGHT, BACKLIGHT, BACKLIGHT]
        else:  # Unknown default to off.
            dutys = [0, 0, 0, 0]
        self.setDutys(dutys)

    def blinkingTick(self):
        if not self._emergencyBlink and self.blinking not in (self.LEFT, self.RIGHT):
            return

        self.blinkIdle += 1
        if self.blinkIdle < 2:
            return
        self.blinkIdle = 0
        self.blinkState = 1 - self.blinkState
        schedule(self._renderScheduled, 0)

    def setBlink(self, direction):
        self.blinking = direction if direction in (self.LEFT, self.RIGHT) else self.OFF
        self.blinkState = 1 if self.blinking else 0
        self.blinkIdle = 0
        self._render()


if __name__ == "main":
    # demo code tja
    from time import sleep

    lygter = Lights()

    lygter.setLights(1)
    sleep(4)
    lygter.setLights(2)
    sleep(4)
    lygter.setLights(0)
